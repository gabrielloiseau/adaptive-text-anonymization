# PUPA - Mistral-Small-3.2-24B

- Task: `pupa`
- Model: `mistral_small` (Mistral-Small-3.2-24B)
- Stage: `dynamic`
- Source: `trained_models/pupa/mistral_small/dynamic`

## Optimized prompt

```
Given the field `text`, produce the field `anonymized_text` by anonymizing sensitive or personally identifiable information (PII) while preserving the quality, usefulness, and completeness of the response. Follow these guidelines:

### 1. **Anonymization Rules**
- **Names**: Replace with `[NAME]` or generic placeholders (e.g., "[USER]" for users, "[AUTHOR]" for authors).
- **URLs/Paths**: Replace with generic descriptions (e.g., "https://gitlab.com/***/ext/***/***") or omit if non-critical. For platforms like Etsy or Stan Store, retain the platform name but anonymize specific handles (e.g., "Etsy shop: [SHOP_NAME]").
- **Dates/Places**: Anonymize only if part of PII (e.g., "[DATE]" for personal dates, but retain general locations like "Montana" or "Macau").
- **Medical/Financial Data**: Replace with placeholders (e.g., "[VACCINATION_RECORDS]").

### 2. **Quality Preservation**
- **Technical Tasks (e.g., Docker, GitLab)**:
  - Assume a Node.js app unless specified otherwise.
  - Include all steps, commands, and context, even if details are anonymized.
  - Example: "Clone the repository from [GIT_REPO_URL] and run `npm install`."
- **Educational Queries**:
  - Provide detailed, informative responses (e.g., "The quality of education in Macau is...").
  - For exercises, give correct answers or guidance (e.g., "The blank should be filled with '[VERB]'.").
- **Marketing/Business Queries**:
  - Align tone with user requests (e.g., minimalist tone for Etsy strategies).
  - Include actionable steps (e.g., "Use hashtags like #HandmadeWithLove for Instagram").

### 3. **Privacy Analysis**
- Track PII units (e.g., names, URLs, dates) and ensure 0% leakage.
- Example: "Total PII units: 3 (names, email, vaccination records). Leakage rate: 0.0%."

### 4. **Domain-Specific Notes**
- **Breaking News (Fictional)**:
  - Use a structured format (Key Points, Expert Analysis, Call to Action).
  - Include realistic elements (e.g., UN meetings, economic impact).
- **Emails/Professional Communication**:
  - Prioritize clarity, conciseness, and professionalism.
  - Example: "Hi [NAME], I’ve attached the [DOCUMENT_TYPE] for the [PROGRAM_NAME] application."

### 5. **Generalizable Strategies**
- **Tone Alignment**: Mirror the user’s requested tone (e.g., minimalist, formal, urgent).
- **Depth vs. Breadth**: For technical queries, favor depth (e.g., PPC strategies for Etsy). For general queries, ensure breadth (e.g., multi-platform marketing).
- **Placeholder Consistency**: Use consistent placeholders (e.g., "[NAME]" for all names, "[DATE]" for all dates).

### 6. **Examples to Follow**
- **Good Example (Technical)**:
  - Input: "Set up Docker for my Node.js app."
  - Output: "Run `docker build -t [APP_NAME] .` and `docker run -p 3000:3000 [APP_NAME]`."
- **Bad Example (Technical)**:
  - Input: "Anonymize my GitLab URL."
  - Output: "The URL is [URL]. No further instructions."
- **Good Example (Educational)**:
  - Input: "Fill in the blank: 'The [VERB] quickly.'"
  - Output: "The correct answer is '[VERB]'."
- **Bad Example (Educational)**:
  - Input: "Fill in the blank: 'The [VERB] quickly.'"
  - Output: "The blank should be filled with a verb."

Ensure the anonymized response is as helpful as the original while minimizing PII leakage.
```
