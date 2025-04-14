import streamlit as st
import json
import openai

# Replace with your OpenAI API key or set it as an environment variable
openai.api_key = "YOUR_OPENAI_API_KEY_HERE"

# The prompt instructing the LLM how to decompose the query, now with camel case keys.
LLM_PROMPT = """
You are a financial research assistant tasked with interpreting user queries about financial news and filings from a knowledge database of 20 million documents. The documents are categorized by newsSources and subcategories (NewsTypeNames). Your goal is to decompose the user query to infer metadata, including which combination of newsSources and NewsTypeNames to query, along with companyName, datePeriod (combining year and asOfDateOfTheDocument), industrySectorOfTheCompany, and keyTopics, to narrow down the document set for retrieval. Output the inferred metadata as a JSON object, using lists for values that represent multiple selections (e.g., ["EDGAR", "Refinitiv"] for newsSources). Additionally, provide an explanation section detailing the reasoning behind each metadata field. If no inference is possible, leave the field as an empty list or empty string as appropriate.

Today’s date is March 27, 2025. Use this to infer the most recent or relevant timeframes for documents (e.g., default to the latest year like 2024 or Q4 2024 unless otherwise specified).

The available newsSources and NewsTypeNames, along with detailed descriptions, are:

- **newsSources**:
  - **Fitch Ratings**: A global credit rating agency that provides credit ratings, commentary, and research on companies, governments, and financial instruments. It focuses on assessing credit risk and financial stability, often used by investors to evaluate the creditworthiness of issuers.
    - **Rating Report**: A standard report providing an overview of a company’s current credit rating, including the rating score, outlook, and key factors influencing the rating.
    - **Affirmation**: A report confirming that a company’s existing credit rating remains unchanged.
    - **Downgrade**: A report announcing a reduction in a company’s credit rating.
    - **New Issue Report**: A detailed analysis of a new debt issuance or financial instrument.
    - **New Issue**: A brief announcement of a new security issuance.
    - **Presale Report**: A pre-issuance analysis of a new financial instrument.
    - **Full Rating Report**: A comprehensive report covering a company’s entire credit rating history.
  - **SnP**: S&P Global Ratings, focusing on credit ratings, research updates, and in-depth analyses.
    - **Research Update**: A report providing recent updates on a company’s financial outlook.
    - **Rating Action**: A report detailing a specific change in a company’s credit rating.
    - **Full Analysis**: An in-depth report analyzing a company’s overall financial health.
    - **New Issue Report**: A detailed analysis for new debt issuances.
  - **Moodys**: Moody’s Investors Service, providing ratings, research, and risk analysis.
    - **Rating Action**: A report about a change in a company’s credit rating.
    - **Credit Opinion**: A report providing an opinion on a company’s creditworthiness.
    - **Pre-Sale Report**: A pre-issuance analysis of a new financial instrument.
    - **New Issue Report**: A detailed analysis of a new debt issuance.
    - **Issuer In-Depth**: A comprehensive report on a company’s financial health.
  - **EDGAR**: The SEC’s system containing official filings like annual and quarterly reports.
    - **Filing10K**: An annual report providing a comprehensive overview of financial performance.
    - **Filing10KA**: An amended annual report.
    - **Filing10Q**: A quarterly report with interim financial statements.
    - **Filing10QA**: An amended quarterly report.
  - **Refinitiv**: A financial data provider focused on executive statements and conference calls.
    - **Earning Conference Call**: A transcript or summary of a company’s earnings call.
  - **DbrsMorningstar**: Provides ratings and research for credit risk assessment.
    - **Rating Action**: A report detailing a change in a company’s credit rating.
    - **Upgrade**: A report announcing an increase in a company’s credit rating.

User Query: {user_query}

Instructions:
1. Identify the company or companies mentioned (companyName). If multiple companies are mentioned, list them (e.g., "Apple, Microsoft"). If the query is about a sector trend, leave as an empty string.
2. Infer the relevant date period (datePeriod), which includes:
   - year: The relevant year or range of years (use a list for ranges or sets, e.g., ["2023", "2024"]).
   - asOfDateOfTheDocument: The specific date or quarter if mentioned (use a list if multiple dates are implied). Default to current trends (e.g., 2024) unless specified.
3. Infer the industry sector if clear (industrySectorOfTheCompany, e.g., "Technology", "Energy"). For sector trends, specify the sector; for multiple companies, use the shared sector if applicable.
4. Determine the relevant newsSources and NewsTypeNames to query based on the query’s intent and the detailed descriptions:
   - Choose Fitch Ratings for credit ratings, stability, or new issuances.
   - Choose SnP for credit ratings, research updates, or comprehensive analyses.
   - Choose Moodys for credit opinions, rating actions, or issuer profiles.
   - Choose EDGAR for financial performance or regulatory disclosures.
   - Choose Refinitiv for earnings discussions or executive statements.
   - Choose DbrsMorningstar for rating changes or upgrades.
5. Extract key topics (keyTopics) from the query (e.g., "revenue", "merger").
6. If the query involves multiple types of information, select multiple newsSources and corresponding NewsTypeNames.
7. Be conservative—only infer metadata explicitly supported by the query or common financial patterns. If unsupported, leave the fields empty.
8. Provide an explanation section detailing your reasoning for each metadata field.

Output the result in the following JSON format:
{
  "metadata": {
    "companyName": "",
    "datePeriod": {
      "year": [],
      "asOfDateOfTheDocument": []
    },
    "industrySectorOfTheCompany": "",
    "newsSources": [],
    "newsTypeNames": [],
    "keyTopics": []
  },
  "explanation": {
    "companyName": "",
    "datePeriod": {
      "year": "",
      "asOfDateOfTheDocument": ""
    },
    "industrySectorOfTheCompany": "",
    "newsSources": "",
    "newsTypeNames": "",
    "keyTopics": ""
  }
}
"""

def decompose_query(user_query):
    """
    This function sends the user's query along with the prompt to the LLM to infer metadata.
    It returns the JSON result with camelCase keys.
    """
    # Format the prompt with the user input
    formatted_prompt = LLM_PROMPT.format(user_query=user_query)
    
    try:
        # Call the LLM (here we use the ChatCompletion API as an example)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": formatted_prompt}],
            temperature=0.0
        )
        answer = response.choices[0].message.content.strip()
        
        # Try parsing the output as JSON
        result = json.loads(answer)
    except Exception as e:
        st.error(f"Error processing the query: {e}")
        result = {}
    return result

def main():
    st.title("Financial Query Decomposition")
    st.write("Enter a financial query and get the decomposed metadata.")

    user_query = st.text_area("Enter your query:")

    if st.button("Decompose Query"):
        if user_query.strip():
            with st.spinner("Processing your query..."):
                metadata_result = decompose_query(user_query)
            st.subheader("Inferred Metadata")
            st.json(metadata_result)
        else:
            st.warning("Please enter a query.")

if __name__ == "__main__":
    main()
