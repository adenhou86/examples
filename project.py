def parse_doc_answers(text):
    """
    Parse lines of the form:
      DOC_ID = 12345 | ANSWER: [Some answer text]
    into a list of dicts like:
      [{"doc_id": "12345", "answer": "[Some answer text]"}, ...]
    """
    # Split text by lines
    lines = text.strip().splitlines()
    
    results = []
    for line in lines:
        line = line.strip()
        if not line:
            continue  # skip any empty lines
        
        # Split at the '|' to separate DOC_ID part from ANSWER part
        doc_part, ans_part = line.split('|')
        
        # Extract the actual doc_id
        # doc_part should look like "DOC_ID = 41824151"
        # So we split by '=' and take the second part
        doc_id = doc_part.split('=')[1].strip()
        
        # Extract the answer
        # ans_part should look like "ANSWER: [New York]"
        # So we split by ':' and take the second part
        answer = ans_part.split(':', 1)[1].strip()
        
        # Append to results
        results.append({"doc_id": doc_id, "answer": answer})
    
    return results


# Example usage:
if __name__ == "__main__":
    sample_text = """DOC_ID = 41824151 | ANSWER: [NOT_FOUND]
DOC_ID = 41824217 | ANSWER: [New York]
DOC_ID = 41824299 | ANSWER: [The NDA is governed by the laws of the State of California.]
DOC_ID = 41824329 | ANSWER: [The NDA is governed by the laws of the State of New York.]"""

    parsed = parse_doc_answers(sample_text)
    print(parsed)
    # Output:
    # [
    #   {'doc_id': '41824151', 'answer': '[NOT_FOUND]'},
    #   {'doc_id': '41824217', 'answer': '[New York]'},
    #   {'doc_id': '41824299', 'answer': '[The NDA is governed by the laws of the State of California.]'},
    #   {'doc_id': '41824329', 'answer': '[The NDA is governed by the laws of the State of New York.]'}
    # ]
