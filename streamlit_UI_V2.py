from langchain.vectorstores import BM25Vectorizer
from langchain.docstore.document import Document
import PyPDF2

# Step 1: Extract text from the PDF file
def extract_text_from_pdf(pdf_path):
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    pages_text = [page.extract_text() for page in pdf_reader.pages]
    return pages_text

# Step 2: Create LangChain documents for each page
def create_documents(pages_text):
    documents = [
        Document(page_content=page, metadata={"page_number": idx + 1})
        for idx, page in enumerate(pages_text)
    ]
    return documents

# Step 3: Perform similarity search using BM25
def bm25_search(reference_text, documents, top_n=2):
    vectorizer = BM25Vectorizer(documents)
    search_results = vectorizer.similarity_search_with_score(reference_text, k=top_n)
    return search_results

# Step 4: Generate output dictionary
def generate_output(company_name, search_results):
    result_dict = {
        company_name: {
            f"Page {doc.metadata['page_number']}": score
            for doc, score in search_results
        }
    }
    return result_dict

# Main process
def main(pdf_path, reference_text, company_name, top_n=2):
    # Extract text from the PDF
    pages_text = extract_text_from_pdf(pdf_path)
    
    # Create LangChain documents
    documents = create_documents(pages_text)
    
    # Perform BM25 search
    search_results = bm25_search(reference_text, documents, top_n)
    
    # Generate output dictionary
    output_dict = generate_output(company_name, search_results)
    
    return output_dict

# Define the reference text and company name
reference_text = """
Consolidated Statements of Cash Flows (Unaudited)

Operating Activities
Net income
Adjustments to reconcile net income to net cash used in operating activities:
Provision for credit losses
Depreciation and amortization
Deferred tax (benefit)/expense
Bargain purchase gain associated with the First Republic acquisition
Other
Originations and purchases of loans held-for-sale
Proceeds from sales, securitizations, and paydowns of loans held-for-sale
Net change in:
- Trading assets
- Securities borrowed
- Accrued interest and accounts receivable
- Other assets
- Trading liabilities
- Accounts payable and other liabilities
Other operating adjustments
Net cash (used in) operating activities
"""
company_name = "Example Company"

# Path to your PDF file
pdf_path = "10Q1_2024.pdf"

# Run the main process and print the output
output = main(pdf_path, reference_text, company_name, top_n=2)
print(output)
