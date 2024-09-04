import re
def extract_email(text):
    # Regular expression pattern to match email addresses within angle brackets
    email_pattern = r'<(.*?)>'
    match = re.search(email_pattern, text)
    if match:
        return match.group(1)
    return text 