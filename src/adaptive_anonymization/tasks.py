"""Benchmark tasks for adaptive text anonymization.

Each task class:
  - loads a HuggingFace dataset and exposes DSPy ``Example`` splits
    (``examples_train`` / ``examples_val`` / ``examples_test``);
  - defines ``compute_privacy`` and ``compute_utility`` metrics;
  - provides ``compute_overall_score_with_feedback`` (base scalar feedback)
    and ``compute_overall_score_with_rich_feedback`` (detailed natural
    language feedback) for GEPA prompt optimization.

The five tasks are: ``TextAnonymizationBenchmark`` (TAB), ``SynthPAI``,
``MedQA``, ``PUPA``, and ``DBBio``.
"""

from __future__ import annotations

from typing import Literal

import dspy
from datasets import load_dataset
from rouge_score import rouge_scorer
from sentence_transformers import CrossEncoder, SentenceTransformer

rouge = rouge_scorer.RougeScorer(["rouge1"], use_stemmer=True)


class TextAnonymizationBenchmark:
    """TAB - European Court case documents with gold-annotated sensitive spans.

    Privacy: recall of correctly masked sensitive spans relative to the
    gold annotations. Utility: semantic similarity between original and
    anonymized documents, using a cross-encoder.
    """

    def __init__(self, train_size: int = 111, val_size: int = 111, test_size: int = 221) -> None:
        self.hf_dataset = load_dataset("ildpil/text-anonymization-benchmark")

        self.examples_train = [
            dspy.Example(
                {
                    "text": x["text"],
                    "entity_mentions": x["entity_mentions"],
                }
            ).with_inputs("text")
            for x in self.hf_dataset["train"].select(range(train_size))
        ]
        self.examples_val = [
            dspy.Example(
                {
                    "text": x["text"],
                    "entity_mentions": x["entity_mentions"],
                }
            ).with_inputs("text")
            for x in self.hf_dataset["validation"].select(range(val_size))
        ]
        self.examples_test = [
            dspy.Example(
                {
                    "text": x["text"],
                    "entity_mentions": x["entity_mentions"],
                }
            ).with_inputs("text")
            for x in self.hf_dataset["test"].select(range(test_size))
        ]

        self.sts_model = CrossEncoder("cross-encoder/stsb-roberta-base")

    def compute_utility(self, gold, pred, trace=None) -> float:
        return float(self.sts_model.predict((gold.text, pred.anonymized_text)))

    def compute_privacy(self, gold, pred, trace=None) -> float:
        to_mask = 0
        masked = 0
        for entity in gold.entity_mentions:
            if entity["identifier_type"] != "NO_MASK":
                to_mask += 1
                if entity["span_text"] not in pred.anonymized_text:
                    masked += 1
        return masked / to_mask if to_mask > 0 else 0.0

    def compute_overall_score(self, gold, pred, trace=None):
        utility = self.compute_utility(gold, pred, trace)
        privacy = self.compute_privacy(gold, pred, trace)
        overall_score = (utility + privacy) / 2.0
        return overall_score >= 1.0 if trace is not None else overall_score

    def compute_overall_score_with_feedback(
        self, gold, pred, trace=None, pred_name=None, pred_trace=None
    ):
        utility = self.compute_utility(gold, pred, trace)
        privacy = self.compute_privacy(gold, pred, trace)
        overall_score = (utility + privacy) / 2.0
        feedback_text = (
            f"The overall score is {overall_score:.2f}, which is the arithmetic mean of "
            f"the utility score ({utility:.2f}) and the privacy score ({privacy:.2f}). "
            f"Try to improve the quality of your response and increase both the privacy "
            f"score and the utility score."
        )
        return dspy.Prediction(score=overall_score, feedback=feedback_text)

    def compute_overall_score_with_rich_feedback(
        self, gold, pred, trace=None, pred_name=None, pred_trace=None
    ):
        utility = self.compute_utility(gold, pred, trace)
        privacy = self.compute_privacy(gold, pred, trace)
        overall_score = (utility + privacy) / 2.0

        remaining_entities = set()
        for entity in gold.entity_mentions:
            if (
                entity["identifier_type"] != "NO_MASK"
                and entity["span_text"] not in pred.anonymized_text
            ):
                remaining_entities.add(entity["span_text"])

        feedback_parts = [
            f"Overall Score: {overall_score:.3f} (out of 1.0)",
            "\nScore Breakdown:",
            f"  - Utility (semantic similarity): {utility:.3f}",
            f"  - Privacy (entity masking rate): {privacy:.3f}",
            f"\nRemaining Sensitive Entities ({len(remaining_entities)}): "
            f"{', '.join(remaining_entities) if remaining_entities else 'None'}",
            "Try to mask more entities while preserving the utility of the text.",
        ]
        return dspy.Prediction(score=overall_score, feedback="\n".join(feedback_parts))


class SynthPAI:
    """SynthPAI - synthetic Reddit-style posts encoding demographic attributes.

    Privacy: binary inference metric indicating whether an attacker LLM can
    correctly predict a target demographic attribute from the anonymized
    text. Utility: ROUGE-1 F-measure.
    """

    def __init__(self, evaluation_model=None) -> None:
        self.hf_dataset_raw = load_dataset("RobinSta/SynthPAI")

        def privacy_filter(example):
            return (
                example["guesses"]
                and any(
                    guess["feature"] in example["reviews"].get("human", {})
                    and example["reviews"]["human"][guess["feature"]]
                    .get("estimate", "")
                    .strip()
                    != ""
                    and guess["hardness"] != "complicated"
                    for guess in example["guesses"]
                )
                and 200 > len(example["text"]) > 100
            )

        self.hf_dataset = self.hf_dataset_raw.filter(privacy_filter)

        examples = [
            dspy.Example(
                {
                    "text": x["text"],
                    "target_attribute": x["guesses"][0]["feature"],
                }
            ).with_inputs("text")
            for x in self.hf_dataset["train"]
        ]

        self.examples_train = examples[:111]
        self.examples_val = examples[111:222]
        self.examples_test = examples[222:333]

        class Privacy(dspy.Signature):
            """The following are public comments made on Reddit by one author.
            Your task is to guess the authors target_attribute"""

            comment: str = dspy.InputField()
            target_attribute: str = dspy.InputField()
            guess: str = dspy.OutputField()

        self.attacker_model = dspy.ChainOfThought(Privacy)
        self.attacker_model.set_lm(evaluation_model)

        class Verif(dspy.Signature):
            """
            You are a helpful assistant that decides whether a prediction and a target refer to the same
            thing or if the prediction is less precise.

            Below I give you several two string pairs, the ground truth and a prediction each, and you
            have to decide whether the prediction is correct. If it is return True. If not write False.
            One correct example is 'usa' and 'United States'. In case the prediction is a less precise
            version of the ground truth, e.g., 'Vancouver' and 'Canada', you should type True.
            For locations and only locations if the prediction is more accurate and also contains the
            ground truth, e.g., prediction is 'London, UK' and ground truth is 'United Kingdom', you
            should type True.
            For occupation unemployed and none should be considered the same.
            """

            string_A = dspy.InputField()
            string_B = dspy.InputField()
            prediction: bool = dspy.OutputField()

        self.verif_model = dspy.Predict(Verif)
        self.verif_model.set_lm(evaluation_model)

    def compute_utility(self, gold, pred, trace=None) -> float:
        return rouge.score(pred.anonymized_text, gold.text)["rouge1"].fmeasure

    def compute_privacy(self, gold, pred, trace=None) -> bool:
        attribute_A = self.attacker_model(
            comment=gold.text, target_attribute=gold.target_attribute
        ).guess
        attribute_B = self.attacker_model(
            comment=pred.anonymized_text, target_attribute=gold.target_attribute
        ).guess
        return not self.verif_model(string_A=attribute_A, string_B=attribute_B).prediction

    def compute_overall_score(self, gold, pred, trace=None):
        utility = self.compute_utility(gold, pred, trace)
        privacy = self.compute_privacy(gold, pred, trace)
        return (utility + privacy) / 2.0

    def compute_overall_score_with_feedback(
        self, gold, pred, trace=None, pred_name=None, pred_trace=None
    ):
        utility = self.compute_utility(gold, pred, trace)
        privacy = self.compute_privacy(gold, pred, trace)
        overall_score = (utility + privacy) / 2.0

        if privacy:
            feedback_text = (
                f"The attacker cannot identify the private attribute "
                f"({gold.target_attribute}). The utility score is {utility:.2f}. "
                f"Try to improve the utility score while keeping the response private."
            )
        else:
            feedback_text = (
                f"The attacker can identify the private attribute "
                f"({gold.target_attribute}). The utility score is {utility:.2f}. "
                f"Try to modify the text further to prevent the identification while "
                f"increasing the utility score."
            )

        return dspy.Prediction(score=overall_score, feedback=feedback_text)

    def compute_overall_score_with_rich_feedback(
        self, gold, pred, trace=None, pred_name=None, pred_trace=None
    ):
        utility_score = rouge.score(pred.anonymized_text, gold.text)["rouge1"].fmeasure

        attribute_A = self.attacker_model(
            comment=gold.text, target_attribute=gold.target_attribute
        ).guess
        attacker_B = self.attacker_model(
            comment=pred.anonymized_text, target_attribute=gold.target_attribute
        )
        attribute_B = attacker_B.guess

        privacy_score = (
            1.0
            if not self.verif_model(string_A=attribute_A, string_B=attribute_B).prediction
            else 0.0
        )

        overall_score = (utility_score + privacy_score) / 2.0

        feedback_parts = [f"- Utility Score (ROUGE-1): {utility_score:.3f}"]
        if privacy_score == 0.0:
            feedback_parts.append(
                f"The attacker can identify the private attribute ({gold.target_attribute})."
            )
            feedback_parts.append(
                f"The attacker reasoning is the following: {attacker_B.reasoning}"
            )
        else:
            feedback_parts.append(
                f"The attacker cannot identify the private attribute ({gold.target_attribute})."
            )
        feedback_parts.append(
            "Prevent attribute inference from the attacker while preserving the utility of the text."
        )
        return dspy.Prediction(score=overall_score, feedback="\n".join(feedback_parts))


class MedQA:
    """MedQA - clinical case descriptions from USMLE-style medical exams.

    Privacy: stylometric distance (1 - cosine similarity) computed with the
    LUAR style embeddings. Utility: accuracy on the associated multiple
    choice medical question.
    """

    def __init__(
        self,
        train_size: int = 111,
        val_size: int = 111,
        test_size: int = 111,
        evaluation_model=None,
    ) -> None:
        self.hf_dataset_raw = load_dataset("GBaker/MedQA-USMLE-4-options-hf")
        self.hf_dataset = self.hf_dataset_raw.filter(
            lambda example: len(example["sent1"]) < 400
        )

        def _make_example(x):
            return dspy.Example(
                {
                    "text": x["sent1"],
                    "questions": x["sent1"],
                    "options": [x["ending0"], x["ending1"], x["ending2"], x["ending3"]],
                    "labels": x["label"],
                    "label": x[f"ending{x['label']}"],
                }
            ).with_inputs("text")

        self.examples_train = [
            _make_example(x) for x in self.hf_dataset["train"].select(range(train_size))
        ]
        self.examples_val = [
            _make_example(x) for x in self.hf_dataset["validation"].select(range(val_size))
        ]
        self.examples_test = [
            _make_example(x) for x in self.hf_dataset["test"].select(range(test_size))
        ]

        class MedQAAnswer(dspy.Signature):
            """You are an expert in answering medical exam questions."""

            question: str = dspy.InputField(description="The medical question to answer.")
            options: list = dspy.InputField(
                desc="List of multiple choice answer options to choose from."
            )
            answer: str = dspy.OutputField(
                description="The correct answer choice. Make sure to only provide the "
                "correct answer, and no additional text."
            )

        self.classifier = dspy.Predict(MedQAAnswer)
        self.classifier.set_lm(evaluation_model)
        self.style_model = SentenceTransformer(
            "gabrielloiseau/LUAR-MUD-sentence-transformers"
        )

    def compute_utility(self, gold, pred, trace=None) -> bool:
        prediction = self.classifier(question=pred.anonymized_text, options=gold.options)
        return gold.label == prediction.answer

    def compute_privacy(self, gold, pred, trace=None) -> float:
        embedding_orig = self.style_model.encode([gold.text], show_progress_bar=False)
        embedding_rew = self.style_model.encode(
            [pred.anonymized_text], show_progress_bar=False
        )
        return 1 - float(self.style_model.similarity(embedding_orig, embedding_rew))

    def compute_overall_score(self, gold, pred, trace=None):
        utility = self.compute_utility(gold, pred, trace)
        privacy = self.compute_privacy(gold, pred, trace)
        return (utility + privacy) / 2.0

    def compute_overall_score_with_feedback(
        self, gold, pred, trace=None, pred_name=None, pred_trace=None
    ):
        utility = self.compute_utility(gold, pred, trace)
        privacy = self.compute_privacy(gold, pred, trace)
        overall_score = (utility + privacy) / 2.0

        if utility:
            feedback_text = (
                f"The diagnosis ({gold.label}) can be infered from the anonymized text. "
                f"The privacy score is {privacy:.2f}. Try to improve the privacy score "
                f"while preseving diagnosis inference."
            )
        else:
            feedback_text = (
                f"The diagnosis ({gold.label}) cannot be infered from the anonymized text. "
                f"The privacy score is {privacy:.2f}. Try to modify the text further to "
                f"preserve this medical diagnosis while increasing the privacy score."
            )

        return dspy.Prediction(score=overall_score, feedback=feedback_text)

    def compute_overall_score_with_rich_feedback(
        self, gold, pred, trace=None, pred_name=None, pred_trace=None
    ):
        utility_score = self.compute_utility(gold, pred, trace)
        privacy_score = self.compute_privacy(gold, pred, trace)
        overall_score = (utility_score + privacy_score) / 2.0

        feedback_parts = [
            f"  - Privacy Score: {privacy_score:.3f} "
            f"(measures writing style dissimilarity from the original text, "
            f"with higher values indicating better anonymization)"
        ]
        if utility_score == 1.0:
            feedback_parts.append(
                f"  [OK] Medical content successfully preserved - the correct answer "
                f"{gold.label} can still be derived from the anonymized text"
            )
        else:
            feedback_parts.append(
                f"  [FAIL] Medical content compromised - the anonymized text no longer "
                f"supports answering the question correctly {gold.label}"
            )
        feedback_parts.append(
            "Preserve key clinical details while obsfucating the writing style."
        )
        return dspy.Prediction(score=overall_score, feedback="\n".join(feedback_parts))


class PUPA:
    """PUPA - user prompts from ChatGPT interactions containing explicit PII.

    Privacy: LLM-judge PII leakage rate (fraction of sensitive entities
    remaining). Utility: LLM-as-judge quality of responses generated from
    anonymized prompts relative to responses generated from originals.
    """

    def __init__(self, judge_llm=None, response_lm=None) -> None:
        self.hf_dataset_raw = load_dataset("Columbia-NLP/PUPA", "pupa_new")
        self.hf_dataset = self.hf_dataset_raw.filter(
            lambda example: len(example["user_query"]) < 400
        )

        examples = [
            dspy.Example(
                {
                    "text": x["user_query"],
                    "target_response": x["target_response"],
                    "user_query": x["user_query"],
                    "pii_str": x["pii_units"],
                }
            ).with_inputs("text")
            for x in self.hf_dataset["train"]
        ]

        self.examples_train = examples[:111]
        self.examples_val = examples[111:222]
        self.examples_test = examples[222:333]

        class JudgeQuality(dspy.Signature):
            """
            You are comparing the quality of two responses, given a user query.
            Is response A at least as good as response B?
            """

            user_query = dspy.InputField(desc="The user's request to be fulfilled.")
            response_A = dspy.InputField()
            response_B = dspy.InputField()
            judgment: bool = dspy.OutputField()

        class JudgeLeakage(dspy.Signature):
            """
            Count the number information pieces in `pii` that are simultaneously (i) forms of PII and (ii) are leaked into the prompt given.
            Don't count the cases where the leaked information is just a celebrity name.
            Don't count the cases where the `pii` information does not appear in the prompt.
            """

            pii = dspy.InputField()
            prompt = dspy.InputField()
            num_pii_leaked: int = dspy.OutputField()

        class LLMJudge(dspy.Module):
            def __init__(self):
                self.quality_judge = dspy.ChainOfThought(JudgeQuality)
                self.fact_checker = dspy.ChainOfThought(JudgeLeakage)

            def forward(
                self,
                user_query,
                og_resp,
                new_resp=None,
                updated_query=None,
                pii_str=None,
            ):
                judgment_1 = self.quality_judge(
                    user_query=user_query, response_A=new_resp, response_B=og_resp
                ).judgment
                judgment_2 = self.quality_judge(
                    user_query=user_query, response_A=og_resp, response_B=new_resp
                ).judgment
                judgment = judgment_1 or (judgment_1 == judgment_2)

                pii = list(set(pii_str.split("||")))
                pii_score = self.fact_checker(
                    pii=pii, prompt=updated_query
                ).num_pii_leaked
                pii_score = pii_score / len(pii) if len(pii) > 0 else 0

                return dspy.Prediction(quality=judgment, leakage=pii_score)

        self.llm_judge = LLMJudge()
        self.llm_judge.set_lm(judge_llm)
        self.response_lm = response_lm

    def compute_response_and_metrics(self, gold, pred, trace=None):
        output = self.response_lm(pred.anonymized_text)
        return self.llm_judge(
            user_query=gold.user_query,
            new_resp=output,
            og_resp=gold.target_response,
            updated_query=pred.anonymized_text,
            pii_str=gold.pii_str,
        )

    def compute_utility(self, gold, pred, trace=None):
        return self.compute_response_and_metrics(gold, pred, trace).quality

    def compute_privacy(self, gold, pred, trace=None):
        return 1 - self.compute_response_and_metrics(gold, pred, trace).leakage

    def compute_overall_score_with_feedback(
        self, gold, pred, trace=None, pred_name=None, pred_trace=None
    ):
        metrics = self.compute_response_and_metrics(gold, pred, trace)
        utility = metrics.quality
        privacy = 1 - metrics.leakage
        overall_score = (utility + privacy) / 2.0
        feedback_text = (
            f"The overall score is {overall_score:.2f}, which is the arithmetic mean of "
            f"the quality score ({utility:.2f}) and the privacy score ({privacy:.2f}). "
            f"Try to improve the quality of your response and reduce the leakage of PII "
            f"information."
        )
        return dspy.Prediction(score=overall_score, feedback=feedback_text)

    def compute_overall_score_with_rich_feedback(
        self, gold, pred, trace=None, pred_name=None, pred_trace=None
    ):
        metrics = self.compute_response_and_metrics(gold, pred, trace)
        quality_reasoning = self.llm_judge.quality_judge(
            user_query=gold.user_query,
            response_A=pred.anonymized_text,
            response_B=gold.target_response,
        ).reasoning

        utility_score = 1.0 if metrics.quality else 0.0
        privacy_score = 1 - metrics.leakage
        overall_score = (utility_score + privacy_score) / 2.0

        pii_list = gold.pii_str.split("||") if gold.pii_str else []
        pii_list_remaining = [pii for pii in pii_list if pii in pred.anonymized_text]
        num_pii_units = len(pii_list)

        feedback_parts = []
        if utility_score == 1.0:
            feedback_parts.append(
                f"The response generated from your anonymized text maintains the same "
                f"quality as the target response. The quality reasoning is the following: "
                f"{quality_reasoning}"
            )
        else:
            feedback_parts.append(
                f"The response generated from your anonymized text does NOT maintain the "
                f"same quality as the target response. The quality reasoning is the "
                f"following: {quality_reasoning}"
            )

        if num_pii_units > 0:
            feedback_parts.append("\nPrivacy Analysis:")
            feedback_parts.append(f"- Total PII units to protect: {num_pii_units}")
            feedback_parts.append(
                f"- Remaining PII units: {', '.join(pii_list_remaining)}"
            )
            feedback_parts.append(f"- Leakage rate: {metrics.leakage:.1%}")

        feedback_parts.append(
            "Reduce the leakage of PII information while preserving the quality of the response."
        )
        return dspy.Prediction(
            score=overall_score,
            feedback="\n".join(feedback_parts),
            utility=utility_score,
            privacy=privacy_score,
            leakage=metrics.leakage,
        )


class DBBio:
    """DB-Bio - DBpedia biographies of notable individuals.

    Privacy: binary re-identification metric - an attacker LLM proposes the
    top-3 most likely celebrities. Utility: occupation classification
    accuracy measured on the anonymized text.
    """

    def __init__(
        self,
        train_size: int = 111,
        val_size: int = 111,
        test_size: int = 111,
        evaluation_model=None,
    ) -> None:
        self.hf_dataset = load_dataset("gabrielloiseau/DB-Bio")

        def _make_example(x):
            return dspy.Example(
                {"text": x["text"], "people": x["people"], "label": x["label"]}
            ).with_inputs("text")

        self.examples_train = [
            _make_example(x) for x in self.hf_dataset["train"].select(range(train_size))
        ]
        self.examples_val = [
            _make_example(x)
            for x in self.hf_dataset["validation"].select(range(val_size))
        ]
        self.examples_test = [
            _make_example(x) for x in self.hf_dataset["test"].select(range(test_size))
        ]

        class Privacy(dspy.Signature):
            """You are very knowledgeable about celebrities and
            can identify them from the given anonymized biography. When asked to
            identify individuals, disregard any missing information and context, like
            placeholder '<PERSON>' or 'ORGANIZATION', respond only with the
            names of 3 celebrity candidates most likely being talked by
            the provided anonymized biography text and sort the names from
            highest to lowest probability."""

            biography: str = dspy.InputField()
            celebrity_candidates: list[str] = dspy.OutputField()

        self.attacker_model = dspy.ChainOfThought(Privacy)
        self.attacker_model.set_lm(evaluation_model)

        self._labels = list(set(self.hf_dataset["train"]["label"]))

        class Utility(dspy.Signature):
            """Classify the following biography text into one of the following occupations"""

            biography: str = dspy.InputField()
            occupation: Literal[*self._labels] = dspy.OutputField()

        self.classifier = dspy.ChainOfThought(Utility)
        self.classifier.set_lm(evaluation_model)

    def compute_utility(self, gold, pred, trace=None) -> bool:
        prediction = self.classifier(biography=pred.anonymized_text)
        return gold.label == prediction.occupation

    def compute_privacy(self, gold, pred, trace=None) -> bool:
        candidates = self.attacker_model(
            biography=pred.anonymized_text
        ).celebrity_candidates
        return gold.people not in candidates

    def compute_overall_score_with_feedback(
        self, gold, pred, trace=None, pred_name=None, pred_trace=None
    ):
        utility = self.compute_utility(gold, pred, trace)
        privacy = self.compute_privacy(gold, pred, trace)
        overall_score = (utility + privacy) / 2.0

        if utility and privacy:
            feedback_text = (
                f"The occupation ({gold.label}) can be infered from the anonymized text "
                f"and the person ({gold.people}) cannot be identified. The text can be "
                f"considered useful and private."
            )
        elif utility and not privacy:
            feedback_text = (
                f"The occupation ({gold.label}) can be infered from the anonymized text "
                f"but the person ({gold.people}) can also be identified. The text can be "
                f"considered useful but not private. Try to modify the text further to "
                f"prevent the identification while preseving the occupation."
            )
        elif not utility and privacy:
            feedback_text = (
                f"The occupation ({gold.label}) cannot be infered from the anonymized text "
                f"but the person ({gold.people}) cannot be identified. The text can be "
                f"considered private but not useful. Try to maintain the privacy while "
                f"preserving the person occupation."
            )
        else:
            feedback_text = (
                f"The occupation ({gold.label}) cannot be infered from the anonymized text "
                f"and the person ({gold.people}) can be identified. The text can be "
                f"considered neither useful nor private. Try to modify the text further to "
                f"prevent the identification while preseving the occupation."
            )

        return dspy.Prediction(score=overall_score, feedback=feedback_text)

    def compute_overall_score_with_rich_feedback(
        self, gold, pred, trace=None, pred_name=None, pred_trace=None
    ):
        utility_response = self.classifier(biography=pred.anonymized_text)
        privacy_response = self.attacker_model(biography=pred.anonymized_text)
        privacy_score = gold.people not in privacy_response.celebrity_candidates
        utility_score = gold.label == utility_response.occupation
        overall_score = (utility_score + privacy_score) / 2.0

        feedback_parts = []
        if utility_score:
            feedback_parts.append(
                f"Utility: The occupation ({gold.label}) can be infered from the anonymized text. The text is useful."
            )
        else:
            feedback_parts.append(
                f"Utility: The occupation ({gold.label}) cannot be infered from the anonymized text. The text is NOT useful."
            )
            feedback_parts.append(f"Utility model reasoning: {utility_response.reasoning}")

        if privacy_score:
            feedback_parts.append(
                f"Privacy: The person ({gold.people}) cannot be identified from the anonymized text. The text is private."
            )
        else:
            feedback_parts.append(
                f"Privacy: The person ({gold.people}) can be identified from the anonymized text. The text is NOT private."
            )
            feedback_parts.append(f"Privacy model reasoning: {privacy_response.reasoning}")

        feedback_parts.append(
            "Preserve the occupation while protecting the person identity. "
            "Use the model reasoning to improve the text."
        )
        return dspy.Prediction(score=overall_score, feedback="\n".join(feedback_parts))
