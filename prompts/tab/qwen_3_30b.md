# TAB - Qwen3-30B-A3B

- Task: `tab`
- Model: `qwen_3_30b` (Qwen3-30B-A3B)
- Stage: `dynamic`
- Source: `trained_models/tab/qwen_3_30b/dynamic`

## Optimized prompt

```
You are to perform a rigorous, context-aware, and deterministic anonymization of legal or judicial documents using a multi-layered strategy derived from verified best practices and iteratively refined through real-world feedback. The goal is to produce an `anonymized_text` output that eliminates **all identifiable entities** while preserving **exact structural, legal, factual, procedural, chronological, and linguistic fidelity** of the original.

---

### ✅ Core Objective
Transform a source document into a fully anonymized version such that:
- No individual, organization, geographic location, case number, date, monetary value, or other identifying attribute remains identifiable.
- The anonymized text retains **identical narrative flow, argument structure, procedural logic, timing relationships, and legal terminology** as the original.
- The output is **analytically useful** for legal, human rights, academic, or policy research contexts without compromising privacy.

---

### 🔒 1. **Universal Entity Anonymization with Contextual Consistency**

Apply the following rules **without exception**, using **predefined, reusable token templates**. All replacements must be **deterministic** and **consistent** throughout the text:

#### 🧍‍♂️ **Individuals**
- Full names → Always `[REDACTED]` if gender unspecified.  
  - Use `Mr [REDACTED]` or `Ms [REDACTED]` when gender is clear from name, pronouns, or context (e.g., “Mr K. Drzewicki” → `Mr [REDACTED]`, not `Mr [REDACTED] Drzewicki`).
- Legal professionals → Replace with:
  - `a lawyer practising in [TOWN]`
  - `a representative of [INSTITUTION]`
  - `a judge at the [CITY] Court of Appeal`
- Do **not** use abbreviations (e.g., “R.K.” → `[REDACTED]` only). Never partially mask.

#### 🌍 **Geographic Locations**
- Cities, towns, villages → Replace with:
  - `Gdańsk` → `[CITY]`
  - `Siemanowice` → `[TOWN]`
  - `Diyarbakır Sur Municipality` → `[CITY] Sur Municipality`
- Federal/cantonal units:
  - “Canton of Geneva” → `[CITY] Cantonal Court`
  - “Special Settlement, Canton of [CITY]” → `[CITY] Special Settlement`
- Countries:
  - “Republic of Poland” → “Republic of [COUNTRY]”
  - “Kosovo (in accordance with UN Security Council Resolution 1244)” → preserved as-is
  - “A national of Poland” → “a national of [COUNTRY]”

#### 📄 **Case and Application Numbers**
- Replace all case/file/application numbers with consistent templates:
  - `no. 34656/03` → `no. [APPLICATION NUMBER]`
  - `IC 119/05` → `[CASE FILE NO. XXXX/XX]` or `[CASE NUMBER]`
  - `43837/06` → `[APPLICATION NUMBER]`
- **Never** use fixed placeholders like `[NUMBER]`. Reuse the **exact same template** globally (e.g., if `no. [APPLICATION NUMBER]` used once, use it again everywhere).

#### 📅 **Dates**
- **Every single date must be replaced**, including:
  - `15 August 1988` → `[DATE]`
  - `March 2003` → `[MONTH] [YEAR]`
  - `17 April 2004` and `20 October 2004` → `[DATE]` and `[DATE]` respectively (no variation)
  - “on 2 January 2000 and 8 March 2001” → “on [DATE] and [DATE]”
  - “Between October 1989 and December 1992” → “Between [MONTH] [YEAR] and [MONTH] [YEAR]”
  - “17 January 1996 to 16 July 1998” → “Between [MONTH] [YEAR] and [MONTH] [YEAR]”
- **Never** mix formats. Use `[MONTH] [YEAR]` for any partial temporal expression. Do **not** use “X” or “n” in place of dates.

#### 💰 **Monetary Values**
- Replace with `[AMOUNT] [CURRENCY]`:
  - `1,000,000 Swiss francs` → `[AMOUNT] CHF`
  - `TRL 1,000,000,0000` → `[AMOUNT] TRL`
- Retain original currency code if mentioned.
- Use `[AMOUNT]` only if currency is **not specified** and **not essential**.
- Never abbreviate: avoid “$X”, “USD”, “CHF” without parsing.

#### 🏛️ **Institutions and Jurisdictions**
- Specific judicial bodies → Use general form with `[CITY]` token:
  - `Karacabey Civil Court` → `[CITY] Civil Court`
  - `Sztum Prison` → `Zakład Karny (Prison)`
  - `Diyarbakır Labour Court` → `[CITY] Labour Court`
  - `Cantonal Court of [CITY]` → `[CITY] Cantonal Court`
- Government departments:
  - `Ministry of Foreign Affairs` → `Ministry of [DEPARTMENT]`
  - `Ministry of Internal Affairs` → `Ministry of [DEPARTMENT]`
  - `Bağ Kur` → `[CITY] retirement pension fund (Bağ Kur)` (if acronym is key), otherwise `retirement pension fund (Bağ Kur)`
- Well-known international or national bodies (e.g., “Court of Cassation”, “European Parliament”, “Secretariat General”) → **do not anonymize**, unless location or jurisdiction would allow re-identification.

---

### 📌 2. **Preserve Structure and Procedural Integrity**

- **Never reorder events**. Maintain **exact chronological sequence**:
  `arrest → detention → indictment → trial → appeal → conviction → release` → keep intact.
- **Retain all legal terminology verbatim**:
  - “remanded in custody”, “bill of indictment”, “bail application”, “execution proceedings”, “motion for adjournment”
- **Do not simplify or rephrase**:
  - “the court declined to grant bail” → keep **exactly** as is
- **Do not reinterpret facts, arguments, or conclusions**. Preserve original logic, assertions, and legal reasoning.
- **Retain all parenthetical references**:
  - “(see paragraph 42 below)” → unchanged
  - “[Note by the Registry]” → unchanged

---

### 🔤 3. **Consistent Token Reuse & Avoid Over-Generalization**

- **Re-use tokens deterministically**:
  - If `Poznań` → `[CITY]` in one place, use `[CITY]` everywhere else (e.g., `[CITY] District Court`, `[CITY] Regional Court`)
  - Never switch to `[TOWN]` or `[REGION]` unless context clearly justifies finer granularity.
- Avoid **over-generalization**:
  - “organised criminal gang” → **do not** replace with “a criminal network” → keep as-is
  - “land registry survey” → do **not** replace with `[PROJECT DESCRIPTION]`; keep: “conducted a land registry survey”
- **Never** leave partial identifiers:
  - “Mr A.F. Demirkan” → `Mr [REDACTED]` only
  - “March 2003” → `[MONTH] [YEAR]` only

---

### 🔢 4. **Handle Numbers and Quantitative Data Precisely**

- Replace all **counts, durations, percentages, or rates** with:
  - `[NUMBER]` for: `120 witnesses`, `13 persons`, `four years`, `sixty days`, `ten years`, `eight years’ imprisonment`
  - `[AMOUNT]` for monetary values (as above)
- Use correct syntax:
  - `sentenced to eight years’ imprisonment` → `sentenced to [NUMBER] years’ imprisonment`
  - `denied to hear evidence from at least 120 witnesses` → `denied to hear evidence from at least [NUMBER] witnesses`
  - `a period of six months` → `a period of [NUMBER] months`
  - `between 1973 and 1981` → `between [YEAR] and [YEAR]`
- **Never** use “X”, “n”, or “a number of” — always use `[NUMBER]`, `[AMOUNT]`, or `[YEAR]`.

---

### 📏 5. **Preserve Formatting Exactly**

- Maintain **identical formatting**:
  - Section headers: “PROCEDURE”, “THE FACTS”, “I. THE CIRCUMSTANCES OF THE CASE”
  - Bullet points, indentation, line breaks, parentheses, quotes, footnotes
  - Reference syntax: “Article 34 of the Convention”, “Rule 52 § 1”, “Article 29 § 3”
  - Metadata: “no. [APPLICATION NUMBER]”, “Case File No. [CASE FILE NO. XXXX/XX]”
- **Do not alter** document layout or spacing.
- **Do not modify** footnotes or endnotes.

---

### 🎯 6. **Privacy by Design: Prevent Information Leakage**

- Use **consistent, predictable placeholders** exclusively:
  - `[CITY]`, `[TOWN]`, `[REGION]`, `[COUNTRY]`, `[DATE]`, `[MONTH] [YEAR]`, `[NUMBER]`, `[AMOUNT]`, `[DEPARTMENT]`
- Never introduce new placeholders (e.g., `[PROJECT DESCRIPTION]`, `[EVENT]`) unless absolutely necessary and contextually justified.
- **Prevent pattern leakage**:
  - Never anonymize one date as `[DATE]` and another as `[MONTH] [YEAR]` in the same context.
  - Avoid combinations like `[CITY] Regional Court` + `[YEAR]` + `[NUMBER] x 120 witnesses` → all masked uniformly.
- **Do not simplify or generalize action**:
  - “for the construction of a highway” → **keep as-is**
  - “a private construction company” → use “a private construction entity”

---

### 🧼 7. **Zero Tolerance for Incomplete Anonymization**

- **Mandatory rule**: Every identifiable entity must be replaced.  
  Check for:
  - Dates: `21 January 2003`, `5 September 2001`, `December 1992` → all → `[DATE]`
  - Names: `Ömer Koç` → `Mr [REDACTED]` (not `R.K.` or `O.K.`)
  - Numbers: `1524/02` → `[APPLICATION NUMBER]`
  - Institutions: `Katowice` → `[CITY]`
  - Amounts: `1,000,000 Swiss francs` → `[AMOUNT] CHF`
  - Acronyms: `Champ-Dollon Prison` → `Prison (Champ-Dollon)`
- **Fail to anonymize** is **not acceptable**. If a single entity remains identifiable, the output fails.

---

### 🧰 Critical Design Principles (Learned from Feedback)

- In **Example 1**, the assistant left **31 entities unmasked**, including specific dates like `27 February 1996`, `1 May 1993`, `1943`, `Poznań`, and `Poland`. The issue: **inconsistent application of date and location anonymization**. Fix: Apply `[DATE]` and `[CITY]` **to all** such instances.
- In **Example 2**, a high privacy score (0.976) but low utility (0.492) suggests **over-anonymization** via excessive use of generic placeholders (e.g., `"a certain [REDACTED]"` for defendant). Fix: Preserve **contextual specificity** where possible (e.g., keep `"a Polish national"`, `"a lawyer practising in [TOWN]"`) while masking identifiers.
- In **Example 3**, all entities were masked, but the assistant replaced the **Law of 17 June 2004** with `[YEAR] Act`, losing legal specificity. Fix: Retain **named legislation** (`the 2004 Act`) with **date anonymization** via `[YEAR]`, e.g., `Law of [DATE] ([YEAR] Act)`.

---

### ✅ Final Instructions

> Perform the anonymization **in one pass** using a **context-aware, rule-driven, deterministic framework**:
> 1. Scan the document **once**, identifying all entities with precise type (name, date, place, number, etc.).
> 2. Apply **predefined, reusable replacements** using the exact templates above.
> 3. Ensure **no partial anonymization**, no omitted entries, and **consistent token reuse**.
> 4. **Double-check**: every name, date, number, location, institution, currency, and case identifier must be masked.
> 5. Preserve **structure, format, legal terminology, and procedural logic** down to the punctuation level.
> 6. **When in doubt, err on the side of over-anonymization**, but **only if utility is preserved**.
> 7. **Never** replace named laws, international conventions, or standard legal instruments (e.g., “the Convention”, “Rule 52 § 1”) with placeholders unless the jurisdiction or location enables re-identification.
> 8. **Never** use `[YEAR]` for specific dates in the format `YYYY`. Instead, use `[DATE]` for full dates and `[MONTH] [YEAR]` for partial dates.
> 9. For court or institutional names, always use the **[CITY]** pattern where applicable, and never use codes or acronyms unless fully transferred to general form (e.g., `Askeri Yargıtay` → `Military Court of Cassation` remains intact; no anonymization unless location-based ID risk exists).
> 10. **Do not omit** any temporal expressions: every date — including in ranges, comparisons, or durations — must be replaced.
>
> **Output only** the fully anonymized text in the `anonymized_text` field. No explanations. No annotations.

### anonymized_text
[anonymized version of the input text]
```
