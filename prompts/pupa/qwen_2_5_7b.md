# PUPA - Qwen-2.5-7B

- Task: `pupa`
- Model: `qwen_2_5_7b` (Qwen-2.5-7B)
- Stage: `dynamic`
- Source: `trained_models/pupa/qwen_2_5_7b/dynamic`

## Optimized prompt

```
Given the fields `text`, produce the fields `anonymized_text` while ensuring the following:

- Eliminate any personally identifiable information (PII) such as names, dates, direct mentions of individuals, or organization-specific details.
- Maintain the general meaning and structure of the original text.
- Replace specific details that are not needed with vague terms or placeholders.
- Ensure that the anonymized text does not introduce logical inconsistencies compared to the original text.
- Adjust numerical values (like costs, quantities, or dates) if necessary to maintain context without revealing exact figures.
- Keep business-sensitive information confidential while preserving the overall intent and purpose of the text.
- Provide a detailed and actionable response when requested for strategies, plans, or proposals.
- Ensure that the response maintains the clarity and coherence of the original text with no unnecessary details.

Detailed Steps:
1. Identify and remove any PII such as names, addresses, phone numbers, email addresses, and specific organization names.
2. Replace sensitive information with general placeholders or vague terms:
   - Names: Replace with "[Name]".
   - Organizations: Replace with "[Company Name]".
   - Locations: Replace with "[City]", "[Country]". If specific locations are needed, use "[Neighborhood]", "[Region]".
   - Dates: Replace with "a few weeks/months/years ago".
   - Numbers: Replace with "a few", "several", "highly profitable", "modest", etc.
3. Ensure the context and intent are preserved without loss of critical details.
4. If asked for a strategic plan, provide specific actionable steps, examples, and justifications.
5. Maintain a professional tone and ensure the generated text flows naturally.
6. Avoid introducing any inconsistencies that could affect the overall meaning and context of the text.
7. If numerical values are mentioned and need to be adjusted, do so in a way that preserves the intended context without revealing exact figures.

Example 1:
## Inputs
### text
Ways to enhance Uber's Pay per Click (PPC) campaigns and achieve the objectives of increasing brand awareness, increasing followers on social media, increasing user acquisition, and increasing website traffic.

## Generated Outputs
### anonymized_text
Strategies to improve PPC campaigns for a platform similar to Uber and achieve goals like boosting brand recognition, growing followers on social media, attracting new users, and increasing website visits.

## Feedback
The response maintains the same quality as the target response. Ensure the response is detailed and actionable by including specific tactics such as keyword refinement, ad copy optimization, retargeting, social media advertising, influencer collaborations, and continuous campaign analysis. Reduce the leakage of PII information while preserving the quality of the response.

Privacy Analysis:
- Total PII units to protect: 1
- Remaining PII units: 
- Leakage rate: 0.0%
```
