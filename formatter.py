from load_config import *
def simplify_logical_expression(expression):
    var_map = {}
    reverse_map = {}  
    current_letter = 'A'
    
    def normalize_variable(var):
        var = var.strip()
        prefixes = ['dw.', 'rtDW.', 'inp.']
        for prefix in prefixes:
            if var.startswith(prefix):
                var = var[len(prefix):]
        return var
    
    def extract_variables(expr):
        import re
        pattern = r'(?:[a-zA-Z][a-zA-Z0-9._]*(?:\s*==\s*[a-zA-Z][a-zA-Z0-9._]*)?)'
        return sorted(set(re.findall(pattern, expr)))
    
    def replace_variable(match):
        nonlocal current_letter
        var = match.group(0).strip()
        normalized_var = normalize_variable(var)
        
        for existing_var, letter in var_map.items():
            if normalize_variable(existing_var) == normalized_var:
                return letter
        
        var_map[var] = current_letter
        reverse_map[current_letter] = var
        current_letter = chr(ord(current_letter) + 1)
        return var_map[var]
    
    if '->' in expression:
        parts = expression.split('->')
        left_part = parts[0].strip()
        right_part = parts[1].strip()
    else:
        left_part = expression
        right_part = ""
    
    all_variables = extract_variables(expression)
    
    normalized_vars = {}
    for var in all_variables:
        normalized = normalize_variable(var)
        if normalized not in normalized_vars:
            normalized_vars[normalized] = var
            if var not in var_map:
                var_map[var] = current_letter
                reverse_map[current_letter] = var
                current_letter = chr(ord(current_letter) + 1)
        else:
            original_var = normalized_vars[normalized]
            var_map[var] = var_map[original_var]
    
    import re
    pattern = r'[a-zA-Z][a-zA-Z0-9._]*(?:\s*==\s*[a-zA-Z][a-zA-Z0-9._]*)?'
    
    simplified_left = re.sub(pattern, replace_variable, left_part)
    
    if right_part:
        simplified_right = re.sub(pattern, replace_variable, right_part)
        simplified = f"{simplified_left} -> {simplified_right}"
    else:
        simplified = simplified_left
    
    mapping_explanation = "\nVariable Mappings:\n"
    
    letter_to_vars = {}
    for var, letter in var_map.items():
        if letter not in letter_to_vars:
            letter_to_vars[letter] = []
        letter_to_vars[letter].append(var)
    
    for letter in sorted(letter_to_vars.keys()):
        vars_list = letter_to_vars[letter]
        mapping_explanation += f"{letter} -> " + " = ".join(f'"{var}"' for var in vars_list) + "\n"
    
    return simplified, mapping_explanation

def main():
    #print("Logical Expression Simplifier")
    #print("-----------------------------")
    #print("\nEnter your logical expression:")
    
    try:
        # Read expression from file instead of input
        specs_path = INPUT_DIR
        try:
            with open(specs_path, "r", encoding='utf-8') as f:
                expression = f.read().strip()
        except Exception as file_err:
            print(f"Error reading input file: {file_err}")
            return
        if not expression:
            print("Error: Empty expression in input file")
            return
            
        simplified, mappings = simplify_logical_expression(expression)
        
        output_file = SIMPLIFIED_FILE
        with open(output_file, "w", encoding='utf-8') as f:
            f.write("logical statement: " + expression + "\n\n")
            f.write("simplified statement : " + simplified + "\n\n")
            f.write(mappings)
            
        print(f"\nOutput has been saved!")


    except Exception as e:
        print(f"Error processing expression: {str(e)}")

if __name__ == "__main__":
    main()
