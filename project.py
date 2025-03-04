import pandas as pd

# Assuming the DataFrame is named df
# Example DataFrame creation (replace this with your actual DataFrame)
data = {
    'doc_id': [41824151, 41824217, 41824298, 41824311, 41824363, 41824625, 41824633, 41824654, 41824656, 41824659],
    'question': ['What is the client legal name?', 'What is the client legal name?', 'What is the client legal name?', 'What is the client legal name?', 'What is the client legal name?', 
                  "Could you state 'Yes' or 'No' to indicate if t...", "Could you state 'Yes' or 'No' to indicate if t...", "Could you state 'Yes' or 'No' to indicate if t...", 
                  "Could you state 'Yes' or 'No' to indicate if t...", "Could you state 'Yes' or 'No' to indicate if t..."],
    'answer': ['NOT_FOUND', 'Eze Castle Software LLC', 'MELLON ALPHAEQUITY UK FUND, LTD.', 'NOT_FOUND', 'OVT Fund LP', 
               'Yes, the client\'s affiliates are covered by th...', 'NOT_FOUND', 'Yes', 'No', 'NOT_FOUND'],
    'topic': ['Client Legal Name', 'Client Legal Name', 'Client Legal Name', 'Client Legal Name', 'Client Legal Name', 
              'Clients Affiliates Covered', 'Clients Affiliates Covered', 'Clients Affiliates Covered', 'Clients Affiliates Covered', 'Clients Affiliates Covered']
}

df = pd.DataFrame(data)

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('output.xlsx', engine='openpyxl')

# Group by the 'topic' column and write each group to a separate sheet
for topic, group in df.groupby('topic'):
    # Limit sheet name to the first 20 characters
    sheet_name = topic[:20]
    group.to_excel(writer, sheet_name=sheet_name, index=False)
    
    # Access the worksheet to adjust column widths
    worksheet = writer.sheets[sheet_name]
    worksheet.column_dimensions['A'].width = 15  # doc_id
    worksheet.column_dimensions['B'].width = 50  # question
    worksheet.column_dimensions['C'].width = 20  # topic

# Save the Excel file
writer.save()
