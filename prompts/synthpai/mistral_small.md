# SynthPAI - Mistral-Small-3.2-24B

- Task: `synthpai`
- Model: `mistral_small` (Mistral-Small-3.2-24B)
- Stage: `dynamic`
- Source: `trained_models/synthpai/mistral_small/dynamic`

## Optimized prompt

```
# Enhanced Anonymization Task Instructions

## Objective
Anonymize text while preserving meaning, tone, and utility by:
1. Removing/Generalizing identifiable personal attributes
2. Maintaining original emotional tone and structure
3. Ensuring output is distinct from input while remaining natural

## Core Requirements

### 1. Anonymization Rules (Enhanced)
- **Occupations**:
  - Replace with generic terms ("professional", "individual", "person")
  - Avoid domain-specific terms unless culturally significant
  - Example: "engineer" → "professional", "coding" → "working"

- **Locations**:
  - Generalize to broader categories
  - Remove specific place names
  - Example: "lane-way cafes" → "hidden cafes", "northern regions" → "certain regions"

- **Personal Habits/Routines**:
  - Replace with broader concepts
  - Example: "gym fees" → "fitness fees", "passeggiata" → "post-work stroll"

- **Proper Nouns**:
  - Remove or rephrase to generic concepts
  - Example: "Dia sin carro" → "a day where vehicles vanish"

- **Domain Jargon**:
  - Replace with generic terms unless culturally significant
  - Example: "impromptu poetry slams" → "spontaneous spoken word"

- **Age/Time References**:
  - Generalize
  - Example: "older areas" → "older communities", "uni classes" → "academic sessions"

- **Cultural Terms**:
  - Preserve if non-identifying
  - Example: "jazz" → "music", "cultural cardio" → "cultural cardio"

### 2. Preservation Rules (Enhanced)
- **Sentiment**:
  - Maintain original emotional tone
  - Preserve emojis and playful elements
  - Example: "haha" → "haha", "lol" → "lol"

- **Structure**:
  - Keep original sentence structure when possible
  - Maintain natural flow and readability

- **Humor**:
  - Preserve playful elements
  - Example: "human tetris" → "human tetris"

- **Cultural Terms**:
  - Keep if non-identifying
  - Example: "passeggiata" → "post-work stroll" (Italian term preserved in concept)

### 3. Utility Enhancement (Enhanced)
- **Meaning**:
  - Ensure output makes complete sense
  - Use more specific terms when possible (score ≥ 0.8)
  - Example: "modern sustainable designs" (better than "new eco-friendly designs")

- **Detail Level**:
  - Match original specificity
  - Example: "transforming urban spaces" (better than "reshaping our cities")

- **Paraphrasing**:
  - Use appropriate techniques
  - Example: "spontaneous spoken word" (better than "impromptu poetry slams")

### 4. Distinctness Requirements (Enhanced)
- **Changes**:
  - Make at least one meaningful change per sentence
  - Example: "older areas" → "older communities"

- **Identifiability**:
  - Remove all potentially identifying information
  - Example: "vehicles" instead of "cars"

- **Originality**:
  - Ensure output is distinct from input
  - Example: "handling tasks" instead of "editing footage"

### 5. Special Cases (Enhanced)
- **Work Activities**:
  - Generalize to "work" or "tasks"
  - Example: "engineer" → "professional"

- **Technologies**:
  - Replace with "devices" or "equipment"

- **Personal Routines**:
  - Generalize to broader concepts
  - Example: "gym fees" → "fitness fees"

- **Unique References**:
  - Remove or generalize
  - Example: "Dia sin carro" → "a day where vehicles vanish"

- **Cultural Terms**:
  - Preserve if non-identifying
  - Example: "passeggiata" → "post-work stroll"

## Example Workflow (Enhanced)
1. Identify all potentially identifying elements in the text
2. Replace each with the most appropriate generic term
3. Verify the output:
   - Makes complete sense
   - Preserves original meaning and tone
   - Contains at least one meaningful change per sentence
   - Removes all identifiable information
4. If utility score is below 0.8, refine replacements to be more specific while still anonymous
5. Ensure emojis and playful language remain intact

## Evaluation Criteria (Enhanced)
- **Privacy**: No identifiable information remains
- **Utility**: Output score ≥ 0.8 (preserves meaning and detail)
- **Distinctness**: Output is clearly different from input
- **Tone**: Matches original emotional tone
- **Structure**: Maintains original sentence structure when possible
- **Humor**: Preserves playful elements

## Example Refinements from Feedback (Enhanced)
- "working outdoors" → "working in natural settings" (better preserves meaning)
- "northern regions" → "certain regions" (more generic)
- "culinary enthusiasts" → "food professionals" (more neutral)
- "shaping cityscapes" → "working in urban environments" (more generic)
- "passeggiata" → "post-work stroll" (preserves cultural concept while anonymizing)
- "uni classes" → "academic sessions" (more generic)

## Additional Guidelines
- For Italian terms like "passeggiata", preserve the concept but generalize the term
- Maintain emojis and playful language to preserve tone
- When replacing occupations, use "professional" or "individual" instead of specific roles
- For location references, generalize to broader categories
- Ensure the output remains natural and conversational
```
