from z3 import *
from z3 import unsat
import re
from load_config import *
# --- File reading for user-specific paths ---
def read_logical_statement(statement_type="original"):
    """Read logical statements from fixed file paths as per user requirements."""
    try:
        if statement_type == "original":
            file_path = SIMPLIFIED_FILE
            with open(file_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                if first_line.lower().startswith("logical statement:"):
                    return first_line[len("logical statement:"):].strip()
                else:
                    print("Error: First line does not start with 'logical statement:'")
                    return None
        elif statement_type == "simplified":
            file_path = FINAL_RESULT_FILE
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        else:
            print(f"Unknown statement_type: {statement_type}")
            return None
    except FileNotFoundError:
        print(f"Error: {file_path} not found")
        return None
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return None

# --- Z3 variable and parsing logic (from user code) ---
def create_variable(var_name):
    if var_name.startswith('IN_') or var_name in ['PLAY', 'REW', 'FF', 'EMPTY', 'DISCINSERT']:
        return Int(var_name)
    elif any(var_name.startswith(prefix) for prefix in ['inp.', 'rtY.', 'rtDW.', 'dw.']):
        if any(x in var_name for x in ['is_', 'has_', 'can_', 'Eject', '_sens']):
            return Bool(var_name)
        else:
            return Int(var_name)
    else:
        return Int(var_name)

def tokenize_statement(statement):
    statement = re.sub(r'(\w+(?:\.\w+)*)\s*<\s*-\s*(\d+)', r'\1 < -\2', statement)
    statement = re.sub(r'(\w+(?:\.\w+)*)\s*>\s*-\s*(\d+)', r'\1 > -\2', statement)
    statement = re.sub(r'(\w+(?:\.\w+)*)\s*==\s*-\s*(\d+)', r'\1 == -\2', statement)
    statement = re.sub(r'(\w+(?:\.\w+)*)\s*!=\s*-\s*(\d+)', r'\1 != -\2', statement)
    statement = re.sub(r'(\w+(?:\.\w+)*)\s*>=\s*-\s*(\d+)', r'\1 >= -\2', statement)
    statement = re.sub(r'(\w+(?:\.\w+)*)\s*<=\s*-\s*(\d+)', r'\1 <= -\2', statement)
    statement = re.sub(r'(\w+(?:\.\w+)*)\s*\+\s*(\d+)', r'ARITH_ADD_\1_\2', statement)
    statement = re.sub(r'(\w+(?:\.\w+)*)\s*-\s*(\d+)', r'ARITH_SUB_\1_\2', statement)
    replacements = {
        '&&': ' AND ',
        '||': ' OR ',
        '->': ' IMPLIES ',
        '==': ' EQUALS ',
        '!=': ' NOTEQUALS ',
        '>=': ' GEQ ',
        '<=': ' LEQ ',
        '!': ' NOT '
    }
    for op, placeholder in replacements.items():
        statement = statement.replace(op, placeholder)
    statement = statement.replace('(', ' ( ').replace(')', ' ) ')
    statement = statement.replace('>', ' > ').replace('<', ' < ')
    tokens = statement.split()
    for i, token in enumerate(tokens):
        if token == 'AND': tokens[i] = '&&'
        elif token == 'OR': tokens[i] = '||'
        elif token == 'IMPLIES': tokens[i] = '->'
        elif token == 'EQUALS': tokens[i] = '=='
        elif token == 'NOTEQUALS': tokens[i] = '!='
        elif token == 'GEQ': tokens[i] = '>='
        elif token == 'LEQ': tokens[i] = '<='
        elif token == 'NOT': tokens[i] = '!'
        elif token.startswith('ARITH_ADD_'):
            parts = token.split('_', 2)
            if len(parts) >= 3:
                var_name = parts[2].rsplit('_', 1)[0]
                num = parts[2].rsplit('_', 1)[1]
                tokens[i] = f"{var_name}+{num}"
        elif token.startswith('ARITH_SUB_'):
            parts = token.split('_', 2)
            if len(parts) >= 3:
                var_name = parts[2].rsplit('_', 1)[0]
                num = parts[2].rsplit('_', 1)[1]
                tokens[i] = f"{var_name}-{num}"
    return tokens

def get_arith_expr(expr_str, variables):
    if '+' in expr_str:
        var_name, num = expr_str.split('+')
        if var_name not in variables:
            variables[var_name] = create_variable(var_name)
        return variables[var_name] + int(num)
    elif '-' in expr_str:
        if expr_str.startswith('-'):
            return -int(expr_str[1:])
        else:
            var_name, num = expr_str.split('-')
            if var_name not in variables:
                variables[var_name] = create_variable(var_name)
            return variables[var_name] - int(num)
    elif expr_str.isdigit():
        return int(expr_str)
    else:
        if expr_str not in variables:
            variables[expr_str] = create_variable(expr_str)
        return variables[expr_str]

def parse_expression(tokens, idx, variables):
    if idx >= len(tokens):
        raise ValueError("Unexpected end of expression")
    if tokens[idx] == '(': 
        idx, expr = parse_subexpression(tokens, idx + 1, variables)
        return idx, expr
    elif tokens[idx] == '!':
        idx, term = parse_expression(tokens, idx + 1, variables)
        return idx, Not(term)
    else:
        if idx + 2 < len(tokens) and tokens[idx + 1] in ['==', '!=', '>', '<', '>=', '<=']:
            left_str = tokens[idx]
            op = tokens[idx + 1]
            right_str = tokens[idx + 2]
            if left_str.isdigit():
                left_val = int(left_str)
            else:
                left_val = get_arith_expr(left_str, variables)
            if right_str.isdigit():
                right_val = int(right_str)
            else:
                right_val = get_arith_expr(right_str, variables)
            if op == '==':
                expr = left_val == right_val
            elif op == '!=':
                expr = left_val != right_val
            elif op == '>':
                expr = left_val > right_val
            elif op == '<':
                expr = left_val < right_val
            elif op == '>=':
                expr = left_val >= right_val
            elif op == '<=':
                expr = left_val <= right_val
            return idx + 3, expr
        else:
            term = tokens[idx]
            if term.lower() == 'true':
                return idx + 1, True
            elif term.lower() == 'false':
                return idx + 1, False
            elif term.isdigit():
                return idx + 1, int(term)
            else:
                if '+' in term or '-' in term:
                    return idx + 1, get_arith_expr(term, variables)
                else:
                    if term not in variables:
                        variables[term] = create_variable(term)
                    return idx + 1, variables[term]

def parse_subexpression(tokens, idx, variables):
    if idx >= len(tokens):
        raise ValueError("Unexpected end of expression")
    if tokens[idx] == ')':
        return idx + 1, True
    idx, left_expr = parse_expression(tokens, idx, variables)
    if idx >= len(tokens) or tokens[idx] == ')':
        return idx + 1, left_expr
    while idx < len(tokens) and tokens[idx] != ')':
        op = tokens[idx]
        if op == '&&':
            idx, right_expr = parse_expression(tokens, idx + 1, variables)
            left_expr = And(left_expr, right_expr)
        elif op == '||':
            idx, right_expr = parse_expression(tokens, idx + 1, variables)
            left_expr = Or(left_expr, right_expr)
        elif op == '->':
            idx, right_expr = parse_expression(tokens, idx + 1, variables)
            left_expr = Implies(left_expr, right_expr)
        else:
            raise ValueError(f"Unexpected token: {op}")
    if idx < len(tokens) and tokens[idx] == ')':
        idx += 1
    return idx, left_expr

def parse_statement(statement):
    if not statement.strip().startswith('('):
        statement = f"({statement})"
    balanced = 0
    for i, char in enumerate(statement):
        if char == '(': balanced += 1
        elif char == ')': balanced -= 1
        elif i < len(statement) - 1 and statement[i:i+2] == '->' and balanced == 0:
            statement = f"({statement[:i]}) -> ({statement[i+2:]})"
            break
    tokens = tokenize_statement(statement)
    variables = {}
    _, expr = parse_subexpression(tokens, 0, variables)
    return expr, variables

def verify_equivalence():
    print("\nLogical Statement Equivalence Verifier using Z3")
    print("===============================================")
    print("Reading logical statements from input files...")
    try:
        statement1 = read_logical_statement(statement_type="original")
        if not statement1:
            print("Error: Could not read original statement")
            return False
        statement2 = read_logical_statement(statement_type="simplified")
        if not statement2:
            print("Error: Could not read simplified statement")
            return False
        print("\nOriginal Statement:")
        print(statement1)
        print("\nSimplified Statement:")
        print(statement2)
        expr1, vars1 = parse_statement(statement1)
        expr2, vars2 = parse_statement(statement2)
        all_vars = {**vars1, **vars2}
        s = Solver()
        s.add(expr1 != expr2)
        result = s.check()
        print("\nVerification Result:")
        print("--------------------")
        if result == unsat:
            print("✓ The statements are semantically equivalent.")
            print("  Both statements yield the same truth value for all possible variable assignments.")
            return True
        else:
            print("✗ The statements are NOT semantically equivalent.")
            print("  Here's a counterexample where they differ:")
            m = s.model()
            print("\nVariable assignments in counterexample:")
            for var in sorted(all_vars.keys()):
                if var in m:
                    print(f"  {var} = {m[all_vars[var]]}")
            print("\nExpression evaluations:")
            print(f"  Original statement evaluates to: {m.evaluate(expr1)}")
            print(f"  Simplified statement evaluates to: {m.evaluate(expr2)}")
            return False
    except Exception as e:
        print(f"\nError during verification: {str(e)}")
        print("Please check your input syntax and try again.")
        return False
    print("\n" + "="*50)

if __name__ == "__main__":
    verify_equivalence()
