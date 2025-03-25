Let’s refine the prompt to include detailed guidance on how to infer the NewsTypeNames subcategories for each newsSources based on the user query. This will help the AI agent make more precise decisions about which subcategories to query, ensuring the retrieved documents are highly relevant. I’ll incorporate specific rules for each NewsTypeNames under their respective newsSources (e.g., "Fitch Ratings", "SnP", "Moodys", "EDGAR", "Refinitiv", "DbrsMorningstar") to align with the query’s intent. The prompt will continue to use the metadata fields (COMPANY_NAME, YEAR, AS_OF_DATE_OF_THE_DOCUMENT, INDUSTRY_SECTOR_OF_THE_COMPANY, newsSources, NewsTypeNames, KEY_TOPICS), the current date (February 25, 2025), and output metadata in JSON format with lists for ranges or sets.
Refined Prompt with Detailed NewsTypeNames Inference

You are a financial research assistant tasked with interpreting user queries about financial news and filings from a knowledge database of 20 million documents. The documents are categorized by newsSources and subcategories (NewsTypeNames). The available newsSources and NewsTypeNames are:

- **newsSources**:
  - "Fitch Ratings": "Rating Report", "Affirmation", "Downgrade", "New Issue Report", "New Issue", "Presale Report", "Full Rating Report"
  - "SnP": "Research Update", "Rating Action", "Full Analysis", "New Issue Report"
  - "Moodys": "Rating Action", "Credit Opinion", "Pre-Sale Report", "New Issue Report", "Issuer In-Depth"
  - "EDGAR": "Filing10K", "Filing10KA", "Filing10Q", "Filing10QA"
  - "Refinitiv": "Earning Conference Call"
  - "DbrsMorningstar": "Rating Action", "Upgrade"

Each document has the following metadata: COMPANY_NAME, YEAR, AS_OF_DATE_OF_THE_DOCUMENT, and INDUSTRY_SECTOR_OF_THE_COMPANY. Your goal is to decompose the user query to infer metadata, including which combination of newsSources and NewsTypeNames to query, to narrow down the document set for retrieval. Output the inferred metadata as a JSON object, using lists for values that represent ranges or sets (e.g., ["2023", "2024"] for YEAR). If no inference is possible, leave the field as an empty list or empty string as appropriate.

Today’s date is February 25, 2025. Use this to infer the most recent or relevant timeframes for documents (e.g., default to the latest year like 2024 or Q4 2024 unless otherwise specified).

User Query: [Insert User Query Here]

Instructions:
1. Identify the company or companies mentioned (COMPANY_NAME).
2. Infer the relevant year or range of years (YEAR; use a list for ranges or sets, e.g., ["2023", "2024"]).
3. Estimate the approximate date of the document if specified (AS_OF_DATE_OF_THE_DOCUMENT, e.g., "Q2 2024" or "June 30, 2024"; use a list if multiple dates are implied).
4. Infer the industry sector if clear (INDUSTRY_SECTOR_OF_THE_COMPANY, e.g., "Technology", "Energy").
5. Determine the relevant newsSources and NewsTypeNames to query based on the query’s intent and the typical content of each source and type:
   - **Fitch Ratings**: Focuses on credit ratings and financial stability.
     - "Rating Report": Use for general queries about a company’s credit rating or financial stability.
     - "Affirmation": Use for queries about a company’s rating being confirmed or unchanged.
     - "Downgrade": Use for queries about a company’s rating being lowered.
     - "New Issue Report": Use for queries about new debt or financial instruments issued by a company.
     - "New Issue": Use for queries about the issuance of new securities.
     - "Presale Report": Use for queries about pre-sale analysis of new financial instruments.
     - "Full Rating Report": Use for comprehensive queries about a company’s overall credit rating history.
   - **SnP**: Focuses on ratings, research updates, and detailed analyses.
     - "Research Update": Use for queries about recent updates or changes in a company’s financial outlook.
     - "Rating Action": Use for queries about specific changes in a company’s credit rating.
     - "Full Analysis": Use for in-depth queries about a company’s financial health or rating rationale.
     - "New Issue Report": Use for queries about new debt or financial instruments issued by a company.
   - **Moodys**: Focuses on credit opinions, rating actions, and in-depth issuer reports.
     - "Rating Action": Use for queries about specific changes in a company’s credit rating.
     - "Credit Opinion": Use for queries about a company’s creditworthiness or financial outlook.
     - "Pre-Sale Report": Use for queries about pre-sale analysis of new financial instruments.
     - "New Issue Report": Use for queries about new debt or financial instruments issued by a company.
     - "Issuer In-Depth": Use for comprehensive queries about a company’s financial health or credit profile.
   - **EDGAR**: Contains SEC filings (10-K, 10-Q, etc.).
     - "Filing10K": Use for queries about annual financial performance, business overviews, or long-term trends.
     - "Filing10KA": Use for queries about amended annual filings or corrections to 10-K reports.
     - "Filing10Q": Use for queries about quarterly financial performance, short-term trends, or specific quarterly events.
     - "Filing10QA": Use for queries about amended quarterly filings or corrections to 10-Q reports.
   - **Refinitiv**: Focuses on earnings conference calls.
     - "Earning Conference Call": Use for queries about earnings discussions, conference calls, or executive statements.
   - **DbrsMorningstar**: Focuses on rating actions and upgrades.
     - "Rating Action": Use for queries about specific changes in a company’s credit rating.
     - "Upgrade": Use for queries about a company’s rating being raised.
6. Extract key topics or keywords from the query (KEY_TOPICS, e.g., "revenue", "hiring", "merger").
7. Be conservative—only infer metadata explicitly supported by the query or common financial news patterns. Use the current date (February 25, 2025) to default to the most recent documents unless the query specifies otherwise.

Output:
{
  "COMPANY_NAME": "",
  "YEAR": [],
  "AS_OF_DATE_OF_THE_DOCUMENT": [],
  "INDUSTRY_SECTOR_OF_THE_COMPANY": "",
  "newsSources": [],
  "NewsTypeNames": [],
  "KEY_TOPICS": []
}

Applying the Refined Prompt to Your Queries
Below, I’ll apply this refined prompt to each of the 12 queries, providing the inferred metadata output in JSON format and a detailed explanation for each, focusing on how the NewsTypeNames are inferred based on the new guidance.
1. What % of the revenue of Apple comes from laptops and desktop computers?
Prompt: (As above, with "What % of the revenue of Apple comes from laptops and desktop computers?" as the user query)
Inferred Metadata Output:
json

{
  "COMPANY_NAME": "Apple",
  "YEAR": ["2024"],
  "AS_OF_DATE_OF_THE_DOCUMENT": [],
  "INDUSTRY_SECTOR_OF_THE_COMPANY": "Technology",
  "newsSources": ["EDGAR"],
  "NewsTypeNames": ["Filing10K"],
  "KEY_TOPICS": ["revenue", "laptops", "desktop computers"]
}

Explanation:

    COMPANY_NAME: "Apple" is explicitly mentioned.
    YEAR: Set to ["2024"] because the query implies recent data, and using February 25, 2025, the most recent annual filing would be for 2024.
    AS_OF_DATE_OF_THE_DOCUMENT: Left empty as no specific date or quarter is mentioned.
    INDUSTRY_SECTOR_OF_THE_COMPANY: "Technology" is inferred because Apple operates in this sector.
    newsSources: ["EDGAR"] is selected because revenue data for specific product categories is typically found in SEC filings, not in rating reports or conference calls.
    NewsTypeNames: ["Filing10K"] is chosen because the query is about annual revenue breakdowns, which aligns with "Filing10K" (annual financial performance) under EDGAR, as per the guidance.
    KEY_TOPICS: ["revenue", "laptops", "desktop computers"] reflect the query’s focus.

2. What are hiring trends in hospitality?
Prompt: (As above, with "What are hiring trends in hospitality?" as the user query)
Inferred Metadata Output:
json

{
  "COMPANY_NAME": "",
  "YEAR": ["2023", "2024"],
  "AS_OF_DATE_OF_THE_DOCUMENT": [],
  "INDUSTRY_SECTOR_OF_THE_COMPANY": "Hospitality",
  "newsSources": ["EDGAR"],
  "NewsTypeNames": ["Filing10K", "Filing10Q"],
  "KEY_TOPICS": ["hiring", "trends"]
}

Explanation:

    COMPANY_NAME: Left blank because the query is industry-wide.
    YEAR: Set to ["2023", "2024"] for recent data, using February 25, 2025, to focus on the latest filings.
    AS_OF_DATE_OF_THE_DOCUMENT: Left empty as no specific date or quarter is mentioned.
    INDUSTRY_SECTOR_OF_THE_COMPANY: "Hospitality" is inferred from the query.
    newsSources: ["EDGAR"] is selected because hiring trends are typically discussed in SEC filings under human capital sections, not in rating reports or conference calls.
    NewsTypeNames: ["Filing10K", "Filing10Q"] are chosen because hiring trends may be discussed in both annual ("Filing10K" for long-term trends) and quarterly ("Filing10Q" for short-term trends) reports, as per the guidance.
    KEY_TOPICS: ["hiring", "trends"] reflect the query’s focus.

3. What was the logic for the AON-WTW merger?
Prompt: (As above, with "What was the logic for the AON-WTW merger?" as the user query)
Inferred Metadata Output:
json

{
  "COMPANY_NAME": "AON, Willis Towers Watson",
  "YEAR": ["2020"],
  "AS_OF_DATE_OF_THE_DOCUMENT": [],
  "INDUSTRY_SECTOR_OF_THE_COMPANY": "Insurance",
  "newsSources": ["EDGAR"],
  "NewsTypeNames": [],
  "KEY_TOPICS": ["merger", "logic"]
}

Explanation:

    COMPANY_NAME: "AON" and "Willis Towers Watson" are explicitly mentioned.
    YEAR: Set to ["2020"] based on historical knowledge of the AON-WTW merger occurring in 2020.
    AS_OF_DATE_OF_THE_DOCUMENT: Left empty as no specific date is mentioned.
    INDUSTRY_SECTOR_OF_THE_COMPANY: "Insurance" is inferred because AON and WTW operate in this sector.
    newsSources: ["EDGAR"] is selected because merger details are often disclosed in SEC filings, though none of the provided NewsTypeNames directly match merger-specific 8-K filings.
    NewsTypeNames: Left empty because the NewsTypeNames for EDGAR ("Filing10K", "Filing10KA", "Filing10Q", "Filing10QA") don’t include 8-K filings, which would typically contain merger details ("Filing8K" is missing). The guidance for EDGAR doesn’t provide a matching subcategory for this event-specific query.
    KEY_TOPICS: ["merger", "logic"] reflect the query’s focus.

Note: As mentioned previously, you might need to expand the NewsTypeNames for EDGAR to include "Filing8K" to handle merger-specific queries.
4. What is the impact of tariffs on interest rates?
Prompt: (As above, with "What is the impact of tariffs on interest rates?" as the user query)
Inferred Metadata Output:
json

{
  "COMPANY_NAME": "",
  "YEAR": ["2023", "2024"],
  "AS_OF_DATE_OF_THE_DOCUMENT": [],
  "INDUSTRY_SECTOR_OF_THE_COMPANY": ["Financial Services", "Manufacturing"],
  "newsSources": ["EDGAR"],
  "NewsTypeNames": ["Filing10K", "Filing10Q"],
  "KEY_TOPICS": ["tariffs", "interest rates", "impact"]
}

Explanation:

    COMPANY_NAME: Left blank because the query is about an economic impact, not a specific company.
    YEAR: Set to ["2023", "2024"] for recent data, using February 25, 2025, to focus on the latest filings.
    AS_OF_DATE_OF_THE_DOCUMENT: Left empty as no specific date or quarter is mentioned.
    INDUSTRY_SECTOR_OF_THE_COMPANY: ["Financial Services", "Manufacturing"] are inferred because tariffs affect manufacturing (trade costs) and financial services (interest rate policies).
    newsSources: ["EDGAR"] is selected because economic impacts like tariffs and interest rates are often discussed in SEC filings under management discussions or risk factors.
    NewsTypeNames: ["Filing10K", "Filing10Q"] are chosen because the query involves long-term and recent impacts, aligning with "Filing10K" (annual financial performance) and "Filing10Q" (short-term trends) under EDGAR, as per the guidance.
    KEY_TOPICS: ["tariffs", "interest rates", "impact"] reflect the query’s focus.

5. What is the impact of tariffs on Canada?
Prompt: (As above, with "What is the impact of tariffs on Canada?" as the user query)
Inferred Metadata Output:
json

{
  "COMPANY_NAME": "",
  "YEAR": ["2023", "2024"],
  "AS_OF_DATE_OF_THE_DOCUMENT": [],
  "INDUSTRY_SECTOR_OF_THE_COMPANY": ["Manufacturing", "Energy"],
  "newsSources": ["EDGAR"],
  "NewsTypeNames": ["Filing10K", "Filing10Q"],
  "KEY_TOPICS": ["tariffs", "impact", "Canada"]
}

Explanation:

    COMPANY_NAME: Left blank because the query is about a geographic and economic impact, not a specific company.
    YEAR: Set to ["2023", "2024"] for recent data, using February 25, 2025, to focus on the latest filings.
    AS_OF_DATE_OF_THE_DOCUMENT: Left empty as no specific date or quarter is mentioned.
    INDUSTRY_SECTOR_OF_THE_COMPANY: ["Manufacturing", "Energy"] are inferred because tariffs on Canada often affect industries like manufacturing (trade goods) and energy (oil exports).
    newsSources: ["EDGAR"] is selected because the impact of tariffs on Canada would be discussed in SEC filings under management discussions or risk factors.
    NewsTypeNames: ["Filing10K", "Filing10Q"] are chosen because the query involves long-term and recent impacts, aligning with "Filing10K" (annual financial performance) and "Filing10Q" (short-term trends) under EDGAR, as per the guidance.
    KEY_TOPICS: ["tariffs", "impact", "Canada"] reflect the query’s focus.

6. What are the implications for FWA for cable companies?
Prompt: (As above, with "What are the implications for FWA for cable companies?" as the user query)
Inferred Metadata Output:
json

{
  "COMPANY_NAME": "",
  "YEAR": ["2023", "2024"],
  "AS_OF_DATE_OF_THE_DOCUMENT": [],
  "INDUSTRY_SECTOR_OF_THE_COMPANY": "Telecommunications",
  "newsSources": ["EDGAR"],
  "NewsTypeNames": ["Filing10K", "Filing10Q"],
  "KEY_TOPICS": ["FWA", "implications"]
}

Explanation:

    COMPANY_NAME: Left blank because the query is industry-wide.
    YEAR: Set to ["2023", "2024"] for recent data, using February 25, 2025, to focus on the latest filings.
    AS_OF_DATE_OF_THE_DOCUMENT: Left empty as no specific date or quarter is mentioned.
    INDUSTRY_SECTOR_OF_THE_COMPANY: "Telecommunications" is inferred because cable companies operate in this sector.
    newsSources: ["EDGAR"] is selected because the implications of Fixed Wireless Access (FWA) for cable companies would be discussed in SEC filings under risk factors or business overviews.
    NewsTypeNames: ["Filing10K", "Filing10Q"] are chosen because the query involves long-term and recent implications, aligning with "Filing10K" (annual financial performance) and "Filing10Q" (short-term trends) under EDGAR, as per the guidance.
    KEY_TOPICS: ["FWA", "implications"] reflect the query’s focus.

7. Are there any public companies with exposure to small cells?
Prompt: (As above, with "Are there any public companies with exposure to small cells?" as the user query)
Inferred Metadata Output:
json

{
  "COMPANY_NAME": "",
  "YEAR": ["2023", "2024"],
  "AS_OF_DATE_OF_THE_DOCUMENT": [],
  "INDUSTRY_SECTOR_OF_THE_COMPANY": "Telecommunications",
  "newsSources": ["EDGAR"],
  "NewsTypeNames": ["Filing10K"],
  "KEY_TOPICS": ["small cells", "exposure"]
}

Explanation:

    COMPANY_NAME: Left blank because the query is industry-wide.
    YEAR: Set to ["2023", "2024"] for recent data, using February 25, 2025, to focus on the latest filings.
    AS_OF_DATE_OF_THE_DOCUMENT: Left empty as no specific date or quarter is mentioned.
    INDUSTRY_SECTOR_OF_THE_COMPANY: "Telecommunications" is inferred because small cells are relevant to telecom companies.
    newsSources: ["EDGAR"] is selected because exposure to small cells would be detailed in SEC filings under business overviews or capital expenditures.
    NewsTypeNames: ["Filing10K"] is chosen because the query focuses on long-term exposure, aligning with "Filing10K" (annual financial performance) under EDGAR, as per the guidance.
    KEY_TOPICS: ["small cells", "exposure"] reflect the query’s focus.

8. What are the US Energy industry revenue growth trends?
Prompt: (As above, with "What are the US Energy industry revenue growth trends?" as the user query)
Inferred Metadata Output:
json

{
  "COMPANY_NAME": "",
  "YEAR": ["2020", "2021", "2022", "2023", "2024"],
  "AS_OF_DATE_OF_THE_DOCUMENT": [],
  "INDUSTRY_SECTOR_OF_THE_COMPANY": "Energy",
  "newsSources": ["EDGAR"],
  "NewsTypeNames": ["Filing10K", "Filing10Q"],
  "KEY_TOPICS": ["revenue growth", "trends"]
}

Explanation:

    COMPANY_NAME: Left blank because the query is industry-wide.
    YEAR: Set to ["2020", "2021", "2022", "2023", "2024"] to capture a multi-year trend, using February 25, 2025, to include the latest filings.
    AS_OF_DATE_OF_THE_DOCUMENT: Left empty as no specific date or quarter is mentioned.
    INDUSTRY_SECTOR_OF_THE_COMPANY: "Energy" is inferred from the query.
    newsSources: ["EDGAR"] is selected because revenue growth trends are typically discussed in SEC filings under financial statements or management discussions.
    NewsTypeNames: ["Filing10K", "Filing10Q"] are chosen because the query involves long-term and recent trends, aligning with "Filing10K" (annual financial performance) and "Filing10Q" (short-term trends) under EDGAR, as per the guidance.
    KEY_TOPICS: ["revenue growth", "trends"] reflect the query’s focus.

9. What are the major drugs in Eli Lilly’s portfolio and the market expectations?
Prompt: (As above, with "What are the major drugs in Eli Lilly’s portfolio and the market expectations?" as the user query)
Inferred Metadata Output:
json

{
  "COMPANY_NAME": "Eli Lilly",
  "YEAR": ["2023", "2024"],
  "AS_OF_DATE_OF_THE_DOCUMENT": [],
  "INDUSTRY_SECTOR_OF_THE_COMPANY": "Pharmaceuticals",
  "newsSources": ["EDGAR"],
  "NewsTypeNames": ["Filing10K"],
  "KEY_TOPICS": ["drugs", "portfolio", "market expectations"]
}

Explanation:

    COMPANY_NAME: "Eli Lilly" is explicitly mentioned.
    YEAR: Set to ["2023", "2024"] for recent data, using February 25, 2025, to focus on the latest filings.
    AS_OF_DATE_OF_THE_DOCUMENT: Left empty as no specific date or quarter is mentioned.
    INDUSTRY_SECTOR_OF_THE_COMPANY: "Pharmaceuticals" is inferred because Eli Lilly operates in this sector.
    newsSources: ["EDGAR"] is selected because major drugs and market expectations are typically detailed in SEC filings under business overviews.
    NewsTypeNames: ["Filing10K"] is chosen because the query focuses on a comprehensive portfolio overview, aligning with "Filing10K" (annual financial performance) under EDGAR, as per the guidance.
    KEY_TOPICS: ["drugs", "portfolio", "market expectations"] reflect the query’s focus.

10. What is the correlation between housing market trends and Home Depot sales performance over the past decade?
Prompt: (As above, with "What is the correlation between housing market trends and Home Depot sales performance over the past decade?" as the user query)
Inferred Metadata Output:
json

{
  "COMPANY_NAME": "Home Depot",
  "YEAR": ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"],
  "AS_OF_DATE_OF_THE_DOCUMENT": [],
  "INDUSTRY_SECTOR_OF_THE_COMPANY": "Retail",
  "newsSources": ["EDGAR"],
  "NewsTypeNames": ["Filing10K", "Filing10Q"],
  "KEY_TOPICS": ["housing market", "sales performance", "correlation"]
}

Explanation:

    COMPANY_NAME: "Home Depot" is explicitly mentioned.
    YEAR: Set to ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"] to cover the past decade, using February 25, 2025, to include the latest filings.
    AS_OF_DATE_OF_THE_DOCUMENT: Left empty as no specific date or quarter is mentioned.
    INDUSTRY_SECTOR_OF_THE_COMPANY: "Retail" is inferred because Home Depot operates in this sector.
    newsSources: ["EDGAR"] is selected because sales performance and market trends are typically discussed in SEC filings under management discussions.
    NewsTypeNames: ["Filing10K", "Filing10Q"] are chosen because the query involves long-term and recent trends, aligning with "Filing10K" (annual financial performance) and "Filing10Q" (short-term trends) under EDGAR, as per the guidance.
    KEY_TOPICS: ["housing market", "sales performance", "correlation"] reflect the query’s focus.

11. How did UnitedHealth discuss healthcare optimization at the Goldman conference?
Prompt: (As above, with "How did UnitedHealth discuss healthcare optimization at the Goldman conference?" as the user query)
Inferred Metadata Output:
json

{
  "COMPANY_NAME": "UnitedHealth Group",
  "YEAR": ["2024"],
  "AS_OF_DATE_OF_THE_DOCUMENT": ["Q2 2024"],
  "INDUSTRY_SECTOR_OF_THE_COMPANY": "Healthcare",
  "newsSources": ["Refinitiv"],
  "NewsTypeNames": ["Earning Conference Call"],
  "KEY_TOPICS": ["healthcare optimization", "Goldman conference"]
}

Explanation:

    COMPANY_NAME: "UnitedHealth" (full name "UnitedHealth Group") is explicitly mentioned.
    YEAR: Set to ["2024"] because the query implies a recent event, and Q2 2024 aligns with typical conference timings, using February 25, 2025, to focus on the latest documents.
    AS_OF_DATE_OF_THE_DOCUMENT: Set to ["Q2 2024"] based on the assumption that the Goldman conference occurred in mid-2024.
    INDUSTRY_SECTOR_OF_THE_COMPANY: "Healthcare" is inferred because UnitedHealth operates in this sector.
    newsSources: ["Refinitiv"] is selected because the query focuses on a conference discussion, and Refinitiv provides conference call documents.
    NewsTypeNames: ["Earning Conference Call"] is chosen because the query is about a conference discussion, aligning with "Earning Conference Call" (earnings discussions, conference calls) under Refinitiv, as per the guidance.
    KEY_TOPICS: ["healthcare optimization", "Goldman conference"] reflect the query’s focus.

12. What are companies saying about cost inflation in Q2 2024?
Prompt: (As above, with "What are companies saying about cost inflation in Q2 2024?" as the user query)
Inferred Metadata Output:
json

{
  "COMPANY_NAME": "",
  "YEAR": ["2024"],
  "AS_OF_DATE_OF_THE_DOCUMENT": ["Q2 2024"],
  "INDUSTRY_SECTOR_OF_THE_COMPANY": ["Energy", "Retail"],
  "newsSources": ["EDGAR"],
  "NewsTypeNames": ["Filing10Q"],
  "KEY_TOPICS": ["cost inflation"]
}

Explanation:

    COMPANY_NAME: Left blank because the query is industry-wide.
    YEAR: Set to ["2024"] because the query specifies Q2 2024, aligning with February 25, 2025.
    AS_OF_DATE_OF_THE_DOCUMENT: Set to ["Q2 2024"] as explicitly mentioned in the query.
    INDUSTRY_SECTOR_OF_THE_COMPANY: ["Energy", "Retail"] are inferred because cost inflation often impacts industries like energy (input costs) and retail (pricing pressures).
    newsSources: ["EDGAR"] is selected because cost inflation in a specific quarter would be discussed in SEC filings under management discussions or risk factors.
    NewsTypeNames: ["Filing10Q"] is chosen because the query focuses on a specific quarter (Q2 2024), aligning with "Filing10Q" (quarterly financial performance) under EDGAR, as per the guidance.
    KEY_TOPICS: ["cost inflation"] reflect the query’s focus.

Additional Notes

    Expanding NewsTypeNames: As noted earlier, the NewsTypeNames for EDGAR lack 8-K filings, which are critical for event-specific queries (e.g., mergers, conference calls). Adding "Filing8K" to EDGAR’s NewsTypeNames would improve coverage for queries like the AON-WTW merger.
    Edge Cases: The refined prompt handles most queries well, but for queries involving rating changes (e.g., "Did Apple get downgraded?"), you might want to prioritize sources like Fitch Ratings, SnP, Moodys, or DbrsMorningstar with NewsTypeNames like "Downgrade", "Rating Action", or "Credit Opinion".
    Testing: Test the prompt with diverse queries (e.g., rating changes, conference calls, financial trends) to ensure the NewsTypeNames inference rules are robust.

This refined prompt provides detailed guidance on inferring NewsTypeNames, ensuring the AI agent selects the most relevant subcategories for each newsSources based on the query’s intent. Let me know if you’d like to test additional queries or further refine the prompt!
