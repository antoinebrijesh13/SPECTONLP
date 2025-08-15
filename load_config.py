import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Project root (default to current folder)
PROJECT_ROOT = Path(__file__).parent.resolve()

# Load config.json
with open(PROJECT_ROOT / "config.json", "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

# Base folder (can be overridden by .env)
BASE_FOLDER = Path(os.getenv("BASE_FOLDER", CONFIG["paths"].get("base_folder", PROJECT_ROOT)))
if not BASE_FOLDER.exists():
    BASE_FOLDER = PROJECT_ROOT  # fallback to project folder

# Paths
INPUT_DIR = BASE_FOLDER / CONFIG["paths"]["input"]
CACHE_DIR = BASE_FOLDER / CONFIG["paths"]["cache"]
SIMPLIFIED_FILE = BASE_FOLDER / CONFIG["paths"]["simplified_expression_file"]
FORMATTER_SCRIPT = BASE_FOLDER / CONFIG["paths"]["formatter_script"]
PATTERN_CHECKER_SCRIPT = BASE_FOLDER / CONFIG["paths"]["pattern_checker_script"]
VERIFY_EQUIV_SCRIPT = BASE_FOLDER / CONFIG["paths"]["verify_equivalence_script"]
NL_TRANSLATION_SCRIPT = BASE_FOLDER / CONFIG["paths"]["nl_translation_script"]
FINAL_RESULT_FILE = BASE_FOLDER / CONFIG["paths"]["final_result_file"]
NLP_TRANSLATION_FILE = BASE_FOLDER / CONFIG["paths"]["nlp_translation_file"]
SIMPLIFIER_SCRIPT = BASE_FOLDER / CONFIG["paths"]["simplifier_script"]

# Simplifier settings
SIMPLIFIER_MODEL = CONFIG["simplifier"]["model"]
SIMPLIFIER_TEMPERATURE = CONFIG["simplifier"]["temperature"]
SIMPLIFIER_TOP_P = CONFIG["simplifier"]["top_p"]
SIMPLIFIER_TOP_K = CONFIG["simplifier"]["top_k"]
SIMPLIFIER_MAX_TOKENS = CONFIG["simplifier"]["max_output_tokens"]

# Natural language settings
NL_MODEL = CONFIG["natural_language"]["model"]
NL_TEMPERATURE = CONFIG["natural_language"]["temperature"]
NL_TOP_P = CONFIG["natural_language"]["top_p"]
NL_TOP_K = CONFIG["natural_language"]["top_k"]
NL_MAX_TOKENS = CONFIG["natural_language"]["max_output_tokens"]

# Conditions
DISTINCT_VAR_THRESHOLD = CONFIG["conditions"]["distinct_variable_threshold"]

# API key from .env
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")
