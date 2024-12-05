from rank_bm25 import BM25Okapi
from langchain.docstore.document import Document
import PyPDF2

def extract_text_from_pdf(pdf_path):
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    pages_text = [page.extract_text() for page in pdf_reader.pages]
    return pages_text

def create_documents(pages_text):
    documents = [
        Document(page_content=page, metadata={"page_number": idx + 1})
        for idx, page in enumerate(pages_text)
    ]
    return documents

def bm25_search(reference_text, documents, top_n=2):
    # Tokenize documents
    tokenized_docs = [doc.page_content.lower().split() for doc in documents]
    
    # Create BM25 object
    bm25 = BM25Okapi(tokenized_docs)
    
    # Tokenize query
    tokenized_query = reference_text.lower().split()
    
    # Get document scores
    doc_scores = bm25.get_scores(tokenized_query)
    
    # Get indices of top N scores
    top_indices = sorted(range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True)[:top_n]
    
    # Create results list with documents and their scores
    results = [(documents[idx], float(doc_scores[idx])) for idx in top_indices]
    return results

def generate_output(company_name, search_results):
    result_dict = {
        company_name: {
            "matches": [
                {
                    "page_number": doc.metadata['page_number'],
                    "similarity_score": score,
                    "content_preview": doc.page_content[:200] + "..."
                }
                for doc, score in search_results
            ]
        }
    }
    return result_dict

def main(pdf_path, reference_text, company_name, top_n=2):
    pages_text = extract_text_from_pdf(pdf_path)
    documents = create_documents(pages_text)
    search_results = bm25_search(reference_text, documents, top_n)
    output_dict = generate_output(company_name, search_results)
    return output_dict
