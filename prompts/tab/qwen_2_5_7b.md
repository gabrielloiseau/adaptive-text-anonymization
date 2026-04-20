# TAB - Qwen-2.5-7B

- Task: `tab`
- Model: `qwen_2_5_7b` (Qwen-2.5-7B)
- Stage: `dynamic`
- Source: `trained_models/tab/qwen_2_5_7b/dynamic`

## Optimized prompt

```
Instructions:

Given the field `text`, produce the field `anonymized_text` by replacing personal identifiers, place names, dates, and institutional names with generic placeholders while preserving the structure and context of the original text. Ensure that all sensitive or identifying information is removed but key contextual elements are maintained. Follow these detailed steps:

1. Replace all personal identifiers such as names and initials with `{first_name}`, `{last_name}`, `{initials}`, etc.
2. Replace all place names (cities, regions, countries, organizations, etc.) with `{city}`, `{province}`, `{country}`, `{institution}`, etc.
3. Replace all dates with `{date}` or `{year}`. Ensure that dates are consistently replaced and maintain proper formatting.
4. Preserve any unique identifiers (like case numbers, file references, etc.) as they might be necessary for context.
5. Utilize a consistent strategy to replace placeholders so that different inputs yield similar anonymized formats.
6. Maintain the logical flow and structure of the original text.
7. Handle special cases like censoring stamps, letter seals, and court proceedings details appropriately.
8. Ensure that placeholders for protocol numbers, article numbers, and case numbers remain intact as they provide necessary context.

Niche and Domain-Specific Information:
- Names can include various forms like given names, surnames, initials (e.g., Mr. A.F. Demirkan).
- Place names could be cities (e.g., Katowice), regions (e.g., Sztum), institutions (e.g., Ministry of Foreign Affairs), courts (e.g., District Court), and organizations (e.g., Penitentiary Association “Patronat”).
- Dates should be generalized consistently; for example, replace any specific date with a placeholder like `{date}` or `{year}`.
- Unique identifiers such as case numbers (e.g., 10450/08) and file references (e.g., file no. 2006/2199) must be preserved.
- Special details like censorship stamps and court ruling information should be maintained accurately in the anonymized output.
- Legal terms and phrases used in judicial contexts like "prosecutor," "court," "district court," "regional court," "European Court of Human Rights," should be anonymized consistently.

Examples:
Input:
```
PROCEDURE

The case originated in an application (no. 43837/06) against the Republic of Poland lodged with the Court under Article 34 of the Convention for the Protection of Human Rights and Fundamental Freedoms ("the Convention") by a Polish national, Mr Roman Misiak ("the applicant"), on 17 October 2006.

The Polish Government ("the Government") were represented by their Agent, Mr J. Wołąsiewicz of the Ministry of Foreign Affairs.

On 5 March 2007 the President of the Fourth Section decided to communicate the complaint concerning the monitoring of the applicant’s correspondence to the Government. Under the provisions of Article 29 § 3 of the Convention, it was decided to examine the merits of the application at the same time as its admissibility.

THE FACTS

I. THE CIRCUMSTANCES OF THE CASE

The applicant was born in 1958 and lives in Gdańsk.

A. Criminal proceedings against the applicant

On 9 August 2006 the applicant was arrested on suspicion of fraud and placed in pre-trial detention. The grounds for this decision are unknown, since the applicant has not produced a copy of it.

On 3 November 2006 the Gdańsk District Court (Sąd Rejonowy) extended the applicant’s detention until 9 February 2007. It referred to the reasonable suspicion that the applicant had committed the offence with which he had been charged. It relied on the possibility of a severe sentence of imprisonment being imposed on the applicant and the need to secure the proper conduct of the proceedings. The court further noted that there was a risk that the applicant might go into hiding, given that earlier he could not be found at his place of permanent residence.

The applicant submitted that he unsuccessfully appealed against decisions extending his detention.

The applicant maintained that during his arrest he was treated in a degrading manner by police officers and that he was subjected to threats. On 19 February 2007 the Gdańsk District Prosecutor instituted an investigation into the applicant’s complaints against the police officers. The investigation is still continuing.

B. Censorship of the applicant’s correspondence

The applicant submitted that during his detention his correspondence was censored by the authorities. He produced five envelopes. All the envelopes bear a stamp that reads: “Censored, date ..., Prosecutor” (Ocenzurowano, dnia ... Prokurator). Those envelopes contained letters from:

the Penitentiary Association “Patronat” (Stowarzyszenie Penitencjarne “Patronat”), a non-governmental organisation, acting, inter alia, on behalf of prisoners and former prisoners, sent on 30 August 2006;

the Supreme Court, sent on 26 September 2006;

the European Committee for the Prevention of Torture and Inhuman and Degrading Treatment, sent on 27 September 2006;

the Ministry of Justice; sent on 27 September 2006;

the Ombudsman, sent on 28 September 2006.

The applicant produced one envelope that indicates as the addressee of the letter the Governor of Sztum Prison and bears a stamp that reads: “Censored, date ..., Prosecutor” (Ocenzurowano, dnia ... Prokurator). A hand-written note indicates case file no. IC 119/05.

One envelope bears traces of having been opened - its sides were cut open and resealed using self-adhesive tape.

The applicant submitted that a letter addressed to him by the Court had been opened and read by the authorities. In a note sent to the applicant from Sztum Prison (Zakład Karny) on 21 December 2006, he was informed that on 29 November 2006 a letter from the European Court of Human Rights to the applicant had been delivered by the District Prosecutor’s Office. The note further states that the letter had clearly been damaged.
```

Output:
```
PROCEDURE

The case originated in an application (no. {ANONYMIZED}/06) against the Republic of {ANONYMIZED} lodged with the Court under Article {ANONYMIZED} of the Convention for the Protection of Human Rights and Fundamental Freedoms ("the Convention") by a Polish national, Mr {first_name} {last_name} ("the applicant"), on {date}.

The Polish Government ("the Government") were represented by their Agent, Mr {last_name} {ANONYMIZED} of the Ministry of Foreign Affairs.

On {date} the President of the Fourth Section decided to communicate the complaint concerning the monitoring of the applicant’s correspondence to the Government. Under the provisions of Article {ANONYMIZED} §{section} of the Convention, it was decided to examine the merits of the application at the same time as its admissibility.

THE FACTS

I. THE CIRCUMSTANCES OF THE CASE

The applicant was born in {year} and lives in {city}.

A. Criminal proceedings against the applicant

On {date} the applicant was arrested on suspicion of {crime} and placed in pre-trial detention. The grounds for this decision are unknown, since the applicant has not produced a copy of it.

On {date} the {city} District Court (Sąd Rejonowy) extended the applicant’s detention until {date}. It referred to the reasonable suspicion that the applicant had committed the offence with which he had been charged. It relied on the possibility of a severe sentence of imprisonment being imposed on the applicant and the need to secure the proper conduct of the proceedings. The court further noted that there was a risk that the applicant might go into hiding, given that earlier he could not be found at his place of permanent residence.

The applicant submitted that he unsuccessfully appealed against decisions extending his detention.

The applicant maintained that during his arrest he was treated in a degrading manner by police officers and that he was subjected to threats. On {date} the {city} District Prosecutor instituted an investigation into the applicant’s complaints against the police officers. The investigation is still continuing.

B. Censorship of the applicant’s correspondence

The applicant submitted that during his detention his correspondence was censored by the authorities. He produced {number} envelopes. All the envelopes bear a stamp that reads: “Censored, date ..., Prosecutor” (Ocenzurowano, dnia ... Prokurator). Those envelopes contained letters from:

a non-governmental organisation, acting, inter alia, on behalf of prisoners and former prisoners, sent on {date};

a governmental institution, sent on {date};

the European Committee for the Prevention of Torture and Inhuman and Degrading Treatment, sent on {date};

a governmental institution, sent on {date};

a governmental institution, sent on {date}.

The applicant produced one envelope that indicates as the addressee of the letter the Governor of prison and bears a stamp that reads: “Censored, date ..., Prosecutor” (Ocenzurowano, dnia ... Prokurator). A hand-written note indicates case file no. {protocol_number}.

One envelope bears traces of having been opened - its sides were cut open and resealed using self-adhesive tape.

The applicant submitted that a letter addressed to him by the Court had been opened and read by the authorities. In a note sent to the applicant from prison on {date}, he was informed that on {date} a letter from the European Court of Human Rights to the applicant had been delivered by the District Prosecutor’s Office. The note further states that the letter had clearly been damaged.
```

Feedback:
- Ensure consistency in the replacement of placeholders.
- Maintain integrity of the context and flow of the text.
- Preserve special procedural details such as detention dates and court rulings.
- Handle special cases like censoring stamps and court proceedings details appropriately.
- Ensure that placeholders for protocol numbers, article numbers, and case numbers remain intact as they provide necessary context.
```
