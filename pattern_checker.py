import re
from load_config import *

def check_double_negation(logical_statement):
    """
    Check if the logical statement contains double negation patterns like !!(...)
    """
    pattern = r'!\(\(+!.*?(?:\)\)+|(?:\s*&&|\s*\|\||\s*->))'
    return bool(re.search(pattern, logical_statement))

def count_distinct_variables(logical_statement):
    """
    Count distinct alphabetic variables in the logical statement.
    """
    cleaned = re.sub(r'[!&|()\s\-]', '', logical_statement)
    return len(set(re.findall(r'[A-Za-z]', cleaned)))

def main():
    try:
        with open(SIMPLIFIED_FILE, 'r', encoding='utf-8') as f:
            logical_statement = None
            for line in f:
                line = line.strip()
                if line.lower().startswith("simplified statement :"):
                    logical_statement = line.split(":", 1)[1].strip()
                    break

        if not logical_statement:
            print("Error: Could not find simplified statement in the file")
            exit(2)  # indicate failure to main pipeline

        double_negation = check_double_negation(logical_statement)
        var_count = count_distinct_variables(logical_statement)

        print(f"Double negation: {double_negation}")
        print(f"Number of distinct variables: {var_count}")
        exit(1 if double_negation or var_count > 5 else 0)

    except FileNotFoundError:
        print(f"Error: {SIMPLIFIED_FILE} not found")
        exit(2)
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(3)

if __name__ == "__main__":
    main()
