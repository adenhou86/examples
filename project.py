
---

### **🚀 FINAL UPDATED RAG_PROMPT (Auto-Detect Concise vs. Detailed)**
```python
TEMPLATE_OPENAI: str = """
CONTEXTS: {context}

QUESTION: {question}

### **Instructions:**
- Use only the provided context to answer the question. **Do not use external knowledge.**
- **Ensure the response is always valid JSON.**
- **Use double quotes (`"`) for all JSON keys and values.** Never use single quotes (`'`).
- **Adjust the response length based on the question's intent:**
  - If the question is **fact-based or numerical**, return a **short and direct answer**.
  - If the question asks for **explanation, analysis, or breakdown**, provide a **detailed and structured response**.
  - **For some questions, and if the user did not specify a preference for detail or conciseness, assess independently** whether a **concise or detailed** response is more appropriate based on the complexity of the question.
  - If unsure, **default to a detailed response** to ensure completeness.
- **Always include citations** from the context using the `"Citations"` field.

### **Expected JSON Output Format:**
```json
{
  "Answer": "Your answer here, matching the required level of detail.",
  "Citations": [
    {"page_no": "12", "excerpt": "Exact text excerpt from the document"},
    {"page_no": "3", "excerpt": "Another relevant excerpt"}
  ]
}
