import streamlit as st
import pandas as pd
import numpy as np
from functools import lru_cache
from rapidfuzz import fuzz

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

# Use RapidFuzz for much faster string similarity calculation
# Cache results to avoid recalculating for the same strings
@lru_cache(maxsize=1024)
def calculate_similarity_fast(str1, str2):
    # Convert both strings to lowercase for case-insensitive comparison
    a = str1.lower()
    b = str2.lower()
    
    if len(a) == 0 or len(b) == 0:
        return 0
    
    # Check if one string contains the other
    if a in b or b in a:
        return 0.9 + 0.1 * (min(len(a), len(b)) / max(len(a), len(b)))
    
    # Use RapidFuzz for much faster similarity calculation
    # Returns ratio between 0 and 100, so we divide by 100
    return fuzz.ratio(a, b) / 100

def main():
    # Page title
    st.title("Company Name Fuzzy Search")
    
    # Add a note about installation requirements
    st.caption("Note: This app requires the rapidfuzz library: `pip install rapidfuzz`")
    
    # Load the company data
    companies_df = load_company_data()
    
    # Create columns for layout
    col1, col2 = st.columns([3, 1])
    
    # User input with callback
    with col1:
        query = st.text_input("Enter Company Name:", placeholder="e.g. Apple")
    
    with col2:
        min_chars = st.number_input("Min. chars:", min_value=1, max_value=5, value=2)
    
    # Add processing status indicator
    if query and len(query.strip()) >= min_chars:
        with st.status("Processing...", expanded=False) as status:
            # Vectorized calculation for better performance
            # Pre-compute lowercase company names to avoid repeated conversions
            lowercase_names = companies_df['companyName'].str.lower()
            lowercase_query = query.lower()
            
            # First quick filter for exact substring matches
            mask = lowercase_names.str.contains(lowercase_query)
            quick_matches = companies_df[mask].copy()
            
            # For remaining companies, calculate similarity scores
            remaining = companies_df[~mask].copy()
            
            if not remaining.empty:
                # Calculate scores using vectorized operations where possible
                remaining['similarityScore'] = remaining['companyName'].apply(
                    lambda name: calculate_similarity_fast(query, name)
                )
                
                # Combine both result sets
                if not quick_matches.empty:
                    quick_matches['similarityScore'] = 0.95  # High score for substring matches
                    combined_results = pd.concat([quick_matches, remaining])
                else:
                    combined_results = remaining
                
                # Sort by similarity score and take top 10
                results_df = combined_results.sort_values(by='similarityScore', ascending=False).head(10)
            else:
                quick_matches['similarityScore'] = 0.95  # High score for substring matches
                results_df = quick_matches.head(10)
            
            status.update(label="Processing complete!", state="complete")
            
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
                    hide_index=True,
                    use_container_width=True
                )
            else:
                st.info("No matching companies found.")
    elif query:
        st.info(f"Please enter at least {min_chars} characters.")

if __name__ == "__main__":
    main()
