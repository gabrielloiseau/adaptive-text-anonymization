# MedQA - Mistral-Small-3.2-24B

- Task: `medqa`
- Model: `mistral_small` (Mistral-Small-3.2-24B)
- Stage: `dynamic`
- Source: `trained_models/medqa/mistral_small/dynamic`

## Optimized prompt

```
Given a medical case description in the field `text`, produce an anonymized version in the field `anonymized_text` that meets the following criteria:

1. **Clinical Content Preservation**:
   - Maintain all key medical details that are necessary to derive the correct clinical answer (e.g., symptoms, test results, treatments, and diagnostic reasoning).
   - Ensure the anonymized text still supports the same medical conclusion as the original.

2. **Anonymization Strategy**:
   - Replace specific patient identifiers (e.g., age, gender, names) with generic placeholders (e.g., `[AGE]`, `[GENDER]`, `[PERSON]`).
   - Preserve numerical values (e.g., blood pressure, laceration size) unless they are directly tied to patient identity.
   - Avoid altering medical terminology, diagnostic criteria, or treatment options unless they are patient-specific.

3. **Writing Style Obfuscation**:
   - Modify the sentence structure or phrasing slightly to reduce similarity to the original text while keeping the meaning intact.
   - Use neutral language (e.g., "person" instead of gendered terms) where appropriate to further anonymize.

4. **Privacy Score Optimization**:
   - Aim for a higher "Privacy Score" (measuring writing style dissimilarity) by ensuring the anonymized text does not closely resemble the original in phrasing or structure.
   - Avoid verbatim copying of sentences unless they are essential for clinical context.

5. **Domain-Specific Nuances**:
   - For questions about diagnoses or treatments, ensure the anonymized text still allows the correct answer to be inferred (e.g., "Crohn disease" or "Lisinopril" in the examples).
   - For procedural or anatomical details (e.g., "right buttock"), retain specificity unless it could identify the patient.

Example of a well-executed anonymization:
- Original: "A 45-year-old man was shown to have a blood pressure of 142/90 mm Hg..."
- Anonymized: "A [AGE]-year-old person was shown to have a blood pressure of [BP] mm Hg..."

Example of a poorly executed anonymization:
- Original: "A 27-year-old female has a history of periodic bloody diarrhea..."
- Poor Anonymized: "A [AGE]-year-old [GENDER] has a history of periodic bloody diarrhea..." (if it compromises the ability to answer the question correctly).

Prioritize clinical accuracy over anonymization when the two conflict. The goal is to make the text unidentifiable to the patient while preserving its medical utility.
```
