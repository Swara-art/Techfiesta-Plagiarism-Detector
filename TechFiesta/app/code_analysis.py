import ast
import re
from radon.visitors import ComplexityVisitor

# --- Mock "Professor's Solution" ---
# In a real app, you would load this from a database.
MOCK_CODE_SOLUTION = """
def calculate_fibonacci(n):
    # Returns the nth fibonacci number
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(n - 1):
            a, b = b, a + b
        return b

if __name__ == "__main__":
    print(calculate_fibonacci(10))
"""

# --- Helper Functions ---

def normalize_code(code_text: str) -> str:
    """Strips comments, docstrings, and empty lines to see the raw logic."""
    # Remove single-line comments
    code_text = re.sub(r'#.*', '', code_text)
    # Remove multi-line docstrings
    code_text = re.sub(r'""".*?"""', '', code_text, flags=re.DOTALL)
    code_text = re.sub(r"'''.*?'''", '', code_text, flags=re.DOTALL)
    # Remove empty lines
    return "\n".join([line for line in code_text.splitlines() if line.strip()])

def get_ast_structure(code_text: str) -> str:
    """
    Parses code into an Abstract Syntax Tree (AST) and returns
    a string representing the STRUCTURE (e.g., 'FunctionDef-If-Return').
    This ignores variable names entirely.
    """
    try:
        tree = ast.parse(code_text)
        # Create a signature string of all node types in order
        structure = "-".join([type(node).__name__ for node in ast.walk(tree)])
        return structure
    except SyntaxError:
        return "SyntaxError"

def get_cyclomatic_complexity(code_text: str) -> float:
    """Calculates how complex the code flow is."""
    try:
        visitor = ComplexityVisitor.from_code(code_text)
        total_complexity = 0
        func_count = 0
        for func in visitor.functions:
            total_complexity += func.complexity
            func_count += 1
        return total_complexity / func_count if func_count > 0 else 0
    except Exception:
        return 0.0

# --- Main Code Analysis Function ---

def perform_code_analysis(extracted_code: str) -> dict:
    """
    Compares the uploaded code against the Mock Solution using
    AST Structure and Cyclomatic Complexity.
    """
    # 1. Analyze the User's Submission
    norm_sub = normalize_code(extracted_code)
    sub_ast = get_ast_structure(norm_sub)
    sub_complexity = get_cyclomatic_complexity(norm_sub)
    
    # 2. Analyze the Mock Solution (The "Source")
    norm_sol = normalize_code(MOCK_CODE_SOLUTION)
    sol_ast = get_ast_structure(norm_sol)
    sol_complexity = get_cyclomatic_complexity(norm_sol)
    
    # 3. Compare Logic (AST)
    # 1.0 means identical structure, 0.0 means totally different
    ast_similarity = 1.0 if sub_ast == sol_ast else 0.0
    
    # 4. Compare Complexity
    # Calculate how close the complexity scores are
    complexity_diff = abs(sub_complexity - sol_complexity)
    complexity_similarity = max(0, (3 - complexity_diff) / 3) # Simple decay formula
    
    # 5. Calculate Final Score (Average of AST and Complexity)
    # High similarity = High Plagiarism
    overall_similarity = (ast_similarity + complexity_similarity) / 2
    
    return {
        "analysis_type": "code",
        "plagiarism_score": round(overall_similarity, 4), # 0 to 1 (1 is bad)
        "details": [
            {
                "metric": "AST Structure Match",
                "score": round(ast_similarity, 2),
                "explanation": "1.0 means the code logic structure is identical."
            },
            {
                "metric": "Cyclomatic Complexity Match",
                "score": round(complexity_similarity, 2),
                "explanation": f"Submission complexity: {sub_complexity}, Solution: {sol_complexity}"
            }
        ]
    }