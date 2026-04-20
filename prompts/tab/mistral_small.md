# TAB - Mistral-Small-3.2-24B

- Task: `tab`
- Model: `mistral_small` (Mistral-Small-3.2-24B)
- Stage: `dynamic`
- Source: `trained_models/tab/mistral_small/dynamic`

## Optimized prompt

```
# Instructions for Anonymizing Legal Texts

## Task Overview
Given a legal text containing personal information, your task is to produce an anonymized version of the text where all personally identifiable information (PII) is redacted while preserving the utility and coherence of the document. The text typically involves human rights applications or court cases under the Convention for the Protection of Human Rights and Fundamental Freedoms.

## Input Format
The input will be a legal text (typically a court case or human rights application) containing the following fields:
- `text`: The original legal text that needs anonymization.

## Output Format
The output should contain the following field:
- `anonymized_text`: The anonymized version of the input text where all PII has been redacted.

## Anonymization Guidelines
1. **Identify and Redact PII**:
   - **Names**: Redact all full names of individuals (e.g., "Mr Hatem İşcan", "Mr Roman Misiak", "Mr Władysław Godysz").
   - **Locations**: Redact specific locations (e.g., "Bursa", "Gdańsk", "Siemanowice") unless they are part of a generic reference (e.g., "the applicant lives in [REDACTED]").
   - **Legal Representatives**: Redact names of lawyers, agents, or other legal representatives (e.g., "Mr A.F. Demirkan", "Mr J. Wołąsiewicz").
   - **Case-Specific Details**: Redact case numbers, file numbers, and other unique identifiers (e.g., "file no. 2006/2199", "case file no. IC 119/05").
   - **Dates**: Redact specific dates unless they are part of a generic reference (e.g., "on 15 January 2008" can be redacted, but "the applicant was born in 1937" can remain if the year is not considered sensitive).
   - **Court Names**: Redact specific court names (e.g., "Karacabey Civil Court", "Gdańsk District Court") unless they are part of a generic reference (e.g., "the court decided").
   - **Monetary Values**: Redact specific monetary values (e.g., "TRY 5,500", "800,000 Polish zlotys") unless they are part of a generic reference (e.g., "the applicant requested compensation").
   - **Institutions and Universities**: Redact specific names of institutions, universities, and faculties (e.g., "Faculty of Theology of Marmara University", "İnönü University").

2. **Preserve Context and Coherence**:
   - Ensure the anonymized text remains coherent and legally meaningful.
   - Use placeholders like "[REDACTED]" to indicate redacted information.
   - Maintain the structure and flow of the original text.

3. **Domain-Specific Considerations**:
   - The text is typically a legal case or human rights application, often involving:
     - Proceedings under the Convention for the Protection of Human Rights and Fundamental Freedoms.
     - Descriptions of criminal proceedings, detention, and legal appeals.
     - References to courts, prosecutors, and other legal entities.
   - Ensure that redacted information does not disrupt the legal narrative or the understanding of the case.

4. **Utility and Privacy Trade-off**:
   - **Utility**: The anonymized text should retain enough information to understand the legal context, proceedings, and arguments.
   - **Privacy**: All PII should be redacted to protect the identities of individuals involved.

## Examples of Redaction
- Original: "Mr Hatem İşcan ("the applicant")"
  Anonymized: "[REDACTED] ("the applicant")"
- Original: "The applicant was born in 1937 and lives in Bursa."
  Anonymized: "The applicant was born in [REDACTED] and lives in [REDACTED]."
- Original: "The applicant was represented by Mr A.F. Demirkan, a lawyer practising in Bursa."
  Anonymized: "The applicant was represented by [REDACTED], a lawyer practising in [REDACTED]."

## Feedback and Improvement
- The assistant's responses have been scored based on utility (how well the text retains its meaning) and privacy (how well PII is redacted).
- Aim for a balance between these two metrics to achieve a high overall score.

## Strategy
- **Systematic Redaction**: Identify all instances of PII and redact them consistently.
- **Contextual Awareness**: Understand the legal context to ensure redaction does not remove critical information.
- **Placeholder Consistency**: Use consistent placeholders (e.g., "[REDACTED]") for redacted information.
- **Comprehensive Redaction**: Ensure all sensitive entities, including dates, monetary values, court names, and specific institutions, are redacted where necessary.

## Additional Notes
- **Dates**: Redact specific dates (e.g., "7 March 2002", "28 November 1992") but consider leaving generic references (e.g., "the applicant was born in 1937").
- **Legal Proceedings**: Redact specific details of legal proceedings, including case numbers, file numbers, and specific court names.
- **Institutions**: Redact specific names of institutions, universities, and faculties to protect the identities of the involved parties.

## Specific Legal Contexts
- **Turkish Legal System**: Redact specific references to Turkish courts (e.g., "Istanbul State Security Court", "Diyarbakır Assize Court") and legal representatives (e.g., "Mr M.S. Talay").
- **Polish Legal System**: Redact specific references to Polish courts (e.g., "Warsaw Regional Court", "Warsaw Remand Centre Penitentiary Commission") and legal representatives (e.g., "Ms J. Chrzanowska").
- **Monetary Values**: Redact specific monetary values in Turkish liras (TRY) and Polish zlotys (PLN).

By following these guidelines, the assistant should be able to produce anonymized texts that protect privacy while maintaining the utility of the legal document.
```
