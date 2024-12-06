{
    "CUSIP": "",  // Unique identifier for the security as assigned by the Committee on Uniform Securities Identification Procedures.
    "ISIN": "",  // International Securities Identification Number, used to uniquely identify the security globally.
    "productName": "",  // Name of the financial product (e.g., Callable Notes, Dual Directional Notes).
    "issuer": "",  // The entity issuing the financial product (e.g., Morgan Stanley, Goldman Sachs).
    "currency": "",  // Currency in which the product is denominated (e.g., USD, EUR).
    "notional": "",  // Notional amount of the product, typically representing the face value or principal amount.
    "registrationType": "",  // Type of registration (e.g., 144A, Reg S, or Public).
    "tradeDate": "",  // The date when the trade was executed.
    "strikeDate": "",  // The date when the initial fixing or strike price of the underliers was determined.
    "issueDate": "",  // The date on which the product was issued to investors.
    "finalValuationDate": "",  // The date when the final valuation of the product occurs.
    "maturityDate": "",  // The date when the product matures and the principal is repaid.
    "settlementType": "",  // Specifies the settlement method (e.g., physical delivery or cash settlement).
    "basketType (WosrtOf, BestOf, Basket, Mono, Rainbow, Other)": "",  // Type of basket used (e.g., WorstOf: worst-performing underlier, Rainbow: weighted basket at maturity).
    "underlierList": [
        {
            "underlierName": "",  // Name of the underlier (e.g., S&P 500 Index, Tesla Inc.).
            "underlierWeight": "",  // Weight of the underlier in the basket (if applicable).
            "underlierSource": "",  // Source of the underlier (e.g., Index, Stock, Commodity).
            "underlierSymbol": "",  // Symbol or ticker of the underlier (e.g., SPX, TSLA).
            "initialFixing": ""  // The initial value of the underlier at the strike date.
        }
    ],
    "productType": "",  // The type of financial product (e.g., Structured Note, Equity-Linked Note).
    "isDualDirectional": "",  // Indicates whether the product has a dual-directional feature (absolute performance).
    "ancillaryFeatures": {
        "isLookback": "",  // Indicates if the product includes a lookback feature.
        "lookbackDateList": [],  // List of dates used for lookback observations.
        "lookbackObservationFrequency (daily/weekly/monthly)": "",  // Frequency of lookback observations.
        "lookbackValuationType (min/max/average)": ""  // Method of lookback valuation (e.g., minimum value, maximum value, or average).
    },
    "dateOffset": "",  // The number of days or period offset for specific dates in the product's lifecycle.
    "productYield": {
        "paymentType": "",  // Type of payment (e.g., fixed, variable, digital return).
        "paymentEvaluationFrequency": "",  // Frequency of payment evaluation (e.g., monthly, quarterly).
        "paymentBarrierObservationFrequency": "",  // Frequency at which barriers are observed for payment.
        "paymentObservationDateList": [],  // List of dates for payment observations.
        "paymentSettlementDateList": [],  // List of dates for payment settlements.
        "paymentFrequency": "",  // Frequency of payments (e.g., monthly, annual).
        "paymentRatePerPeriod": "",  // Payment rate per period (e.g., 2.5% quarterly).
        "paymentBarrierPercentage": "",  // Barrier percentage for payments.
        "paymentMemory": "",  // Indicates if the product has a memory feature for missed payments.
        "paymentRatePerAnnum": ""  // Payment rate on an annualized basis.
    },
    "productCall": {
        "callType (Auto/Issuer)": "",  // Specifies whether the call is automatic (Auto) or initiated by the issuer (Issuer).
        "callObservationDateList": [],  // List of dates for call observations.
        "callSettlementDateList": [],  // List of settlement dates for calls.
        "callBarrierPercent": "",  // Percentage barrier for calling the product.
        "callPremiumPercent": "",  // Premium percentage paid upon call.
        "callPremiumMemory": "",  // Indicates if the call has a premium memory feature.
        "callObservationFrequency": "",  // Frequency of call observations (e.g., monthly, quarterly).
        "numberOfCallPeriods": "",  // Number of periods for calls.
        "callPeriodObservationType": ""  // Type of observation for the call period (e.g., periodic, continuous).
    },
    "productProtection": {
        "downsideType (barrier/buffer/full)": "",  // Type of downside protection (e.g., full protection, barrier, or buffer).
        "fullPrincipleProtection": "",  // Indicates if the product has full principal protection.
        "putStrikePercent": "",  // Strike percentage for a put option (if applicable).
        "principalBarrierLevel": "",  // Barrier level for principal protection.
        "principalBarrierLevelPercentage": "",  // Barrier percentage for principal protection.
        "putObservationFrequency": "",  // Frequency of put option observations.
        "putObservationDateList": [],  // List of dates for put option observations.
        "putLeverage": "",  // Leverage applied to put options.
        "bufferPercentage": ""  // Buffer percentage for downside protection.
    },
    "productGrowth": {
        "upsideParticipationRate": "",  // Participation rate for upside returns.
        "callStrikeList": [
            {
                "callStrikePercentage": ""  // List of strike percentages for calls.
            }
        ],
        "underlierReturnCapLevel": "",  // Maximum return cap level for the underlier.
        "digitalReturn": "",  // Indicates if the product provides a digital return.
        "digitalReturnBarrier": "",  // Barrier level for digital return.
        "digitalReturnBarrierObservationDateList": [],  // Observation dates for digital return barriers.
        "uncappedAboveDigitalReturn": "",  // Indicates if returns above the digital level are uncapped.
        "upsideParticipationAboveDigitalReturn": "",  // Participation rate above the digital return.
        "absoluteReturnBarrierLevel": "",  // Barrier level for absolute return.
        "maximumReturn": "",  // Maximum return level of the product.
        "growthType": [],  // List of growth types (e.g., capped, uncapped).
        "bearish": ""  // Indicates if the product has bearish exposure.
    },
    "estimatedValue": ""  // The estimated value of the product.
}
