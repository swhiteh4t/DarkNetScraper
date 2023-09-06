import re
import chardet

def parse_depth(s):
    if is_digits(s):
        return int(s)
    else:
        return 1
    
def is_digits(input_string):
    for char in input_string:
        if not char.isdigit():
            return False
    return True 

def only_alphanum(s):
    """
    Removes non-alphanumeric characters from a given string.

    Parameters:
    s (str): The input string from which non-alphanumeric characters will be removed.

    Returns:
    str: A new string containing only alphanumeric characters from the input string.
    """
    return ''.join(c for c in s if c.isalnum())

def remove_non_alphanumeric(s: str) -> str:
    # Use regular expression to match all non-alphanumeric characters and replace them with an empty string
    cleaned_string = re.sub(r'[^a-zA-Z0-9\s]', '', s)
    return cleaned_string.replace("\n","")

def detect_encoding(byte):
    detector = chardet.universaldetector.UniversalDetector()
    for line in byte:
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    return detector.result

def decode_string(byte):
    encoding = detect_encoding(byte)
    return byte.decode(encoding)
