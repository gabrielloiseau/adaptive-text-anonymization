# MedQA - Qwen3-30B-A3B

- Task: `medqa`
- Model: `qwen_3_30b` (Qwen3-30B-A3B)
- Stage: `dynamic`
- Source: `trained_models/medqa/qwen_3_30b/dynamic`

## Optimized prompt

```
Given a clinical text input containing patient details and a medical question, generate a new anonymized version—`anonymized_text`—that achieves maximum privacy through comprehensive de-identification and stylistic obfuscation, while preserving full diagnostic and clinical reasoning fidelity. This requires careful, multi-layered manipulation grounded in both clinical precision and privacy engineering principles.

Your output must strictly adhere to the following constraints, each of which is critical for success based on observed failures in prior examples:

1. **Preserve Diagnostic Fidelity with Surgical Precision**:
   - Do not remove, generalize, or obscure any clinically diagnostic fact that is essential to arriving at the correct answer. The anonymized text must allow a trained physician to derive the intended answer with confidence—this is non-negotiable.
   - **Retain key diagnostic landmarks exactly as they inform the mechanism or diagnosis**, including:
     - Specific anatomic or pathologic findings (e.g., “white blood cell casts” must remain; never generalize to “inflammatory casts” or “cellular elements”).
     - Laboratory relationships that define a syndrome (e.g., “urine osmolality 334 mOsm/kg > serum osmolality ~285 mOsm/kg” → must be preserved as “urine osmolality was markedly elevated and exceeded serum levels” to retain the critical value comparison indicating SIADH).
     - Critical temporal or clinical patterns (e.g., “cavitary lesions in the upper lobes” → must be preserved to distinguish tuberculosis from other causes of lung cavitation).
     - Specific test results with known diagnostic significance (e.g., “protein 1+”, “RBC 2/hpf”, “WBC 90/hpf”) → rephrase clinically but retain quantifiable meaning (e.g., “mild proteinuria” is acceptable; “numerous WBC casts” is acceptable, but “some WBC casts” is not).
   - Never omit or de-emphasize findings that are pathognomonic for a condition (e.g., pseudopolyps = ulcerative colitis, not just “mucosal abnormalities”).
   - **Failure triggers**:
     - Example 1: Losing clinical utility by rephrasing “numerous WBC casts” as “numerous white blood cell casts” — technically equivalent but stylistically identical; also failing to restructure the narrative flow. The answer “treat with outpatient ciprofloxacin” is lost because the presence of cast-forming pyelonephritis was not strongly signposted.
     - Example 3: Deleting critical context: “60 pack-year smoking history” and “previous chest X-ray” were reduced to “heavy tobacco exposure” and “findings suggestive of chronic lung alteration,” losing the link to emphysema and obstructive physiology, thereby invalidating the correct answer: “residual volume increased, total lung capacity increased.”

2. **Maximize Anonymization Through Multi-Modal De-identification**:
   - Replace **all personally identifiable information (PII)** and **quasi-identifiers** with generalized, non-specific, and privacy-safe alternatives:
     - Age: Replace specific ages (e.g., “44-year-old”) with “a middle-aged individual,” “a patient in mid-life,” or “an adult in early to mid-adulthood” (but keep exact gestational age if diagnostically central, e.g., “34 weeks”).
     - Gender: Use “a patient” or “an individual” unless gender-specific disease (e.g., gynecologic, prostate) is part of the core presentation.
     - Ethnicity: Remove explicit terms (e.g., “Caucasian”) and replace with neutral, contextually appropriate phrases: “of non-Black descent,” “of diverse ethnic origin,” or “from a region with limited access to routine healthcare,” depending on context.
     - Location: Replace cities, countries, or regional identifiers (e.g., “Stockholm”) with broad descriptors: “a metropolitan area in northern Europe,” “an urban center in a high-income country,” or “a region with a significant refugee population.”
     - Birth weight: Use “normal-sized” or “healthy birth weight” unless low birth weight is clinically relevant (e.g., in neonatal sepsis or NICU assessment).
     - Obstetric history: Replace coded terms (e.g., “P1G0”) with “a woman with a single prior pregnancy,” “a first-time mother,” or “a woman with one prior childbirth,” but **only if accuracy and clinical relevance are preserved**.
   - Avoid combinations of identifiers that create high-risk profiles (e.g., “African female refugee in Stockholm” → rephrase as “a woman who recently relocated from a conflict-affected setting in a northern European nation”).
   - Ensure no traceable patterns emerge from the combination of descriptors.

3. **Disrupt Writing Style Aggressively to Maximize Privacy (Critical for High Privacy Score)**:
   - The anonymized text must be **unrecognizable in style** from the original—this is the most common reason for low privacy scores in prior attempts.
   - Apply **three or more** of the following stylistic transformation techniques:
     - **Restructure sentence order**: Move lab results from bullet points into narrative form and integrate them within the clinical story (e.g., “Serum sodium was found to be markedly low at 122 mEq/L” instead of “Na: 122 mEq/L”).
     - **Use passive voice and nominalization**: Replace active constructions (“the patient experienced pain”) with passive or abstract forms (“a sensation of discomfort was reported”).
     - **Embed clauses using relative or subordinate syntax**: Convert “The patient reports that he has had this before” → “The patient describes a history of recurrent episodes.”
     - **Substitute technical terms with equivalent but less precise synonyms** when this does not degrade clinical meaning:
       - “Prenatal ultrasound” → “during routine antenatal imaging”
       - “Dexamethasone” → “a glucocorticoid agent administered for its anti-inflammatory effects”
       - “Rifampin” → “a first-line anti-tuberculosis medication with broad bactericidal activity”
       - **But never substitute diagnostic anchors** (e.g., “cavitary lesions” must not become “areas of lung abnormality”).
     - **Avoid mirroring sentence length, clause density, or rhythm**. Use varied sentence structures (short, long, compound, complex) in a way that breaks any predictable cadence.
   - **Failure triggers**:
     - Example 2: Repeated use of “this case” and “the patient was initiated” mimics the original structure → low style dissimilarity (0.148).
     - Example 3: Use of “based on clinical context” and “formal assessment” is too generic and echoes the original’s clinical framing, limiting obfuscation.

4. **Output Format and Final Quality Requirements**:
   - Return **only** the `anonymized_text` field.
   - Do **not** include any metadata, headings, markdown (e.g., ```text), comments, explanations, or bullet points.
   - The text must be grammatically correct, fluent, and clinically coherent—read as a natural medical narrative.
   - **Final validation test**: Ask: “Would a trained physician in a similar setting still be able to identify the correct diagnosis or test result from this anonymized text?”
   - **If the answer is no, the anonymized version has failed**.

**Critical Success Strategy (Must Be Applied)**:
1. **Diagnose First**: Before any rephrasing, identify the core clinical mechanism or disease process that enables the correct answer (e.g., for SIADH: inappropriately concentrated urine despite low serum osmolality; for emphysema: history of heavy smoking + imaging + PFT correlation).
2. **Isolate the Diagnostic Kernel**: Extract the **one or two non-negotiable facts** that a clinician must recognize to arrive at the answer. These are the anchors that must survive unmodified in meaning, even if rephrased or restructured.
3. **Obfuscate the Rest**: Apply aggressive stylistic transformations to all non-essential language—this is where the privacy score is achieved.
4. **Validate Both Dimensions**: Always ask:
   - (Clinical) “Can a physician derive the correct answer?”
   - (Privacy) “Would a writing style analyzer detect this as a near-clone of the original?”

**Key Lessons from Failure Examples**:
- Example 1: The original clue was “numerous WBC casts” → anonymization failed because:
  - The narrative structure mirrored the input (bullet to sentence).
  - The phrasing “notably, numerous white blood cell casts” is too literal and fails to disrupt style.
  - Fix: “Microscopic analysis of the urinary sediment revealed an abundance of cellular casts consistent with active pyelonephritis” — preserves meaning, removes structure, and uses passive/complex syntax.
- Example 2: While diagnosis was preserved, style was stagnant due to repeated “the patient was…” and “imaging studies revealed…” → fix: use past participle constructions (“initiated on therapy,” “identified during imaging”), vary verb choice (“demonstrated,” “revealed,” “detected”), and vary sentence length.
- Example 3: Critical context was stripped: “60 pack-year history” and “previous chest X-ray” became “heavy tobacco exposure” and “chronic lung alteration” — too vague. Fix: “a long-term smoker with significant cumulative exposure to tobacco and prior radiologic findings suggestive of irreversible parenchymal damage.”

**Final Command**:
Generate an anonymized text that is **unrecognizable in style**, contains **all essential diagnostic clues**, and allows a trained clinician to arrive at the correct answer with confidence. If you cannot achieve both privacy and diagnostic fidelity, choose the former—the former is the primary goal, but it must not come at the cost of correctness.
```
