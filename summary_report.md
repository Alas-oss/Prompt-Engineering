# Prompt Engineering - Summary Report

## The task

Accross given 10 Wikipedia articles compare 5 prompting techniques for text summarization. Scoring each technique on accuracy, conciseness, and consistency (1-5 scale).

| Technique | Accuracy | Conciseness | Consistency | Overall |
| :--- | :---: | :---: | :---: | :---: |
| **json_output** | 4.8 | 5.0 | 4.0 | **4.60** |
| **role_prompting** | 5.0 | 4.5 | 4.0 | 4.50 |
| **few_shot** | 5.0 | 4.3 | 4.0 | 4.43 |
| **chain_of_thought** | 5.0 | 3.3 | 5.0 | 4.43 |
| **zero_shot** | 5.0 | 3.9 | 3.0 | 3.97 |

**Optimal performing technique:** `json_output` (overall average: 4.6)

## Which Technique Scored Best and Why

JSON output scored the highest overall, with a score of 4.6 because the srtuctured format makes the model be disciplined. Moreover, it cannot stray away from the given format, when it has to fit its reponse into specific JSON fields. This strict constraint logically produced the most concise reponses of all the 5 technique, with a score of 5.0. While maintaing high accuracy across all of the 10 articles.

## A Surprising Finding

Chain-of-Thought (CoT) was the most consistent technique by far with a score of 5.0, as it produced the exact same "Step 1 \n Step 2" structure every time regardless of topic, but it had the lowest concisesness of all techniques, with a score of 3.3. This suggests CoT is valuable when you need a reliable structure and don't mind verbose output, which could be improved by changing the prompt slightly and making it more specific.

## Recommended Default Prompt
### For the winning technique: json_output

System prompt:
"You are an exact assistant who always responds with valid JSON files."
"Never include anything that would make your response invalid for JSON."

### Using the mesage template:

Summarize the following article and return ONLY a JSON object with exactly the fields listed:
{"headline": "one sentence title", "summary": "2-3 sentence summary", "key_terms": ["term1", "term2", "term3"]}

Article:
{article_text}

Reason: JSON output produced the best balance of accuracy and conciseness, and the structured format makes the output directly usable in any downstream application without further parsing or cleanup, which is a practical advantage in any real production system.