import re


def extract_code(text):
    """Extract Python code from an LLM response.

    Priority:
    1. First fenced markdown python code block.
    2. Any fenced code block.
    3. Text region starting near `import pulp` or `pulp.LpProblem`.
    4. Original text as a last resort.
    """
    if text is None:
        return ""

    python_blocks = re.findall(r"```(?:python|py)\s*\n(.*?)```", text, flags=re.IGNORECASE | re.DOTALL)
    if python_blocks:
        return python_blocks[0].strip() + "\n"

    any_blocks = re.findall(r"```\s*\n(.*?)```", text, flags=re.DOTALL)
    if any_blocks:
        return any_blocks[0].strip() + "\n"

    markers = ["import pulp", "from pulp", "pulp.LpProblem"]
    starts = [text.find(marker) for marker in markers if text.find(marker) >= 0]
    if starts:
        start = min(starts)
        candidate = text[start:]
        stop_markers = ["\n# Explanation", "\nExplanation:", "\n```", "\nNotes:"]
        stop_positions = [candidate.find(marker) for marker in stop_markers if candidate.find(marker) > 0]
        if stop_positions:
            candidate = candidate[: min(stop_positions)]
        return candidate.strip() + "\n"

    return text.strip() + "\n"
