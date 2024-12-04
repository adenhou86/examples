import pandas as pd

def create_multi_sheet_excel(company_dataframes, output_file='financial_reports.xlsx'):
    # Create Excel writer object
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Iterate through each company and their data
        for company_name, df in company_dataframes.items():
            # Clean sheet name (Excel has 31 character limit for sheet names)
            sheet_name = company_name[:31]
            
            # Write the DataFrame to Excel
            df.to_excel(writer, sheet_name=sheet_name, index=True)
            
            # Get workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            
            # Format columns
            for idx, col in enumerate(df.columns):
                # Set column width based on maximum length in column
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(str(col))
                ) + 2
                worksheet.column_dimensions[chr(ord('B') + idx)].width = max_length
            
            # Set first column width (index)
            worksheet.column_dimensions['A'].width = 35
            
            # Format numbers
            for row in worksheet.iter_rows(min_row=2):  # Skip header
                for cell in row:
                    if isinstance(cell.value, (int, float)):
                        # Check if it's a negative number in parentheses
                        if isinstance(cell.value, str) and cell.value.startswith('('):
                            cell.value = float(cell.value.strip('()')) * -1
                        cell.number_format = '#,##0.000'

    print(f"Excel file '{output_file}' has been created with sheets for each company.")

# Example usage:
company_dataframes = {
    'BANK OF AMERICA CORP DE': pd.DataFrame({
        'category': ['Proceeds from Sales', '', '', 'Proceeds from Paydowns and Maturities', '', '', 'Purchases', '', '', '', 'Net', '', ''],
        '': ['', 'HTM', 'AFS', 'HTM', 'AFS', '', 'HTM', 'AFS', '', '', 'AFS', 'HTM', ''],
        '2024-04': ['', '', 16.266, 7.407, 82.080, '', 0, -157.726, '', '', -48.400, 7.407, ''],
        'Diff_2024-04_2024-07': ['', '', 8.183, 5.151, 95.458, '', 0, -82.020, '', '', 21.617, 5.151, ''],
        '2024-07': ['', '', 25.140, 9.465, 29.064, '', 0, -72.431, '', '', -15.207, 9.465, ''],
        'Diff_2024-07_2024-10': ['', '', 24.454, -16.568, 188.518, '', 0, -239.756, '', '', -20.783, 16.568, ''],
        '2024-10': ['', '', 52.504, 26.033, 217.602, '', 0, -312.195, '', '', -41.990, 26.033, '']
    }),
    'JPMORGAN CHASE & CO': pd.DataFrame({
        'category': ['Proceeds from Sales', '', '', 'Proceeds from Paydowns and Maturities', '', '', 'Purchases', '', '', '', 'Net', '', ''],
        '': ['', 'HTM', 'AFS', 'HTM', 'AFS', '', 'HTM', 'AFS', '', '', 'AFS', 'HTM', ''],
        '2024-05': ['', '', 28.451, 35.518, 10.356, '', -479, -75.265, '', '', -37.456, 35.039, ''],
        'Diff_2024-05_2024-08': ['', '', 32.760, 11.282, 6.386, '', -555, -69.967, '', '', -30.821, 10.727, ''],
        '2024-08': ['', '', 23.183, 25.554, 5.667, '', -1.324, -86.891, '', '', -57.981, '', ''],
        'Diff_2024-08_2024-10': ['', '', 61.211, 46.800, 16.742, '', -1.034, -146.232, '', '', -68.279, '', ''],
        '2024-10': ['', '', 84.394, 72.354, 22.409, '', -2.358, -233.063, '', '', -126.260, '', '']
    })
}

# Create the Excel file
create_multi_sheet_excel(company_dataframes)
