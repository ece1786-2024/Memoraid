# Test Data Documentation

## Overview
From the prepared structured QA pairs, the questions are transformed into sentences with early, mid, and advanced stages' patterns. This README file contains the system prompts we used for this transformation.

## Prompts

### Early Stage Alzheimer's Communication Transformation/Generation Prompt:
```
Simulate how a person with early stage Alzheimer's might speak by transforming sentences from a typical conversation to reflect the common communication patterns observed in dementia. Use the following guidelines:
    1. Word-Finding Difficulties (Anomia): Substitute incorrect words for intended terms. For example, replace a specific word with a generic one (e.g., 'that thing' instead of 'remote').
    2. Reduced Verbal Expression: Simplify sentences by reducing the number of words and removing detailed or descriptive language.
    3. Impaired Comprehension: Introduce slight misunderstandings or responses that seem unrelated to the original question or context.
Symptom frequency: low in conversation, minor influence on communication.
Format: Try not to use filler words like "um," "uh," or "..." to represent pauses or hesitations. Instead, directly reflect the transformation through the structure, word choice, or content of the sentence.
```

### Mid Stage Alzheimer's Communication Transformation/Generation Prompt:
```
Simulate how a person with mid stage Alzheimer's might speak by transforming sentences from a typical conversation to reflect the common communication patterns observed in dementia. Use the following guidelines:
    1. Word-Finding Difficulties (Anomia): Substitute incorrect words for intended terms. For example, replace a specific word with a generic one (e.g., 'that thing' instead of 'remote').
    2. Reduced Verbal Expression: Simplify sentences by reducing the number of words and removing detailed or descriptive language.
    3. Impaired Comprehension: Introduce slight misunderstandings or responses that seem unrelated to the original question or context.
    4. Repetition Issues (Perseveration): Repeat certain words, phrases, or topics within the dialogue, even if unnecessary.
    5. Incomplete or Fragmented Sentences: Break sentences into incomplete fragments that may lack grammatical clarity or logical flow.
    6. Language Reversion: Occasionally switch to using simpler vocabulary or phrases in a first-learned language (if applicable).
Symptom frequency: mid frequency in conversation, 1-3 patterns could show simultaneously in one sentence, moderate influence on communication.
Format: Try not to use filler words like "um," "uh," or "..." to represent pauses or hesitations. Instead, directly reflect the transformation through the structure, word choice, or content of the sentence.
```

### Advanced Stage Alzheimer's Communication Transformation/Generation Prompt:
```
Simulate how a person with advanced stage Alzheimer's might speak by transforming sentences from a typical conversation to reflect the common communication patterns observed in dementia. Use the following guidelines:
    1. Word-Finding Difficulties (Anomia): Substitute incorrect words for intended terms. For example, replace a specific word with a generic one (e.g., 'that thing' instead of 'remote').
    2. Reduced Verbal Expression: Simplify sentences by reducing the number of words and removing detailed or descriptive language.
    3. Impaired Comprehension: Introduce slight misunderstandings or responses that seem unrelated to the original question or context.
    4. Repetition Issues (Perseveration): Repeat certain words, phrases, or topics within the dialogue, even if unnecessary.
    5. Incomplete or Fragmented Sentences: Break sentences into incomplete fragments that may lack grammatical clarity or logical flow.
    6. Language Reversion: Occasionally switch to using simpler vocabulary or phrases in a first-learned language (if applicable).
    7. Use of New or Forgotten Words: Create new words to replace forgotten ones, or use unrelated but familiar terms.
    8. Emotional Language: Add occasional outbursts, cursing, or emotionally charged words that seem out of place.
    9. Talking Less or Hesitating More: Include moments of silence or reduced speech output in responses.
Symptom frequency: mid to high frequency in conversation and multiple patterns could show simultaneously in one sentence. Severe influence on communication.
Format: Try not to use filler words like "um," "uh," or "..." to represent pauses or hesitations. Instead, directly reflect the transformation through the structure, word choice, or content of the sentence.
```