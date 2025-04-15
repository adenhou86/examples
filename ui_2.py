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

# Cache for similarity calculations to improve performance
similarity_cache = {}

# Mock company database (replace with your actual database)
@st.cache_data
def load_company_data():
    data = {
        "companyId": [
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
            "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
            "21", "22", "23", "24", "25", "26", "27"
        ],
        "companyName": [
            "Apple Inc.", "Microsoft Corporation", "Alphabet Inc.", "Amazon.com, Inc.", 
            "Meta Platforms, Inc.", "Tesla, Inc.", "NVIDIA Corporation", "JPMorgan Chase & Co.", 
            "Visa Inc.", "Johnson & Johnson", "Walmart Inc.", "Procter & Gamble Company", 
            "Mastercard Incorporated", "The Home Depot, Inc.", "Bank of America Corporation", 
            "The Walt Disney Company", "Verizon Communications Inc.", "Adobe Inc.", 
            "Netflix, Inc.", "Cisco Systems, Inc.", "Intel Corporation", "Salesforce, Inc.", 
            "Pfizer Inc.", "The Coca-Cola Company", "PepsiCo, Inc.", 
            "USAA Auto Owner Trust 2023-A", "USAA 2023-B Auto Owner Trust"
        ]
    }
    
    df = pd.DataFrame(data)
    # Pre-compute lowercase names to avoid repeated conversions
    df['lowercaseName'] = df['companyName'].str.lower()
    return df

# Optimized similarity calculation function with caching
@lru_cache(maxsize=10000)
def calculate_similarity(str1, str2):
    # Convert both strings to lowercase for case-insensitive comparison
    a = str1.lower()
    b = str2.lower()
    
    if len(a) == 0 or len(b) == 0:
        return 0
    
    # Quick check for exact match
    if a == b:
        return 1.0
    
    # Special case: Check if string a is a prefix/beginning of string b
    # This handles cases like "USAA" vs "USAA Auto Owner Trust"
    if b.startswith(a):
        # Higher score for prefix matches - length ratio affects the score
        return 0.95 + 0.05 * (len(a) / len(b))
    
    # Check for word-by-word prefix match
    words1 = a.split()
    words2 = b.split()
    
    # If the first words match exactly, it's likely related
    if len(words1) >= 1 and len(words2) >= 1 and words2[0] == words1[0]:
        # Calculate how many consecutive words match
        matching_words = 0
        for i in range(min(len(words1), len(words2))):
            if words1[i] == words2[i]:
                matching_words += 1
            else:
                break
        
        if matching_words > 0:
            # Score based on matching words and word coverage
            word_match_ratio = matching_words / len(words1)
            return 0.85 + 0.15 * word_match_ratio
    
    # Check if one string contains the other
    if a in b or b in a:
        return 0.8 + 0.2 * (min(len(a), len(b)) / max(len(a), len(b)))
    
    # Basic Levenshtein distance calculation for remaining cases
    # Using a windowed approach for better performance
    max_len = max(len(a), len(b))
    matrix = np.zeros((len(a) + 1, len(b) + 1))
    
    # Initialize the matrix
    for i in range(len(a) + 1):
        matrix[i, 0] = i
    for j in range(len(b) + 1):
        matrix[0, j] = j
    
    # Fill the matrix with a windowed approach
    window_size = min(10, max_len)  # Limit calculation to a window for performance
    
    for i in range(1, len(a) + 1):
        j_start = max(1, i - window_size)
        j_end = min(len(b) + 1, i + window_size)
        
        for j in range(j_start, j_end):
            cost = 0 if a[i-1] == b[j-1] else 1
            matrix[i, j] = min(
                matrix[i-1, j] + 1,      # deletion
                matrix[i, j-1] + 1,      # insertion
                matrix[i-1, j-1] + cost  # substitution
            )
    
    # Calculate similarity as 1 - normalized distance
    distance = matrix[len(a), len(b)]
    return 1 - distance / max_len

def search_companies(query, companies_df, min_chars=2):
    """Optimized search function with multi-tier matching strategy"""
    if not query or len(query.strip()) < min_chars:
        return pd.DataFrame()
    
    start_time = time.time()
    query_lower = query.lower()
    results = pd.DataFrame()
    
    # Step 1: Look for exact prefix matches
    prefix_matches = companies_df[
        (companies_df['lowercaseName'].str.startswith(query_lower)) |
        (companies_df['lowercaseName'].apply(
            lambda name: all(
                name.split()[i] == query_lower.split()[i] 
                for i in range(min(len(query_lower.split()), len(name.split())))
                if len(query_lower.split()) <= len(name.split())
            )
        ))
    ].copy()
    
    if not prefix_matches.empty:
        prefix_matches['similarityScore'] = 0.98  # Highest score for prefix matches
        
    # Step 2: Regular substring matches (exclude companies already matched)
    already_matched = set(prefix_matches.index) if not prefix_matches.empty else set()
    
    substring_matches = companies_df[
        ~companies_df.index.isin(already_matched) & 
        companies_df['lowercaseName'].str.contains(query_lower)
    ].copy()
    
    if not substring_matches.empty:
        substring_matches['similarityScore'] = 0.9  # High score for substring matches
        
    # Step 3: Calculate similarity for remaining companies
    remaining_df = companies_df[
        ~companies_df.index.isin(already_matched) & 
        ~companies_df.index.isin(set(substring_matches.index) if not substring_matches.empty else set())
    ]
    
    # Only calculate similarity for a reasonable number of companies
    # This helps with performance for large databases
    if not remaining_df.empty:
        remaining_df = remaining_df.sample(min(500, len(remaining_df)))
        remaining_df['similarityScore'] = remaining_df['companyName'].apply(
            lambda name: calculate_similarity(query, name)
        )
        # Filter for reasonable similarity
        remaining_df = remaining_df[remaining_df['similarityScore'] > 0.6]
    
    # Combine all results
    combined_results = pd.concat([prefix_matches, substring_matches, remaining_df])
    
    # Sort by similarity score and take top 10
    results = combined_results.sort_values(by='similarityScore', ascending=False).head(10)
    
    # Format the similarity score as percentage
    if not results.empty:
        results['Similarity'] = results['similarityScore'].apply(
            lambda score: f"{score * 100:.1f}%"
        )
    
    # For logging/debug only
    process_time = time.time() - start_time
    st.session_state['process_time'] = process_time
    st.session_state['cache_size'] = len(similarity_cache)
    
    return results

def main():
    # Page title and style
    st.title("Company Name Fuzzy Search")
    
    # Initialize session state for storing processing info
    if 'process_time' not in st.session_state:
        st.session_state['process_time'] = 0
    if 'cache_size' not in st.session_state:
        st.session_state['cache_size'] = 0
    
    # Load the company data
    companies_df = load_company_data()
    
    # Create columns for layout
    col1, col2 = st.columns([3, 1])
    
    # User input with callback
    with col1:
        query = st.text_input("Enter Company Name:", placeholder="e.g. USAA 2023")
    
    with col2:
        min_chars = st.number_input("Min. chars:", min_value=1, max_value=5, value=2)
    
    # Search logic
    if query and len(query.strip()) >= min_chars:
        with st.status("Processing...", expanded=False) as status:
            # Search companies
            results_df = search_companies(query, companies_df, min_chars)
            
            status.update(label=f"Processing complete! ({st.session_state['process_time']:.3f}s)", state="complete")
            
            # Display results
            if not results_df.empty:
                st.subheader("Top 10 Similar Companies:")
                
                # Display the results in a table
                st.dataframe(
                    results_df[['companyId', 'companyName', 'Similarity']],
                    column_config={
                        'companyId': 'Company ID',
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
    if st.session_state['process_time'] > 0:
        st.sidebar.subheader("Performance Info")
        st.sidebar.text(f"Last processing time: {st.session_state['process_time']:.3f}s")
        st.sidebar.text(f"Cache entries: {st.session_state['cache_size']}")
        st.sidebar.markdown("""
        **Optimizations:**
        - Multi-tier matching strategy
        - Prefix matching prioritization
        - Similarity calculation caching
        - Windowed Levenshtein distance
        - Pre-indexed lowercase names
        """)

if __name__ == "__main__":
    main()
