# DB-Bio - Gemma-3-27B-it

- Task: `dbbio`
- Model: `gemma_3_27b` (Gemma-3-27B-it)
- Stage: `dynamic`
- Source: `trained_models/dbbio/gemma_3_27b/dynamic`

## Optimized prompt

```
Given the field `text` containing a biography of a notable person, produce the field `anonymized_text` containing a paraphrased version of the biography that protects the individual's identity while preserving the key facts about their career and accomplishments.

**Detailed Instructions:**

1.  **Goal:** The primary goal is to anonymize the text to prevent identification of the person while retaining the essential information about their achievements and life story. The anonymized text should *not* allow someone to readily identify the original person using external knowledge.

2.  **Anonymization Strategy:**
    *   Replace proper nouns (names, specific locations, organization names where they uniquely identify the person) with generic placeholders. For instance:
        *   "David Bouley" becomes "a chef"
        *   "TriBeCa, New York City" becomes "a city, New York" or "a neighborhood"
        *   "Jean Georges Vong" becomes "a renowned restaurant"
        *   "Top Chef" becomes "a reality television cooking competition show"
    *   Avoid specifics that are highly unique to the individual.
    *   Retain the person’s occupation and broad career path.
    *   Preserve dates (birthdates, years of events) as these contribute to the narrative without immediately identifying the individual.
    *   Maintain the overall story arc and sequence of events.
    *   Use gender-neutral pronouns (they/them/their) where possible to avoid inference.
    *   **Generalizable Strategy:** The assistant has demonstrated success by replacing names, location names, and specific organizations with generic equivalents. Continue to use this approach consistently.

3.  **Privacy Considerations:** This task is designed to test privacy. Prioritize preventing re-identification.

4. **Reasoning about Re-identification Risks**: After anonymizing the text, consider the risk of re-identification. A successful anonymization will obscure enough details that the combination of facts doesn't pinpoint a single individual. The biography often creates a unique profile based on the combination of:
    *   Early life details (birthdate, birthplace)
    *   Educational background
    *   Career progression (specific roles, awards, unique events participated in)
    *   Post-career activities
    *   Ethnicity (if mentioned)
    *   Activism or public statements

5. **Domain-Specific Knowledge:**  Pay close attention to the following domains and common identifying factors. Note that success heavily relies on avoiding these:
    *   **Chefs:** Profiles of chefs often include details regarding restaurant names, culinary style, awards (Michelin stars, James Beard awards), and training (specifically *who* they trained under). Avoid specifics related to the restaurant's location/unique dishes.
    *   **Astronauts:** Profiles often contain mission details (Apollo, Skylab, Space Shuttle), command roles, position in the mission order (e.g., “fourth person to walk on the moon”), and post-NASA activities (e.g., writing, painting, public speaking). Avoid specifics that reflect the order in which they walked on the moon or the missions they flew.
    *   **Chess Players:** Profiles often include details such as nationality, birth city, national championships won, specific opponents (e.g., Garry Kasparov), significant tournaments (like the USSR Championship), coaching roles (e.g,. coaching world champions), online pseudonyms, and references in chess literature. Avoid specifics around unusual achievements (e.g., first Grandmaster from a specific country), specific coaching details, or unique online pseudonyms.
    *   **Basketball Players:** Profiles often contain team names, league achievements, scoring averages, and specific game-winning plays. Avoid specifics such as regional team naming and the high ranking in single-season points.
    *   **Media Personalities:** Profiles often contain show titles, co-hosts, and details about controversial events (particularly convictions). When dealing with controversial events, carefully anonymize details to avoid exact matching.

6.  **Expected Output:**  `anonymized_text` should be a coherent and grammatically correct paragraph that conveys the essence of the original biography without revealing the person's identity.

7. **Advanced Anonymization Techniques:**
    * **Combine/Generalize Specifics**: If a person played for several teams in a specific city, combine them into one statement about playing for teams within that region.
    * **Re-order Events**: When possible, subtly re-order the sequence of events to obscure the individual’s unique timeline.
    * **Omit Unique Achievements**:  If a specific achievement is extraordinarily rare or unique to the person, consider omitting it entirely.
```
