Here’s a breakdown of the **desk names** you provided, including a **financial interpretation** of what types of content and themes you can expect in documents from each desk. This will help you define metadata tags or query-routing logic in your agentic RAG system.

---

### 🔝 High-Level Categories by DeskName:

| DeskName                                                          | Description of Expected Content                                                                                                                                                                          |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **RMBS** *(Residential Mortgage-Backed Securities)*               | Deal documents, prospectuses, remittance reports, bond structure waterfalls, prepayment rates, credit enhancements, tranche-level data, stress scenarios, rating agency notes, housing market analytics. |
| **MSFS** *(Morgan Stanley Fund Services)*                         | NAV reports, hedge fund valuation statements, fund administration documents, shadow accounting reconciliations, performance summaries, and compliance documentation.                                     |
| **CLO** *(Collateralized Loan Obligations)*                       | Deal term sheets, offering memoranda, trustee reports, collateral quality reports, cash flow waterfalls, tranche performance, covenant data, asset manager commentary.                                   |
| **CMBS** *(Commercial Mortgage-Backed Securities)*                | Deal packages, loan tapes, rent rolls, DSCR/LTV metrics, lease-level data, property appraisals, servicer surveillance reports, and commercial real estate trends.                                        |
| **MSIM** *(Morgan Stanley Investment Management)*                 | Fund strategy docs, investor communications, ESG reports, fund performance overviews, allocation strategies, macroeconomic outlooks, asset manager views.                                                |
| **ABS** *(Asset-Backed Securities)*                               | Auto loan ABS, credit card ABS, student loan ABS documentation. Expect asset pool summaries, credit enhancement structures, payment structures, delinquency & default reports.                           |
| **LEVLOANS** *(Leveraged Loans)*                                  | Syndicated loan term sheets, commitment letters, LIBOR/SOFR margins, covenant-lite status, company financials, credit agreements, bank book info.                                                        |
| **EU** *(Likely Europe-focused debt/capital markets)*             | EMEA-focused deal summaries, regulatory documentation (MiFID II, PRIIPs), European bond issuances, local market credit data, and EU macroeconomic reports.                                               |
| **DOCPOINT\_ISDA**                                                | Derivatives documentation: ISDA Master Agreements, CSAs (Credit Support Annexes), confirmations, netting agreements, legal opinions, and credit events.                                                  |
| **LEVFIN\_SMF** *(Leveraged Finance – Structured Market Finance)* | Hybrid debt/equity deal docs, term loan Bs, high-yield bond issues, covenant summaries, arranger/sponsor info, liquidity events, use of proceeds.                                                        |
| **MUNI\_TOB** *(Municipal Tender Option Bonds)*                   | TOB trust agreements, municipal bond performance, interest rate resets, floating rate note disclosures, tax-exempt yield analysis.                                                                       |
| **MUNI\_SYNDICATE\_DEAL**                                         | Municipal new issue deal files: POS (Preliminary Official Statements), OS (Official Statements), bond purchase agreements, tax opinions, rating letters, syndicate allocation summaries.                 |
| **NDA\_PILOT**                                                    | Internal or experimental pilot projects involving **Non-Disclosure Agreements**, potentially cross-desk legal and compliance workflows related to R\&D or confidential partnerships.                     |
| **EU\_LOANS**                                                     | Likely related to European leveraged/corporate loans. Expect credit memos, facility agreements, EMEA sector analysis, distressed or syndicated loan activity.                                            |
| **CRT** *(Credit Risk Transfer)*                                  | Primarily seen in Fannie Mae/Freddie Mac credit deals: STACR/CAS reports, risk retention documents, GSE deal tapes, historical loss curves, and modeling assumptions.                                    |

---

### 🧠 Suggestions for Your Agentic RAG Use:

To effectively route queries or filter documents:

* **Metadata Tags** you can infer for chunk retrieval:
  `instrument_type`, `region`, `issuer_type`, `document_type`, `risk_metrics`, `deal_name`, `counterparty`, `coverage_desk`, `regulation`.

* **Example tags for RMBS documents**:
  `{"instrument_type": "RMBS", "region": "US", "issuer_type": "non-agency", "document_type": "offering_memo", "risk_metrics": ["LTV", "FICO", "default_rate"]}`

* **Agent Tasks (per desk)**:

  * *RMBS Agent*: Summarize cash flow waterfall, extract delinquency trends.
  * *CLO Agent*: Pull tranche IRR projections, identify manager style drift.
  * *ISDA Agent*: Verify netting clauses and margin requirements.
  * *MUNI Agent*: Generate 3-year yield curve from POS.

Would you like me to help define metadata schema or RAG query templates for some of these desk types?
