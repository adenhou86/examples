import pandas as pd

# Sample data (replace this with your actual data)
data = {
    'BANK OF AMERICA CORP DE': [
        {'DocId': '33971020', 'AsOfDate': '2024-04-30', 'Company': 'BANK OF AMERICA CORP DE', 'FileName': '10-Q 20240430.pdf', 'DocumentType': 'Filing10Q', 'fiscal_period': '2024-04', 'extracted_data': '181,553'},
        {'DocId': '36979217', 'AsOfDate': '2024-07-30', 'Company': 'BANK OF AMERICA CORP DE', 'FileName': '10-Q 20240730.pdf', 'DocumentType': 'Filing10Q', 'fiscal_period': '2024-07', 'extracted_data': '208,693'},
        {'DocId': '38637988', 'AsOfDate': '2024-10-29', 'Company': 'BANK OF AMERICA CORP DE', 'FileName': '10-Q 20241029.pdf', 'DocumentType': 'Filing10Q', 'fiscal_period': '2024-10', 'extracted_data': '232,010'}
    ],
    'JPMORGAN CHASE & CO': [
        {'DocId': '33987125', 'AsOfDate': '2024-05-01', 'Company': 'JPMORGAN CHASE & CO', 'FileName': '10-Q 20240501.pdf', 'DocumentType': 'Filing10Q', 'fiscal_period': '2024-05', 'extracted_data': '140,677'},
        {'DocId': '37039970', 'AsOfDate': '2024-08-02', 'Company': 'JPMORGAN CHASE & CO', 'FileName': '10-Q 20240802.pdf', 'DocumentType': 'Filing10Q', 'fiscal_period': '2024-08', 'extracted_data': '143,925'},
        {'DocId': '38655173', 'AsOfDate': '2024-10-30', 'Company': 'JPMORGAN CHASE & CO', 'FileName': '10-Q 20241030.pdf', 'DocumentType': 'Filing10Q', 'fiscal_period': '2024-10', 'extracted_data': '179,277'}
    ]
}

# Dictionary to store dataframes
dataframes = {}

for company, records in data.items():
    # Convert to DataFrame and sort by 'AsOfDate'
    df = pd.DataFrame(records)
    df['AsOfDate'] = pd.to_datetime(df['AsOfDate'])
    df['extracted_data'] = df['extracted_data'].str.replace(',', '').astype(int)
    df = df.sort_values(by='AsOfDate')
    
    # Calculate change from previous quarter
    df['change_from_prev_qtr'] = df['extracted_data'].diff()
    
    # Create new DataFrame with required format
    final_df = pd.DataFrame({
        'Items in a Fair value hedged relationship': df['extracted_data'].values,
        'Change from prev qtr': df['change_from_prev_qtr'].values
    }, index=['Items in a Fair value hedged relationship', 'Change from prev qtr'])
    
    # Store in dictionary
    dataframes[company] = final_df
    
    # Display the DataFrame
    import ace_tools as tools
    tools.display_dataframe_to_user(name=company, dataframe=final_df)
