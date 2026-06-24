import os
import json
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key = os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "llama-3.1-8b-instant"

def call_llm(system_prompt, user_message):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.3,
        max_tokens=500   
    )
    return response.choices[0].message.content



def load_articles():
    with open("data/articles.json", "r", encoding="utf-8") as f:
        return json.load(f)
    
# A - Zero-Shot
def zero_shot(article_text):
    system = "You are a helpful assistant."
    user = f"Summarize the following article in 3 sentences.\n\nArticle:\n{article_text}"
    return call_llm(system, user)

# B - Role Prompting
def role_prompting(article_text):
    system = ("You are a scientific researcher delivering information to high schoolers on a field trip."
              "You are explaining clearly, informatively, and explain terminology where necessary in a concise manner.")
    user = f"Summarize the following article in 3 sentences for someone with minimal understanding of the topic.\n\nArticle:\n{article_text}"
    return call_llm(system, user)

# C - Few-Shot
FEW_SHOT_EXAMPLES = """
    Example 1:
    Article: Quantum computing is a type of computation that harnesses quantum mechanical phenomena such as superposition and entanglement to process information. Unlike classical computers that use bits representing 0 or 1, quantum computers use qubits which can represent both states simultaneously. This allows quantum computers to solve certain problems exponentially faster than classical machines.
    Summary: Quantum computing uses the principles of quantum mechanics to process information in fundamentally new ways. Its basic unit, the qubit, can exist in multiple states at once unlike a classical bit. This enables quantum computers to tackle certain complex problems far faster than traditional computers.

    Example 2:
    Article: RNA, or ribonucleic acid, is a molecule essential to all known forms of life. It is involved in coding, decoding, regulation, and expression of genes. RNA is transcribed from DNA and plays a central role in protein synthesis, carrying genetic instructions from the nucleus to the ribosomes where proteins are built.
    Summary: RNA is a fundamental biological molecule involved in turning genetic information into proteins. It is produced from DNA and carries instructions out of the cell nucleus. These instructions are then used by ribosomes to build the proteins that cells need to function.
"""


def few_shot(article_text):
    system = "You are a helpful assistant, who write concise, accurate, and informative summaries."
    user = (
        f"{FEW_SHOT_EXAMPLES}\n\n"
        f"Summarize the following article in 3 sentences, following the same manner and style as the examples above.\n\n"
        f"Article:\n{article_text}")
    return call_llm(system, user)

# D - Chain-of-Thought
def chain_of_thought(article_text):
    system = "You are a helpful assistant, who write concise, accurate, and informative summaries."
    user = (
        f"Read the article and provide 3 key points from there:\n"
        f"Step 1: List the 3 main ideas.\n"
        f"Step 2: Write a summary in 3 sentences using those ideas.\n"
        f"Article:\n{article_text}")
    return call_llm(system, user)

# E - Output Formatting (JSON)
def json_output(article_text):
    system = ("You are an exact assistant who always responds with valid JSON files."
              "Never include anything that would make your response an invalid for JSON.")
    user = (
        f"Summarize the following article and return ONLY a JSON object with exactly the fields listed:\n"
        f'{{"headline": "one sentence title", "summary": "2-3 sentence summary", "key_terms": ["term1", "term2", "term3"]}}\n\n'
        f"Article:\n{article_text}")
    raw = call_llm(system, user)

    try:
        cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        parsed = json.loads(cleaned)
        return {"raw" : raw, "parsed": parsed, "valid_json": True}
    except json.JSONDecodeError:
        return {"raw": raw, "parsed":None, "valid_json": False}

def run_all_experiments():
    articles = load_articles()
    results = []

    experiments = [
        ("zero_shot",        zero_shot),
        ("role_prompting",   role_prompting),
        ("few_shot",         few_shot),
        ("chain_of_thought", chain_of_thought),
        ("json_output",      json_output),
    ]

    total = len(articles) * len(experiments)
    count = 0

    for title, text in articles.items():
        for technique_name, func in experiments:
            count += 1
            print(f"[{count}/{total}] {technique_name} - {title}")

            output = func(text)

            results.append({
                "article": title, "technique": technique_name, "output": output,
                "scores": {
                    "accuracy": None,
                    "conciseness": None,
                    "consistency": None
                }
            })
            time.sleep(3)
    output_path = os.path.join("data", "results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nDone! {len(results)} results saved to {output_path}")

if __name__=="__main__":
    run_all_experiments()