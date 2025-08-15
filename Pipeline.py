import subprocess
import sys
import os
from load_config import *
from verify_equivalence import verify_equivalence  # import your verification function

def run_script(script_name, cwd=None):
    script_path = os.path.join(cwd or BASE_FOLDER, script_name)
    print(f"\nRunning {script_name}...")
    try:
        result = subprocess.run([sys.executable, script_path], cwd=cwd or BASE_FOLDER)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        raise

def main():
    print("=== Step 1: Run Formatter ===")
    run_script(FORMATTER_SCRIPT) 

    print("\n=== Step 2: Run Pattern Checker ===")
    pattern_code = run_script(PATTERN_CHECKER_SCRIPT)
    if pattern_code == 1:
        print("SIMPLYFING....")
        run_script(SIMPLIFIER_SCRIPT)
    elif pattern_code != 0:
        print("Pattern checker failed. Stopping pipeline.")
        run_script(NL_TRANSLATION_SCRIPT)

    print("\n=== Step 3: Verify Equivalence ===")
    if not verify_equivalence():
        print("\nVerification failed. Stopping pipeline.")
        return  # Stop immediately if verification fails

    print("\n=== Step 4: Run Natural Language Translation ===")
    run_script(NL_TRANSLATION_SCRIPT)

if __name__ == "__main__":
    main()
