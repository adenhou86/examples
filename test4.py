import ast
import re

def parse_string_to_dict(input_string):
    # Extract the question
    question_match = re.match(r"^(.*?)\?:\s*\[", input_string)
    question = question_match.group(1) if question_match else "Unknown Question"

    # Extract the list content
    list_content_match = re.search(r"\[(.*)\]", input_string, re.DOTALL)
    if not list_content_match:
        return {question: []}

    list_content = list_content_match.group(0)

    # Convert the list-like string to a Python object
    try:
        parsed_list = ast.literal_eval(list_content)
    except Exception as e:
        print(f"Error parsing string: {e}")
        return {question: []}

    return {question: parsed_list}

# Example input (Replace with the actual extracted string)
input_string = '''{'What is the client legal name?': [{'doc_id': '41824151', 'answer': '[NOT_FOUND]'}, {'doc_id': '41824217', 'answer': '[Eze Castle Software LLC]'}, ...]}'''

# Parsing the string
parsed_dict = parse_string_to_dict(input_string)

# Output the parsed dictionary
print(parsed_dict)
