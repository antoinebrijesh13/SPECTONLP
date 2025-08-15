````markdown
# SPECTONLP - Tool Instructions

Follow these steps to run the SPECTONLP tool:

---

## 1. Clone the Repository
Clone the repository into your working directory using:

```bash
git clone https://github.com/antoinebrijesh13/SPECTONLP.git
````

---

## 2. Install Required Packages

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## 3. Set Up Google API Key

Create a `.env` file in the project root and add your Google API key:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

You can obtain an API key from [AI Studio](https://ai.google.com/studio).

---

## 4. Configure Base Folder

Open `config.json` and update the `"base_folder"` path to match your working directory.

Example:

```json
"base_folder": "C:/Users/YourUsername"
```

---

## 5. Add Input Specifications

Open `SPEC2NLP/specs/specs.txt`.
Add your input specifications and save the file.

---

## 6. Run the Pipeline

Execute the pipeline to run the full process:

```bash
python pipeline.py
```

This will process your input specifications and generate the output according to the pipeline logic.

---

## Notes

* Ensure all paths in `config.json` are correct.
* Make sure the `.env` file is in the project root and contains a valid API key.

## Additional 
---
Paths (paths)

input: Path to your input specification file.

cache: Directory to store intermediate and final outputs.
---
Scripts (scripts)

formatter_script, pattern_checker_script, simplifier_script, verify_equivalence_script, nl_translation_script: Paths to the respective pipeline scripts.
---
simplified_expression_file: Path to store the simplified logical expressions.

final_result_file: Path to store the final pipeline results.

nlp_translation_file: Path or name for storing natural language translations.
---
Simplifier (simplifier)

model: LLM model used for simplifying logical expressions.

temperature: Controls randomness of the output (lower = more deterministic).

top_p, top_k: Sampling parameters to control diversity in generated output.

max_output_tokens: Maximum tokens the model can generate for simplification.
---
Natural Language (natural_language)

model: LLM model used for translating logical expressions into natural language.

temperature, top_p, top_k: Sampling parameters for translation.

max_output_tokens: Maximum tokens for natural language output.
---
Conditions (conditions)

distinct_variable_threshold: Threshold for the number of distinct variables before applying special handling in simplification.
---
