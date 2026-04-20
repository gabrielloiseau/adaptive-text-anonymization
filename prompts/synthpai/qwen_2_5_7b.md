# SynthPAI - Qwen-2.5-7B

- Task: `synthpai`
- Model: `qwen_2_5_7b` (Qwen-2.5-7B)
- Stage: `dynamic`
- Source: `trained_models/synthpai/qwen_2_5_7b/dynamic`

## Optimized prompt

```
Given the fields `text`, produce the fields `anonymized_text` while ensuring the following conditions are met:
- Preserve the overall structure, meaning, and sentiment of the original text.
- Remove any identifiable attributes or elements such as names, addresses, dates, and unique personal details that might allow an attacker to infer the private information of individuals mentioned in the text.
- Maintain the utility of the text as much as possible, meaning that the anonymized text should still be coherent and retain its original message.
- Avoid substituting common words with their synonyms that might change the sentiment or meaning of the text.

For example, if the text contains a person's name, replace it with a non-specific term like "person" or "individual". If it mentions a date or location relevant to the context, ensure the anonymized version still conveys the same context and sentiment.

Detailed instructions and sample outputs:
1. Input:
   ```
   ## Inputs
   ### text
   Architectural beauty here can mask some daily hassles – like when centuries-old streets aren't really made for modern traffic; charming until you're late for an appointment!
   ```
   - **Generated Output**:
     ```
     ### anonymized_text
     Architectural beauty here can mask some daily hassles – like when old streets aren't really made for cars; charming until you're late for an appointment!
     ```
   - **Feedback**:
     ```
     - Utility Score (ROUGE-1): 0.926
     The attacker cannot identify the private attribute ({gold.target_attribute}).
     Prevent attribute inference from the attacker while preserving the utility of the text.
     ```

2. Input:
   ```
   ## Inputs
   ### text
   Definitely strange our little escapes are now plugged-in zones; guess everything's bowing to tech? Even benches where we'd swap stories are charging stations!
   ```
   - **Generated Output**:
     ```
     ### anonymized_text
     Definitely strange our little escapes are now plugged-in zones; guess everything's bowing to tech? Even benches where we'd swap stories are charging stations!
     ```
   - **Feedback**:
     ```
     - Utility Score (ROUGE-1): 1.000
     The attacker can identify the private attribute ({gold.target_attribute}).
     The attacker reasoning is the following: {attacker_B.reasoning}
     Prevent attribute inference from the attacker while preserving the utility of the text.
     ```

3. Input:
   ```
   ## Inputs
   ### text
   systemic probs are real 😩 even so got find your own way ya kno? let little rituals n chill spots keep u sane amidst all da chaos 🌆🛀
   ```
   - **Generated Output**:
     ```
     ### anonymized_text
     systemic probs are real 😩 even so got find your own way ya kno? let little rituals n chill spots keep u sane amidst all da chaos 🌆🛀
     ```
   - **Feedback**:
     ```
     - Utility Score (ROUGE-1): 1.000
     The attacker can identify the private attribute ({gold.target_attribute}).
     The attacker reasoning is the following: {attacker_B.reasoning}
     Prevent attribute inference from the attacker while preserving the utility of the text.
     ```

New Instruction:
Given the fields `text`, produce the fields `anonymized_text` while:
- Preserving the coherent meaning and sentiment of the original text.
- Removing any identifiable names, addresses, dates, and other specific personal details.
- Avoiding the substitution of common words with synonyms that could alter the meaning.
- Maintaining the context and utility of the original message.
```
