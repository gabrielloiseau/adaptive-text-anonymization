# DB-Bio - Mistral-Small-3.2-24B

- Task: `dbbio`
- Model: `mistral_small` (Mistral-Small-3.2-24B)
- Stage: `dynamic`
- Source: `trained_models/dbbio/mistral_small/dynamic`

## Optimized prompt

```
# Task: Anonymize Text While Preserving Occupation and Context

## Objective
Anonymize the given text by redacting all personally identifiable information (PII) while ensuring:
1. The occupation or role of the individual(s) remains clear from the context.
2. The text remains useful and coherent for its intended purpose.
3. The anonymized text does not allow identification of the individual(s) through inference or remaining details.

## Inputs
- `text`: A passage containing personal information about an individual, including names, dates, locations, and other identifying details.

## Outputs
- `anonymized_text`: The input text with all PII redacted, replaced with generic placeholders (e.g., `[Name]`, `[Location]`, `[Year]`), while preserving the occupation, context, and overall meaning.

## Guidelines
### 1. **Redaction Rules**
   - **Names**: Replace all names (first, last, nicknames, titles) with placeholders (e.g., `[Name]`, `[Nickname]`, `[Lastname]`).
   - **Dates**: Replace specific dates, years, or ranges with placeholders (e.g., `[Date]`, `[Year]`, `[Year1]`, `[Year2]`).
   - **Locations**: Replace cities, states, countries, and specific addresses with placeholders (e.g., `[City]`, `[State]`, `[Country]`).
   - **Organizations**: Replace company names, institutions, teams, or clubs with placeholders (e.g., `[Company]`, `[University]`, `[Team Name]`).
   - **Titles/Roles**: Replace specific titles (e.g., "President's Club") with placeholders (e.g., `[Title]`).
   - **Achievements/Events**: Replace specific awards, medals, or event names (e.g., "Order of Australia Medal") with placeholders (e.g., `[Award]`).
   - **Quantitative Data**: Replace specific amounts (e.g., money, distances, speeds) with placeholders (e.g., `[$Amount]`, `[Distance]`, `[Speed]`).
   - **Languages**: Replace specific languages with placeholders (e.g., `[Language1]`, `[Language2]`).

### 2. **Preservation Rules**
   - **Occupation/Role**: Ensure the individual's profession or role is still inferable (e.g., "cyclist," "diplomat," "racing driver").
   - **Context**: Preserve the structure, grammar, and coherence of the original text.
   - **Flow**: Maintain logical connections and narrative flow.

### 3. **Special Cases**
   - **Multiple Individuals**: Redact all names and identifiers for all mentioned individuals.
   - **Historical/Cultural References**: Ensure redaction does not obscure the significance of the context.
   - **Unique Achievements**: Redact specific achievements (e.g., "gold medal in 2004 Olympics") to prevent identification.
   - **Scandals/Controversies**: Redact details of scandals or controversies that could uniquely identify the individual (e.g., "convicted of harassing an ex-girlfriend" → "[Name] faced legal consequences in [Year]").
   - **Chess-Specific Cases**: For chess-related biographies, avoid leaving identifiable details about:
     - Age at achieving titles (e.g., "FIDE Master at 13" → "FIDE Master at [Age]").
     - Specific tournaments or scandals (e.g., "2012 Bundesliga cheating scandal" → "[Year] tournament incident").
     - Suspensions or bans (e.g., "2-year suspension by the German Chess Federation" → "[Organization] issued a suspension").

### 4. **Validation**
   - **Identifiability Check**: Verify that no combination of remaining details (e.g., dates, locations, achievements) can uniquely identify the individual.
   - **Utility Check**: Ensure the text remains useful for its intended purpose (e.g., educational, informational).

## Examples
### Example 1 (Diplomat)
**Input**:
"Yosef Tekoah (born Yosef Tukaczynski; 4 March 1925 – 14 April 1991) was a senior Israeli diplomat and an Israeli doctor and the President of the Ben-Gurion University of the Negev (1975–1981). Tekoah was born in Lyakhavichy, Poland as Yosef Tukaczynski. At the age of five he emigrated with his family to Harbin, due to the rise of fascism in his homeland. Some time after the Fall of Harbin to the Imperial Japanese Army, Tekoah's family moved to Shanghai for financial purposes. He had a Doctorate in international relations from Harvard University, where he also taught and Master's degree in Natural and legal rights from Aurora University. In 1948 he made Aliyah, changed his name to Tekoah and started working for the Ministry of Foreign Affairs, where he met his wife, Ruth Tekoah. During his work in the Israeli Ministry of Foreign Affairs, Tekoah appointed for several positions: The Israel Foreign Ministry legal adviser (1949–1953), Head of Armistice Affairs in the Israeli Ministry of Foreign Affairs (1954–1958), Deputy and Acting Head of the Israeli delegation to the UN (1958–1960), The Israeli Ambassador to Brazil (1960–1962), The Israeli Ambassador to the Soviet Union (1962–1965), VP of the Israeli Foreign Ministry (1965–1967), Permanent Representative of Israel to the United Nations (1968–1975). Tekoah died in 1991 in New York after a Heart attack. Tekoah knew fluent Hebrew, English, Russian, French, Portuguese, Chinese and French."

**Output**:
"[Name] (born [Name2]; [Date1] – [Date2]) was a senior Israeli diplomat and an Israeli doctor and the President of the [University] ([Year1]–[Year2]). [Name] was born in [City], [Country] as [Name2]. At the age of five he emigrated with his family to [City2], due to the rise of fascism in his homeland. Some time after the Fall of [City2] to the Imperial Japanese Army, [Name]'s family moved to [City3] for financial purposes. He had a Doctorate in international relations from [University2], where he also taught and Master's degree in Natural and legal rights from [University3]. In [Year] he made Aliyah, changed his name to [Name] and started working for the Ministry of Foreign Affairs, where he met his wife, [Name3]. During his work in the Israeli Ministry of Foreign Affairs, [Name] was appointed for several positions: The Israel Foreign Ministry legal adviser ([Year4]–[Year5]), Head of Armistice Affairs in the Israeli Ministry of Foreign Affairs ([Year6]–[Year7]), Deputy and Acting Head of the Israeli delegation to the UN ([Year8]–[Year9]), The Israeli Ambassador to [Country2] ([Year10]–[Year11]), The Israeli Ambassador to the [Country3] ([Year12]–[Year13]), VP of the Israeli Foreign Ministry ([Year14]–[Year15]), Permanent Representative of Israel to the United Nations ([Year16]–[Year17]). [Name] died in [Year18] in [City4] after a Heart attack. [Name] knew fluent [Language1], [Language2], [Language3], [Language4], [Language5], [Language6] and [Language7]."

### Example 2 (Comedian)
**Input**:
"Justin Lee Collins (born 28 July 1974) is an English radio host, television presenter and actor. Justin Lee Collins started out as a stand up comedian in his late teens, having been influenced by the stand up of American comedians such as Eddie Murphy, Anthony George and Steve Martin. He then moved on to be a presenter on a number of TV shows. From 2003 – 2005 he hosted his own radio show on XFM, and was one half of the famous duo presenting The Sunday Night Project (previously named The Friday Night Project) alongside Alan Carr for Channel 4. He also hosted numerous specials on Channel 4 entitled 'Bring Back...' reuniting the cast and crew from famous shows or films such as Dallas, Star Wars and Fame. He then took on challenges to become a Mexican Wrestler, a Surfer, a Ballroom Dancer, a Ten Pin Bowler, a High Diver and a West End Star. He later became a West End Star in Rock of Ages. In 2012 he was convicted of harassing an ex-girlfriend. Since his conviction, Collins has sought professional help and now hosts a weekly radio show on Fubar Radio, the UK's only uncensored station. In 2014 Collins starred in the comedy/horror feature film The Hatching alongside Thomas Turgoose and Andrew Lee Potts and in 2015 played a small role in the time travel comedy Time Slips (2015)."

**Output**:
"[Name] [Name2] (born [Date]) is an English radio host, television presenter and actor. [Name] [Name2] started out as a stand up comedian in his late teens, having been influenced by the stand up of American comedians such as [Name3], [Name4] and [Name5]. He then moved on to be a presenter on a number of TV shows. From [Year1] – [Year2] he hosted his own radio show on [Redacted], and was one half of the famous duo presenting The Sunday Night Project (previously named The Friday Night Project) alongside [Name6] for [Channel]. He also hosted numerous specials on [Channel] entitled 'Bring Back...' reuniting the cast and crew from famous shows or films such as [Redacted], [Redacted] and [Redacted]. He then took on challenges to become a Mexican Wrestler, a Surfer, a Ballroom Dancer, a Ten Pin Bowler, a High Diver and a West End Star. He later became a West End Star in [Redacted]. In [Year3] he faced legal consequences. Since then, [Name] has sought professional help and now hosts a weekly radio show on [Redacted], the UK's only uncensored station. In [Year4] [Name] starred in the comedy/horror feature film [Redacted] alongside [Name7] and [Name8] and in [Year5] played a small role in the time travel comedy [Redacted] ([Year5])."

### Example 3 (Chess Player)
**Input**:
"Falko Bindrich (born October 17, 1990) is a German chess grandmaster and trainer. He started to rise as a chess prodigy when he became a FIDE Master at the age of 13 in 2003. He earned his International Master title in 2006 and his grandmaster title a year later. Bindrich played in the 2008 Chess Olympiad, held in Dresden, where his German team placed 13th. He has attended several other prestigious chess events, such as the 2008 Bundesliga and the 2009 and 2010 Chess Olympiads. In October 2012, Falko Bindrich was accused of cheating in the 2012 Bundesliga tournament. In round 2 of the event, in a game against Sebastian Siebrecht, Bindrich had his game declared lost by an arbiter, after he refused to hand over his smartphone which he claimed held personal data and analysis on his former chess games. In January 2013, as a result of his actions, the German Chess Federation (GCF) issued a 2-year suspension from over-the-board play. Bindrich did not accept the decision and filed a protest stating that, if necessary, he would submit the case to court, and later the arbitration court cancelled the ban stating it was issued without legal basis."

**Output**:
"[Name] (born [Date]) is a German chess grandmaster and trainer. He started to rise as a chess prodigy when he became a FIDE Master at the age of [Age] in [Year1]. He earned his International Master title in [Year2] and his grandmaster title a year later. [Name] played in the [Year3] Chess Olympiad, held in [Location], where his German team placed [Number]th. He has attended several other prestigious chess events, such as the [Year3] Bundesliga and the [Year4] and [Year5] Chess Olympiads. In [Month] [Year6], [Name] was accused of an incident in the [Year6] Bundesliga tournament. In round 2 of the event, in a game against [Name2], [Name] had his game declared lost by an arbiter, after he refused to hand over his smartphone which he claimed held personal data and analysis on his former chess games. In [Month] [Year7], as a result of his actions, the German Chess Federation (GCF) issued a suspension. [Name] did not accept the decision and filed a protest stating that, if necessary, he would submit the case to court, and later the arbitration court cancelled the ban stating it was issued without legal basis."

## Key Insights from Feedback
1. **Avoid Unique Combinations**: Redact specific achievements, dates, and locations that could uniquely identify the individual (e.g., "gold medal in 2004 Olympics" → "[Award] in [Year] Olympics").
2. **Preserve Occupation**: Ensure the role (e.g., "cyclist," "diplomat") is still inferable.
3. **Generic Placeholders**: Use consistent placeholders (e.g., `[Name]`, `[Year]`) to avoid reintroducing identifiers.
4. **Iterative Validation**: After redaction, verify that no remaining details can be cross-referenced to identify the individual.
5. **Chess-Specific Nuances**: For chess players, avoid leaving details about:
   - Age at achieving titles (e.g., "FIDE Master at 13" → "FIDE Master at [Age]").
   - Specific tournaments or scandals (e.g., "2012 Bundesliga cheating scandal" → "[Year] tournament incident").
   - Suspensions or bans (e.g., "2-year suspension by the German Chess Federation" → "[Organization] issued a suspension").

## Strategy
1. **Scan for PII**: Identify all names, dates, locations, organizations, and unique achievements.
2. **Replace with Placeholders**: Use generic placeholders while preserving context.
3. **Validate**: Check for identifiability and utility.
4. **Iterate**: Refine redaction if feedback indicates potential identification risks.
```
