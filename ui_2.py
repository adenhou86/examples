import streamlit as st
import pandas as pd
import numpy as np
from functools import lru_cache
import time

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
    df = pd.DataFrame(data)
    # Pre-compute lowercase names to avoid repeated conversions
    df['lowercaseName'] = df['companyName'].str.lower()
    return df

# Calculate similarity function - use caching for significant speed improvement
@lru_cache(maxsize=10000)
def calculate_similarity(str1, str2):
    # Convert both strings to lowercase for case-insensitive comparison
    a = str1.lower()
    b = str2.lower()
    
    if len(a) == 0 or len(b) == 0:
        return 0
    
    # Check if one string contains the other
    if a in b or b in a:
        return 0.8 + 0.2 * (min(len(a), len(b)) / max(len(a), len(b)))
    
    # Basic Levenshtein distance calculation but with optimization
    m, n = len(a), len(b)
    
    # For large strings, use only two rows to save memory
    # This dramatically reduces memory usage for long strings
    current_row = range(n+1)
    for i in range(1, m+1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n+1):
            add, delete, change = previous_row[j] + 1, current_row[j-1] + 1, previous_row[j-1]
            if a[i-1] != b[j-1]:
                change += 1
            current_row[j] = min(add, delete, change)
    
    # Calculate similarity as 1 - normalized distance
    max_length = max(m, n)
    distance = current_row[n]
    return 1 - distance / max_length

def main():
    # Page title
    st.title("Company Name Fuzzy Search")
    
    # Load the company data
    companies_df = load_company_data()
    
    # Create columns for layout
    col1, col2 = st.columns([3, 1])
    
    # User input
    with col1:
        query = st.text_input("Enter Company Name:", placeholder="e.g. Apple")
    
    with col2:
        min_chars = st.number_input("Min. chars:", min_value=1, max_value=5, value=2)
    
    # Initialize timing variables in session state
    if 'search_time' not in st.session_state:
        st.session_state.search_time = 0
    
    # Search logic
    if query and len(query.strip()) >= min_chars:
        with st.status("Processing...", expanded=False) as status:
            start_time = time.time()
            
            # Quick pre-filter to find potential matches to reduce the number of full calculations
            query_lower = query.lower()
            
            # 1. First find exact matches in lowercase
            mask_exact = companies_df['lowercaseName'] == query_lower
            exact_matches = companies_df[mask_exact].copy()
            
            # 2. Then find companies that start with the query
            mask_prefix = companies_df['lowercaseName'].str.startswith(query_lower)
            prefix_matches = companies_df[mask_prefix & ~mask_exact].copy()
            
            # 3. Then find companies that contain the query
            mask_contains = companies_df['lowercaseName'].str.contains(query_lower)
            contains_matches = companies_df[mask_contains & ~mask_prefix & ~mask_exact].copy()
            
            # 4. For the rest, calculate full similarity but limit to a reasonable number
            remaining = companies_df[~mask_contains & ~mask_prefix & ~mask_exact]
            
            # Assign similarity scores
            if not exact_matches.empty:
                exact_matches['similarityScore'] = 1.0
                
            if not prefix_matches.empty:
                prefix_matches['similarityScore'] = prefix_matches['companyName'].apply(
                    lambda name: 0.9 + 0.1 * (len(query) / len(name))
                )
                
            if not contains_matches.empty:
                contains_matches['similarityScore'] = contains_matches['companyName'].apply(
                    lambda name: calculate_similarity(query, name)
                )
            
            # Calculate full similarity only for a limited number of remaining companies
            sample_size = min(100, len(remaining))
            if sample_size > 0:
                # Sample to avoid calculating for all companies
                sampled_remaining = remaining.sample(sample_size)
                sampled_remaining['similarityScore'] = sampled_remaining['companyName'].apply(
                    lambda name: calculate_similarity(query, name)
                )
                # Filter out low similarity scores
                sampled_remaining = sampled_remaining[sampled_remaining['similarityScore'] > 0.5]
            else:
                sampled_remaining = pd.DataFrame()
            
            # Combine all results
            all_results = pd.concat([exact_matches, prefix_matches, contains_matches, sampled_remaining])
            
            # Sort by similarity score and take top 10
            results_df = all_results.sort_values(by='similarityScore', ascending=False).head(10)
            
            # Calculate and store processing time
            end_time = time.time()
            st.session_state.search_time = end_time - start_time
            
            status.update(label=f"Processing complete! ({st.session_state.search_time:.3f}s)", state="complete")
            
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
    
    # Performance info
    if st.session_state.search_time > 0:
        st.sidebar.subheader("Performance Info")
        st.sidebar.text(f"Search time: {st.session_state.search_time:.3f}s")
        st.sidebar.text(f"Cache entries: {calculate_similarity.cache_info().currsize}")
        st.sidebar.markdown("""
        **Optimizations:**
        - Multi-tier search approach
        - Function result caching
        - Optimized Levenshtein algorithm
        - Pre-filtering with exact/prefix/contains
        - Limited full similarity calculations
        """)

if __name__ == "__main__":
    main()
