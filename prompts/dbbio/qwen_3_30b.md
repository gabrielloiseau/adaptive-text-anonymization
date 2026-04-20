# DB-Bio - Qwen3-30B-A3B

- Task: `dbbio`
- Model: `qwen_3_30b` (Qwen3-30B-A3B)
- Stage: `dynamic`
- Source: `trained_models/dbbio/qwen_3_30b/dynamic`

## Optimized prompt

```
Given a textual input containing biographical or narrative information about a person, produce an anonymized version of the text by systematically replacing specific, personally identifiable information with standardized placeholder tokens while preserving the semantic structure, logical flow, and most importantly, the core occupation or role of the individual.

The anonymization must ensure that the individual cannot be re-identified through a combination of factual details (e.g., name, birth date, place of birth, specific locations, exact years, unique events such as rare sports achievements, or known affiliations with specific organizations, clubs, or teams). Use the following principles:

1. **Replace Personally Identifiable Information**:
   - Full name → [REDACTED PERSON]
   - Birth date → [DATE]
   - Place of birth (city, town, region, province, country) → [REDACTED PLACE] or [REDACTED LOCATION]
   - Exact dates of events (e.g., "in 1963", "April 1972") → [YEAR], [MONTH] [YEAR], or [YEAR] depending on context
   - Specific club names → [REDACTED CLUB NAME] (for sports teams, restaurants, hotels, organizations)
   - Specific hotel/restaurant names → [REDACTED HOTEL NAME] or [REDACTED ESTABLISHMENT NAME]
   - Specific geographic regions (e.g., "Gwent", "Misiones", "Buenos Aires Province") → [REDACTED REGION] or [REDACTED PROVINCE]
   - Nicknames → [NICKNAME]
   - Nationality → [REDACTED NATIONALITY]
   - Ethnicity/ancestry → [ETHNICITY]
   - Currency → [CURRENCY]
   - Number of goals/matches → [NUMBER]
   - Dates with precision → [YEAR], [MONTH] [YEAR], or [MONTH] [YEAR] (avoid revealing time sequences that might allow inference)

2. **Preserve Occupation and Role**:
   - The occupation (e.g., "chef", "football player", "tennis player") must remain clear and inferable from the text. Do not anonymize job titles or roles.
   - Retain key achievements related to the occupation (e.g., winning a gold medal, gaining a Michelin star, being ranked top scorer), but replace the names of awarding bodies, tournaments, and specific locations (e.g., "2004 Summer Paralympics in Athens, Greece" → "the [YEAR] Paralympics in [COUNTRY]").

3. **Avoid Over-Anonymization**:
   - Do not replace all instances of generic words (e.g., "Saturday", "grandmother", "family", "child") with placeholders.
   - Avoid introducing artificial identity markers like "Person A" or "Person B" unless absolutely necessary and only for co-participants in events (e.g., doubles teams), and even then, use [REDACTED PERSON] consistently. Except in rare cases where the structure requires distinguishing between multiple people in a team, use [REDACTED PERSON] for all individuals.

4. **Critical Privacy Principle – Prevent Re-Identification via Factual Inference**:
   - Ensure that the anonymized text does not allow identification through logical inference using publicly known facts (e.g., Paralympic results, unique sport histories, club records, or known timelines).
   - Example: Do not imply a unique sequence of events that only one person could have experienced (e.g., "won a gold medal at the 2004 Paralympics with partner X" when only two players are known to have achieved this – substitute with "won a gold medal in the doubles event at a major international competition" unless specific details can be safely generalized).

5. **Structural and Linguistic Fidelity**:
   - Maintain the original sentence structure, grammar, and narrative flow.
   - Avoid introducing new terms or incorrect phrasing (e.g., "the top club [CLUB]" is acceptable; "a prominent team member there was the World Cup [YEAR] winning player" → keep as-is but anonymize the player's name).

6. **Use of Model Reasoning to Verify Privacy**:
   - Before outputting, review whether the anonymized text can still logically lead to the identification of the individual using external knowledge. If yes, revise the placeholders to ensure complete unlinkability (e.g., generalize "the 2004 Summer Paralympics in Athens, Greece" to "the 2004 Paralympics").

Final Output Format:
- Output only the anonymized text in a field named `anonymized_text`.
- No additional explanation, commentary, or metadata.
- Maintain all original punctuation and capitalization as much as possible.

Apply this methodology consistently across all inputs.
```
