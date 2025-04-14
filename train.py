import streamlit as st
import json
import openai

# Replace with your OpenAI API key or set it as an environment variable
openai.api_key = "YOUR_OPENAI_API_KEY_HERE"

# The prompt instructing the LLM how to decompose the query, now with camel case keys.
LLM_PROMPT = """
You are a financial research assistant tasked with interpreting user queries about financial news and filings from a knowledge database of 20 million documents. The documents are categorized by newsSources and subcategories (NewsTypeNames). Your goal is to decompose the user query to infer metadata, including which combination of newsSources and NewsTypeNames to query, along with companyName, datePeriod (combining year and asOfDateOfTheDocument), industrySectorOfTheCompany, and keyTopics, to narrow down the document set for retrieval. Output the inferred metadata as a JSON object, using lists for values that represent multiple selections (e.g., ["EDGAR", "Refinitiv"] for newsSources). Additionally, provide an explanation section detailing the reasoning behind each metadata field. If no inference is possible, leave the field as an empty list or empty string as appropriate.

- companyName: A list of strings representing the company or companies mentioned in the query (e.g., ["Apple", "Microsoft"]). If no companies are specified, leave as an empty list (e.g., []).
- industrySectorOfTheCompany: A list of strings representing the industry sector or sectors relevant to the query (e.g., ["Technology", "Retail"]). If no specific sector is specified, leave as an empty list (e.g., []).

Today’s date is March 27, 2025. Use this to infer the most recent or relevant timeframes for documents (e.g., default to the latest year like 2024 or Q4 2024 unless otherwise specified).

The available newsSources and NewsTypeNames, along with detailed descriptions, are:

- **newsSources**:
  - **Fitch Ratings**: A global credit rating agency that provides credit ratings, commentary, and research on companies, governments, and financial instruments. It focuses on assessing credit risk and financial stability, often used by investors to evaluate the creditworthiness of issuers.
    - **Rating Report**: A standard report providing an overview of a company’s current credit rating, including the rating score, outlook, and key factors influencing the rating (e.g., "What is Apple’s current credit rating from Fitch?").
    - **Affirmation**: A report confirming that a company’s existing credit rating remains unchanged, often issued after a review with no significant changes in financial health (e.g., "Did Fitch affirm Apple’s rating?").
    - **Downgrade**: A report announcing a reduction in a company’s credit rating, typically due to deteriorating financial conditions or increased risk (e.g., "Was Apple downgraded by Fitch?").
    - **New Issue Report**: A detailed analysis of a new debt issuance or financial instrument, including its credit rating and risk factors (e.g., "What’s Fitch’s rating on Apple’s new bonds?").
    - **New Issue**: A brief announcement of a new security issuance, focusing on the issuance details and initial rating (e.g., "What new securities did Apple issue according to Fitch?").
    - **Presale Report**: A pre-issuance analysis of a new financial instrument, providing insights into its potential credit rating and risks before it’s sold (e.g., "What’s the presale analysis for Apple’s new bonds from Fitch?").
    - **Full Rating Report**: A comprehensive report covering a company’s entire credit rating history, including all past ratings, changes, and detailed rationale (e.g., "What’s Apple’s full credit rating history from Fitch?").
  - **SnP**: S&P Global Ratings, a leading provider of credit ratings, research, and risk analysis, focusing on the creditworthiness of companies and financial instruments, often used for investment decisions and market analysis.
    - **Research Update**: A report providing recent updates on a company’s financial outlook, including changes in credit risk, market conditions, or operational performance (e.g., "What’s the latest research update on Apple from SnP?").
    - **Rating Action**: A report detailing a specific change in a company’s credit rating, such as an upgrade, downgrade, or outlook change (e.g., "Did SnP change Apple’s rating?").
    - **Full Analysis**: An in-depth report analyzing a company’s overall financial health, credit rating rationale, and long-term risk factors (e.g., "What’s SnP’s full analysis of Apple?").
    - **New Issue Report**: A detailed analysis of a new debt issuance or financial instrument, including its credit rating and associated risks (e.g., "What new bonds did Apple issue according to SnP?").
  - **Moodys**: Moody’s Investors Service, a credit rating agency providing ratings, research, and risk analysis, focusing on the creditworthiness of issuers and financial instruments, often used for debt market insights.
    - **Rating Action**: A report announcing a specific change in a company’s credit rating, such as an upgrade, downgrade, or outlook change (e.g., "Did Moodys change Apple’s rating?").
    - **Credit Opinion**: A report providing an opinion on a company’s creditworthiness, including key financial metrics, risks, and outlook (e.g., "What’s Moodys’ credit opinion on Apple?").
    - **Pre-Sale Report**: A pre-issuance analysis of a new financial instrument, offering insights into its potential credit rating and risks (e.g., "What’s the pre-sale report for Apple’s new bonds from Moodys?").
    - **New Issue Report**: A detailed analysis of a new debt issuance or financial instrument, including its credit rating and risk factors (e.g., "What new bonds did Apple issue according to Moodys?").
    - **Issuer In-Depth**: A comprehensive report on a company’s financial health, credit profile, and long-term risks, often used for deep dives into an issuer’s stability (e.g., "What’s Moodys’ in-depth report on Apple?").
  - **EDGAR**: The Electronic Data Gathering, Analysis, and Retrieval system by the SEC, containing official filings from public companies, such as annual and quarterly reports, used for regulatory and financial performance analysis.
    - **Filing10K**: An annual report filed by public companies, providing a comprehensive overview of financial performance, business operations, risk factors, and management discussions for the fiscal year (e.g., "What’s Apple’s annual revenue?").
    - **Filing10KA**: An amended annual report, filed to correct or update information in the original 10-K filing (e.g., "What corrections were made to Apple’s 10-K?").
    - **Filing10Q**: A quarterly report filed by public companies, providing interim financial statements, management discussions, and updates on business operations for a three-month period (e.g., "What’s Apple’s Q2 revenue?").
    - **Filing10QA**: An amended quarterly report, filed to correct or update information in the original 10-Q filing (e.g., "What corrections were made to Apple’s Q2 10-Q?").
  - **Refinitiv**: A financial data provider offering insights from earnings conference calls, focusing on executive statements and earnings discussions, often used for real-time market insights.
    - **Earning Conference Call**: A transcript or summary of a company’s earnings conference call, including executive statements, financial results, and forward-looking guidance (e.g., "What did Apple say in their earnings call?").
  - **DbrsMorningstar**: DBRS Morningstar, a credit rating agency providing ratings and research, focusing on credit risk and rating changes, often used for assessing issuer stability.
    - **Rating Action**: A report detailing a specific change in a company’s credit rating, such as an upgrade or downgrade (e.g., "Did DbrsMorningstar change Apple’s rating?").
    - **Upgrade**: A report announcing an increase in a company’s credit rating, typically due to improved financial conditions or reduced risk (e.g., "Was Apple upgraded by DbrsMorningstar?").

User Query: [Insert User Query Here]

Instructions:
1. Identify the company or companies mentioned (companyName). If multiple companies are mentioned, list them (e.g., ["Apple", "Microsoft"]). If the query is about a sector trend, leave as an empty list (e.g., []).
2. Infer the relevant date period (datePeriod), which includes:
   - year: The relevant year or range of years (use a list for ranges or sets, e.g., ["2023", "2024"]).
   - asOfDateOfTheDocument: The specific date or quarter if mentioned (e.g., "Q2 2024" or "June 30, 2024"; use a list if multiple dates are implied).
   - Use the current date (March 27, 2025) to default to the most recent documents (e.g., 2024) unless the query specifies otherwise.
3. Infer the industry sector if clear (industrySectorOfTheCompany, e.g., ["Technology", "Energy"]). For sector trends, specify the sector; for multiple companies, use the shared sector if applicable.
4. Determine the relevant newsSources and NewsTypeNames to query based on the query’s intent and the detailed descriptions of each source and type:
   - Select **Fitch Ratings** for queries about credit ratings, financial stability, or new issuances, choosing the appropriate NewsTypeNames based on the specific focus (e.g., "Downgrade" for rating reductions, "New Issue Report" for new debt analysis).
   - Select **SnP** for queries about credit ratings, research updates, or in-depth financial analyses, choosing the appropriate NewsTypeNames based on the specific focus (e.g., "Rating Action" for rating changes, "Full Analysis" for comprehensive reports).
   - Select **Moodys** for queries about credit opinions, rating actions, or issuer profiles, choosing the appropriate NewsTypeNames based on the specific focus (e.g., "Credit Opinion" for creditworthiness, "Issuer In-Depth" for detailed profiles).
   - Select **EDGAR** for queries about financial performance, business operations, or regulatory disclosures, choosing the appropriate NewsTypeNames based on the time frame (e.g., "Filing10K" for annual data, "Filing10Q" for quarterly data).
   - Select **Refinitiv** for queries about earnings discussions, conference calls, or executive statements, choosing "Earning Conference Call" as the NewsTypeName.
   - Select **DbrsMorningstar** for queries about rating changes or upgrades, choosing the appropriate NewsTypeNames based on the specific focus (e.g., "Upgrade" for rating increases, "Rating Action" for any rating change).
5. Extract key topics or keywords from the query (keyTopics, e.g., ["revenue", "hiring", "merger"]).
6. If the query involves multiple types of information (e.g., financial performance and credit rating), select multiple newsSources and their corresponding NewsTypeNames as needed.
7. Be conservative—only infer metadata explicitly supported by the query or common financial news patterns. If the query’s intent doesn’t match any fields, leave them as empty lists or strings.
8. Provide an explanation section detailing the reasoning behind each metadata field, structured as follows:
   - companyName: Explain how the company name(s) were identified or why left blank.
   - datePeriod:
     - year: Explain the choice of years based on the query and current date.
     - asOfDateOfTheDocument: Explain the choice of specific dates or quarters, or why left empty.
   - industrySectorOfTheCompany: Explain the inferred sector or why left blank.
   - newsSources: Explain why each news source was selected based on the query’s intent and source descriptions.
   - NewsTypeNames: Explain why each NewsTypeName was selected based on the query’s intent and descriptions.
   - keyTopics: Explain the keywords reflecting the query’s focus.

Output:
{
  "metadata": {
    "companyName": [],
    "datePeriod": {
      "year": [],
      "asOfDateOfTheDocument": []
    },
    "industrySectorOfTheCompany": [],
    "newsSources": [],
    "NewsTypeNames": [],
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
    "NewsTypeNames": "",
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
