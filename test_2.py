import re

def extract_amount(sentence):
    """
    Extracts the numerical amount from a given sentence.

    Parameters:
    sentence (str): The input string containing an amount.

    Returns:
    float: The extracted amount as a float.
    """
    match = re.search(r'\$([\d,]+(?:\.\d+)?)', sentence)
    if match:
        return float(match.group(1).replace(',', ''))
    return None

# Example usage
sentence = "The carrying value for Available-for-sale investment securities under fair value hedges as of March 31, 2024, is $18,981 million."
amount = extract_amount(sentence)

if amount:
    print(f"Extracted amount: {amount} million")
else:
    print("No amount found.")
