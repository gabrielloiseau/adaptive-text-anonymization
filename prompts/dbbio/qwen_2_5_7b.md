# DB-Bio - Qwen-2.5-7B

- Task: `dbbio`
- Model: `qwen_2_5_7b` (Qwen-2.5-7B)
- Stage: `dynamic`
- Source: `trained_models/dbbio/qwen_2_5_7b/dynamic`

## Optimized prompt

```
Given the field `text`, produce the field `anonymized_text` while ensuring the original individual cannot be identified. The anonymization process should preserve key details such as profession, achievements, and significant events in the person's career while replacing all personal identifiers with generic placeholders. Ensure that the anonymized text still provides utility by retaining relevant information necessary for understanding the context.

# Detailed Task Description:
1. **Identify Personal Identifiers**: Recognize names (including nicknames, titles, and honorifics), dates, places, specific organizations or clubs, and significant figures mentioned in the `text`.
2. **Maintain Key Details**: Preserve the occupation, main accomplishments, significant events, and other critical elements of the person's career while anonymizing associated identifiers.
3. **Use Generic Placeholders**: Replace all specific names, places, organizations, and figures with generic terms like `[Name]`, `[Date]`, `[Place]`, `[Organization]`, `[Manager]`, etc. For example:
   - Replace "John Smith" with `[Person Name]`
   - Replace "New York City" with `[City]`
   - Replace "IBM" with `[Company]`
4. **Preserve Contextual Information**: Maintain the overall context and flow of the text to ensure it remains useful and retains its intent.

# Specific Guidelines and Examples:
## Inputs
### text
Lena Horne (born April 30, 1917) was an American actress, singer, and civil rights activist. She was known for her powerful contralto singing voice and was one of the first African-American performers to achieve stardom without playing the stereotypical black mammy archetype. During World War II, she served with the Women's Auxiliary Army Corps (WAAC). In 1950, Lena Horne starred in the Broadway musical "Pin-Up Girl." She was the first black woman to sign a long-term contract with a major Hollywood studio. In 1951, she appeared in the film "Stormy Weather" alongside Billie Holiday, Dorothy Dandridge, and Joe Louis. Lena Horne continued to fight for racial equality throughout her career and in 1994, she was awarded a Kennedy Center Honor.

## Generated Outputs
### anonymized_text
[Person Name] (born [Date of Birth]) was an American actress, singer, and civil rights activist. She was known for her powerful contralto singing voice and was one of the first African-American performers to achieve stardom without playing the stereotypical black mammy archetype. During World War II, she served with the Women's Auxiliary Army Corps. In 1950, [Person Name] starred in the Broadway musical "Pin-Up Girl." She was the first black woman to sign a long-term contract with a major Hollywood studio. In 1951, she appeared in the film "Stormy Weather" alongside [Actor 1], [Actor 2], and [Boxer]. [Person Name] continued to fight for racial equality throughout her career and in 1994, she was awarded a Kennedy Center Honor.

## Feedback
- Utility: The occupation (Actress/Singer/Civil Rights Activist) can be inferred from the anonymized text.
- Privacy: The person (Lena Horne) cannot be identified from the anonymized text.
- Preserve the occupation while protecting the person identity.

## Another Example
### text
James Buchanan Eads (October 23, 1820 – September 8, 1902) was a prolific American engineer, ironmaster, and civil engineer. He is known for designing the Mississippi River Bridge in St. Louis, which opened in 1874 and was considered the "Eighth Wonder of the World." Eads built the Eads Bridge, a steel bridge that is the first railroad and highway bridge to cross the Mississippi River, opening in 1874. His design featured iron caissons for the construction of the piers, which is considered one of the earliest examples of hydraulic construction in modern architecture. He was inducted into the National Inventors Hall of Fame in 2004.

## Generated Outputs
### anonymized_text
[Engineer Name] (born [Date of Birth] – [Date of Death]) was an American engineer, ironmaster, and civil engineer. He is known for designing the [Bridge Name] in [City], which opened in [Year] and was considered the "Eighth Wonder of the World." [Engineer Name] built the [Bridge Name], the first railroad and highway bridge to cross the [River Name], opening in [Year]. His design featured iron caissons for the construction of the piers, which is considered one of the earliest examples of hydraulic construction in modern architecture. He was inducted into the National Inventors Hall of Fame in [Year].

## Feedback
- Utility: The occupation (Engineer/Ironmaster/Civil Engineer) can be inferred from the anonymized text.
- Privacy: The person (James Buchanan Eads) cannot be identified from the anonymized text.
- Preserve the occupation while protecting the person identity.

## Domain-Specific Insights:
- Specific titles: Such as "Chef," "Chef/Owner," "FIDE Master," "Chess Grandmaster," "Civil Engineer," "Civil Rights Activist."
- Organizations: Specific restaurant names, chess tournaments, clubs, engineering projects, political affiliations.
- Places: Major cities, countries, specific events, and historical sites.
- Dates: Major life events, career milestones, and significant dates in political or professional contexts.
- Significant Individuals: Key figures, historical figures, celebrities, colleagues in the industry, political figures.

# Instruction:
Given the field `text`, produce the field `anonymized_text` while ensuring the original individual cannot be identified. The anonymization process should preserve key details such as profession, achievements, and significant events in the person's career while replacing all personal identifiers with generic placeholders. Ensure that the anonymized text still provides utility by retaining relevant information necessary for understanding the context. Follow the detailed task description and specific guidelines provided above.

# Feedback and Model Reasoning:
In all cases, the key is to maintain the contextual integrity while removing specific personal identifiers. Utilize the guidelines to ensure that the anonymized text remains informative yet privacy-preserving.
```
