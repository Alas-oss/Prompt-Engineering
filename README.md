# Prompt Engineering

Accross given 10 Wikipedia articles compare 5 prompting techniques for text summarization. Scoring each technique on accuracy, conciseness, and consistency (1-5 scale).

## Setup

1. Clone this repo
2. Create a virtual environment: 'python -m venv venv'
3. Activate it: '.\venv\Scripts\activate' (for Windows) or 'source venv/bin/activate' (for Max/Linux)
4. Install the necessary dependencies: 'pip install -r requirements.txt'
5. Create a '.env' file in the root folder with your Groq API key
    GROQ_API_KEY=replace_with_your_key

## How to Run

### Step 1 - Fetch the articles: python src/fetch_articles.py
This will download the 10 Wikipedia articles and save them to 'data/articles.json'.

### Step 2 - Run the experiments: python src/prompt_experiments.py
Run all 5 prompting techniques accross all 10 articles and save the results to 'data/results.json'.

### Step 3 - Analyze results: python src/analyze_results.py
Read the scored results that are printed and given an average score table per technique to the terminal.

## Experiment
### Technique -> Description

Zero-shot -> Direct instructions with no examples 

Role prompting -> Model given a persona before summarizing

Few-shot -> Two examples are given for input/output pairs show before given the real article

Chain-of-Thought -> Model lists key ideas first, showing its thought process, then writes the summary

Output Formatting (JSON) -> Model retuns structured JSON with a headline, summary, and key terms related to each of the articles separately

## Results Summary


| Technique        | Accuracy | Conciseness | Consistency | Overall |
|------------------|----------|-------------|-------------|---------|
| json_output      | 4.8      | 5.0         | 4.0         | 4.6     |
| role_prompting   | 5.0      | 4.5         | 4.0         | 4.5     |
| few_shot         | 5.0      | 4.3         | 4.0         | 4.43    |
| chain_of_thought | 5.0      | 3.3         | 5.0         | 4.43    |
| zero_shot        | 5.0      | 3.9         | 3.0         | 3.97    |

**Winner: json_output** with an overall average score of 4.6.
See `summary_report.md` for the full analysis of this project.

## Model User
- LLM: `llama-3.1-8b-instant` via Groq
- Dataset: 10 Wikipedia article introductions (Machine learning, Climate change,
  Photosynthesis, World War II, Artificial intelligence, Quantum computing,
  Solar energy, Electric vehicle, Blockchain, RNA)