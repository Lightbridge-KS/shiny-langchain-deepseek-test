

def extract_thinking(string: str):
    """
    Extract content from <think> tags, even if the closing tag isn't present yet (streaming case).
    
    Args:
        string: The input string that may contain <think> tags
        
    Returns:
        The content inside the <think> tags, or None if no tags are found
    """
    import re
    
    # Try to match complete <think> tags first
    complete_match = re.search(r"<think>\s*(.*?)\s*</think>", string, re.DOTALL)
    if complete_match:
        return complete_match.group(1)
    
    # If complete tags aren't found, check for partial (streaming) case
    last_think_pos = string.rfind("<think>")
    if last_think_pos != -1:
        # Extract everything after the last <think> tag (removing leading whitespace)
        return string[last_think_pos + len("<think>"):].lstrip()
    
    # No <think> tags found
    print(f"No <think> tags found in the input string.")
    return ""


def display_thinking(string: str):
    thinking = extract_thinking(string)
    return f"""**Thinking:**
<details>
    <summary>Toggle to expand</summary>
    {thinking}
</details>
"""


def extract_answer(string: str):
    """
    Extract the answer part that appears after the closing </think> tag.
    
    Args:
        string: The input string that may contain <think> tags
        
    Returns:
        The content after the </think> tag, or an empty string if no closing tag is found
    """
    # Find the position of the last closing </think> tag
    last_closing_tag_pos = string.rfind("</think>")
    
    if last_closing_tag_pos != -1:
        # Extract everything after the closing tag (removing leading whitespace)
        answer = string[last_closing_tag_pos + len("</think>"):].lstrip()
        return answer
    
    # If no closing tag is found, it means we're still in the thinking phase
    # or there are no think tags at all
    return ""


def display_message(string: str):
    thinking = extract_thinking(string)
    answer = extract_answer(string)
    return f"""<details>
    <summary>Reason</summary>
    {thinking}
</details>

---

{answer}
"""
