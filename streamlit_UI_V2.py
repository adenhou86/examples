import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Define the reference text for comparison
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
Investing Activities
Net change in:
- Federal funds sold and securities purchased under resale agreements
Held-to-maturity securities:
- Proceeds from paydowns and maturities
- Purchases
Available-for-sale securities:
- Proceeds from paydowns and maturities
- Proceeds from sales
- Purchases
Proceeds from sales and securitizations of loans held-for-investment
Other changes in loans, net
All other investing activities, net
Net cash provided by/(used in) investing activities
Financing Activities
Net change in:
- Deposits
- Federal funds purchased and securities loaned or sold under repurchase agreements
- Short-term borrowings
- Beneficial interests issued by consolidated VIEs
Proceeds from long-term borrowings
Payments of long-term borrowings
Proceeds from issuance of preferred stock
Treasury stock repurchased
Dividends paid
All other financing activities, net
Net cash provided by financing activities
Effect of exchange rate changes on cash and due from banks and deposits with banks
Net decrease in cash and due from banks and deposits with banks
Cash and due from banks and deposits with banks at the beginning of the period
Cash and due from banks and deposits with banks at the end of the period
Cash interest paid
Cash income taxes paid, net
"""

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    pages_text = [page.extract_text() for page in pdf_reader.pages]
    return pages_text

# Function to calculate similarity scores
def calculate_similarity(reference, pages_text):
    vectorizer = TfidfVectorizer()
    all_text = [reference] + pages_text
    tfidf_matrix = vectorizer.fit_transform(all_text)
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    return similarity_scores

# Main process
def find_most_similar_pages(pdf_path, reference_text, top_n=2):
    # Extract text from the PDF
    pages_text = extract_text_from_pdf(pdf_path)
    
    # Calculate similarity scores
    similarity_scores = calculate_similarity(reference_text, pages_text)
    
    # Find the top N most similar pages
    top_indices = similarity_scores.argsort()[-top_n:][::-1]
    
    # Return the top N pages and their scores
    return [(index, similarity_scores[index]) for index in top_indices]

# Path to the PDF file
pdf_path = "10Q1_2024.pdf"

# Find the top 2 most similar pages
top_pages = find_most_similar_pages(pdf_path, reference_text, top_n=2)

# Print the results
for index, score in top_pages:
    print(f"Page {index + 1} is similar with a score of {score:.4f}")
