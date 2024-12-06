Optimized Prompt:

Instruction to the LLM:

You are a financial data analyst. Your task is to extract and populate a detailed JSON structure based on the provided SEC termsheet. Follow these instructions to ensure maximum accuracy and consistency:

    Data Extraction:
        Carefully read and analyze the SEC termsheet for all relevant information.
        Extract key details and map them to the corresponding fields in the JSON structure below.

    Formatting Rules:
        Date Fields: Convert all dates into the format YYYY/MM/DD.
        Currency and Numerical Values: Ensure all numerical values (e.g., notional, percentages) are formatted correctly and exclude any non-numeric characters (e.g., "$", "%").
        Boolean Fields: Use true or false for fields requiring Boolean values.
        Empty Fields: Leave blank any sections for which information is unavailable or irrelevant.
        Enumerated Types: Use the predefined options (e.g., "callType" must be either "Auto" or "Issuer"; "basketType" must be one of "WorstOf", "BestOf", "Basket", "Mono", "Rainbow", or "Other").
        Descriptive Terms: Use clear, concise terms based on the definitions provided in the SEC termsheet. For example:
            A fixed payment above a threshold = "Digital Return."
            A dual directional product = "Absolute Return."
            A weighted basket determined at maturity = "Rainbow."

    Underlier List:
        Populate the underlierList array with information for each underlying asset.
        Include fields like underlierName, underlierWeight, underlierSource, underlierSymbol, and initialFixing for each underlier.

    Key Definitions:
        Call Type: Use "Auto" if the product is callable automatically. Use "Issuer" if the issuer initiates the call.
        Basket Type: Define the type of basket (e.g., "WorstOf", "BestOf", "Rainbow") based on the composition and conditions described in the termsheet.
        Digital Return: Identify if the product has a fixed payment above a barrier threshold.
        Absolute Performance: Populate isDualDirectional as true if the product includes dual-directional/absolute return features.

    JSON Structure:
        Populate the following JSON structure with the extracted data. Ensure all fields are accurate, consistent, and adhere to the formatting rules above.

{
    // Unique identifier for the security
    "CUSIP": "",
    // International Securities Identification Number
    "ISIN": "",
    // Full legal name of the security from cover page
    "productName": "",
    // Legal entity name of the issuer
    "issuer": "",
    // Currency of the notional (e.g., "USD")
    "currency": "",
    // Principal amount without currency symbol
    "notional": "",
    // SEC registration numbers
    "registrationType": "",
    // Pricing date in YYYY/MM/DD format
    "tradeDate": "",
    // Initial fixing date in YYYY/MM/DD format
    "strikeDate": "",
    // Settlement date in YYYY/MM/DD format
    "issueDate": "",
    // Last valuation date in YYYY/MM/DD format
    "finalValuationDate": "",
    // Final payment date in YYYY/MM/DD format
    "maturityDate": "",
    // Type of settlement (Cash/Physical)
    "settlementType": "",
    // Basket performance type (WcrtOf for worst-of structure)
    "basketType (WcrtOf, BestOf, Basket, Mono, Rainbow, Other)": "",
    // List of underlying assets
    "underlierList": [{
        // Name of the underlying asset
        "underlierName": "",
        // Weight in the basket (if applicable)
        "underlierWeight": "",
        // Data source/index provider
        "underlierSource": "",
        // Trading symbol
        "underlierSymbol": "",
        // Initial fixing level
        "initialFixing": ""
    }],
    // Main product category
    "productType": "",
    // Set to "true" for absolute performance features
    "isDualDirectional": "",
    // Lookback features if any
    "ancillaryFeatures": {
        "isLookback": "",
        "lookbackDateList": [],
        "lookbackObservationFrequency (daily/weekly/monthly)": "",
        "lookbackValuationType (min/max/average)": ""
    },
    // Business day convention
    "dateOffset": "",
    // Coupon/yield related features
    "productYield": {
        // Type of coupon payment
        "paymentType": "",
        // Frequency of coupon evaluation
        "paymentEvaluationFrequency": "",
        // Frequency of barrier observation
        "paymentBarrierObservationFrequency": "",
        // List of coupon observation dates in YYYY/MM/DD
        "paymentObservationDateList": [],
        // List of coupon payment dates in YYYY/MM/DD
        "paymentSettlementDateList": [],
        // Coupon payment frequency
        "paymentFrequency": "",
        // Coupon rate per period
        "paymentRatePerPeriod": "",
        // Coupon barrier level in percentage
        "paymentBarrierPercentage": "",
        // Memory feature indicator
        "paymentMemory": "",
        // Annualized coupon rate
        "paymentRatePerAnnum": ""
    },
    // Autocall features
    "productCall": {
        // Set to "Auto" for automatic calls
        "callType (Auto/Issuer)": "",
        // List of potential call dates in YYYY/MM/DD
        "callObservationDateList": [],
        // List of call payment dates in YYYY/MM/DD
        "callSettlementDateList": [],
        // Call trigger level in percentage
        "callBarrierPercent": "",
        // Call premium amount
        "callPremiumPercent": "",
        // Memory feature for call premium
        "callPremiumMemory": "",
        // Frequency of call observations
        "callObservationFrequency": "",
        // Total number of call periods
        "numberOfCallPeriods": "",
        // Type of observation for calls
        "callPeriodObservationType": ""
    },
    // Capital protection features
    "productProtection": {
        // Type of downside protection
        "downsideType (barrier/buffer/full)": "",
        // Full principal protection indicator
        "fullPrincipleProtection": "",
        // Put strike level
        "putStrikePercent": "",
        // Barrier level for principal protection
        "principalBarrierLevel": "",
        // Barrier level in percentage
        "principalBarrierLevelPercentage": "",
        // Frequency of put barrier observation
        "putObservationFrequency": "",
        // List of put observation dates
        "putObservationDateList": [],
        // Downside participation rate
        "putLeverage": "",
        // Buffer percentage if applicable
        "bufferPercentage": ""
    },
    // Upside participation features
    "productGrowth": {
        // Participation rate in underlying performance
        "upsideParticipationRate": "",
        // List of call strike levels
        "callStrikeList": [{
            // Strike level in percentage
            "callStrikePercentage": ""
        }],
        // Cap on underlying return
        "underlierReturnCapLevel": "",
        // Fixed return above barrier
        "digitalReturn": "",
        // Barrier for digital return
        "digitalReturnBarrier": "",
        // Observation dates for digital return
        "digitalReturnBarrierObservationDateList": [],
        // Uncapped return above digital level
        "uncappedAboveDigitalReturn": "",
        // Participation rate above digital level
        "upsideParticipationAboveDigitalReturn": "",
        // Barrier for absolute return
        "absoluteReturnBarrierLevel": "",
        // Maximum return possible
        "maximumReturn": "",
        // Type of growth feature
        "growthType": [],
        // Bearish product indicator
        "bearish": ""
    },
    // Estimated value per security
    "estimatedValue": ""
}

End Extraction.

    Ensure the JSON is fully populated with the available data. For any missing or ambiguous details, leave the fields blank but ensure the structure is intact.
    
