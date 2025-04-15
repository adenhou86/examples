import streamlit as st
import pandas as pd
import numpy as np

# Set the page configuration
st.set_page_config(
    page_title="Company Fuzzy Search",
    layout="centered"
)

# Mock company database (replace with your actual database)
@st.cache_data
def load_company_data():
    data = {
        "companyTicker": [
            "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "JPM", "V", "JNJ",
            "WMT", "PG", "MA", "HD", "BAC", "DIS", "VZ", "ADBE", "NFLX", "CSCO",
            "INTC", "CRM", "PFE", "KO", "PEP"
        ],
        "companyName": [
            "Apple Inc.", "Microsoft Corporation", "Alphabet Inc.", "Amazon.com, Inc.", 
            "Meta Platforms, Inc.", "Tesla, Inc.", "NVIDIA Corporation", "JPMorgan Chase & Co.", 
            "Visa Inc.", "Johnson & Johnson", "Walmart Inc.", "Procter & Gamble Company", 
            "Mastercard Incorporated", "The Home Depot, Inc.", "Bank of America Corporation", 
            "The Walt Disney Company", "Verizon Communications Inc.", "Adobe Inc.", 
            "Netflix, Inc.", "Cisco Systems, Inc.", "Intel Corporation", "Salesforce, Inc.", 
            "Pfizer Inc.", "The Coca-Cola Company", "PepsiCo, Inc."
        ]
    }
    return pd.DataFrame(data)

# Function to calculate similarity between two strings
def calculate_similarity(str1, str2):
    # Convert both strings to lowercase for case-insensitive comparison
    a = str1.lower()
    b = str2.lower()
    
    if len(a) == 0 or len(b) == 0:
        return 0
    
    # Check if one string contains the other
    if a in b or b in a:
        return 0.8 + 0.2 * (min(len(a), len(b)) / max(len(a), len(b)))
    
    # Basic Levenshtein distance calculation
    matrix = np.zeros((len(a) + 1, len(b) + 1))
    
    # Initialize the matrix
    for i in range(len(a) + 1):
        matrix[i, 0] = i
    for j in range(len(b) + 1):
        matrix[0, j] = j
    
    # Fill the matrix
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = 0 if a[i-1] == b[j-1] else 1
            matrix[i, j] = min(
                matrix[i-1, j] + 1,      # deletion
                matrix[i, j-1] + 1,      # insertion
                matrix[i-1, j-1] + cost  # substitution
            )
    
    # Calculate similarity as 1 - normalized distance
    max_length = max(len(a), len(b))
    distance = matrix[len(a), len(b)]
    return 1 - distance / max_length

def main():
    # Page title
    st.title("Company Name Fuzzy Search")
    
    # Load the company data
    companies_df = load_company_data()
    
    # User input
    query = st.text_input("Enter Company Name:", placeholder="e.g. Apple")
    
    # Search logic
    if query and len(query.strip()) >= 2:
        # Calculate similarity scores
        companies_df['similarityScore'] = companies_df['companyName'].apply(
            lambda name: calculate_similarity(query, name)
        )
        
        # Sort by similarity score and take top 10
        results_df = companies_df.sort_values(by='similarityScore', ascending=False).head(10)
        
        # Display results
        if not results_df.empty:
            st.subheader("Top 10 Similar Companies:")
            
            # Format the similarity score as percentage
            results_df['Similarity'] = results_df['similarityScore'].apply(
                lambda score: f"{score * 100:.1f}%"
            )
            
            # Display the results in a table
            st.dataframe(
                results_df[['companyTicker', 'companyName', 'Similarity']],
                column_config={
                    'companyTicker': 'Ticker',
                    'companyName': 'Company Name',
                    'Similarity': 'Similarity'
                },
                hide_index=True
            )
        else:
            st.info("No matching companies found.")
    elif query:
        st.info("Please enter at least 2 characters.")

if __name__ == "__main__":
    main()
