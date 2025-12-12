import re
from difflib import SequenceMatcher

# ---------------------------------------------------
# 1. NORMALIZATION
# ---------------------------------------------------

def remove_comments(code: str) -> str:
    # Remove single-line comments
    code = re.sub(r"#.*", "", code)
    # Remove multiline comments """ ... """ or ''' ... '''
    code = re.sub(r'""".*?"""', "", code, flags=re.DOTALL)
    code = re.sub(r"'''.*?'''", "", code, flags=re.DOTALL)
    return code


def normalize_variables(code: str) -> str:
    """
    Replace variable names with <VAR>.
    Variables = alphabetic sequences (excluding keywords)
    """
    python_keywords = {
        "def", "class", "return", "if", "else", "for", "while", "import",
        "from", "as", "try", "except", "finally", "with", "lambda", "pass",
        "break", "continue", "True", "False", "None"
    }

    def repl(match):
        word = match.group(0)
        if word in python_keywords:
            return word
        return "<VAR>"

    # Replace all alphanumeric identifiers
    return re.sub(r"[A-Za-z_][A-Za-z0-9_]*", repl, code)


def normalize_numbers(code: str) -> str:
    # Replace numbers with <NUM>
    return re.sub(r"\b\d+(\.\d+)?\b", "<NUM>", code)


def normalize_code(code: str) -> list:
    """
    Produces a normalized list of code lines.
    """
    code = remove_comments(code)
    code = normalize_variables(code)
    code = normalize_numbers(code)

    # Trim whitespace & ignore empty lines
    lines = [
        line.strip()
        for line in code.splitlines()
        if line.strip()
    ]

    return lines


# ---------------------------------------------------
# 2. SIMILARITY METRICS
# ---------------------------------------------------

def jaccard_similarity(a: str, b: str) -> float:
    set_a = set(a.split())
    set_b = set(b.split())
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def levenshtein_similarity(a: str, b: str) -> float:
    seq = SequenceMatcher(None, a, b)
    return seq.ratio()


def combined_line_similarity(a: str, b: str) -> float:
    """
    Combines 2 similarity methods.
    """
    return (jaccard_similarity(a, b) + levenshtein_similarity(a, b)) / 2


# ---------------------------------------------------
# 3. BLOCK MATCHING DETECTION
# ---------------------------------------------------

def detect_matching_blocks(code_a: list, code_b: list, min_block=3):
    """
    Detects matching sequences of lines.
    """
    matches = []
    i = 0

    while i < len(code_a):
        block = []
        j = 0

        while j < len(code_b):
            if combined_line_similarity(code_a[i], code_b[j]) > 0.85:
                block.append((i, j))
                i += 1
                j += 1

                if i >= len(code_a) or j >= len(code_b):
                    break
            else:
                j += 1

        if len(block) >= min_block:
            matches.append(block)

        i += 1

    return matches


# ---------------------------------------------------
# 4. MAIN DRIVER FOR SYSTEM
# ---------------------------------------------------

def compute_code_plagiarism(code_a: str, code_b: str) -> dict:
    """
    Compare two source code files using normalized line matching.
    """

    norm_a = normalize_code(code_a)
    norm_b = normalize_code(code_b)

    blocks = detect_matching_blocks(norm_a, norm_b)

    matched_lines = sum(len(b) for b in blocks)
    total_lines = max(len(norm_a), 1)

    plagiarism_score = round((matched_lines / total_lines) * 100, 2)

    return {
        "matched_blocks": blocks,
        "matched_lines": matched_lines,
        "total_lines": total_lines,
        "plagiarism_score": plagiarism_score,
    }
