import pandas as pd
import json

# Sample JSON data (replace this with your actual JSON data)
data = {
    "JPMORGAN CHASE & CO": {
        "2023": {
            "filing10Q": {
                "section_1": {
                    "28014733": {
                        "sales_afs": 34554,
                        "difference_sales_afs": 34554,
                        "paydowns_afs": 11018,
                        "difference_paydowns_afs": 11018,
                        "purchases_afs": -26490,
                        "difference_purchases_afs": -26490,
                        "paydowns_htm": 9258,
                        "difference_paydowns_htm": 9258,
                        "purchases_htm": 3621,
                        "difference_purchases_htm": 3621,
                        "page_number": 117,
                        "as_of_date": "2023-05-03"
                    },
                    "78655005": {
                        "sales_afs": 35221,
                        "difference_sales_afs": 35321,
                        "paydowns_afs": 23470,
                        "difference_paydowns_afs": 12452,
                        "purchases_afs": -52433,
                        "difference_purchases_afs": -25943,
                        "paydowns_htm": 13762,
                        "difference_paydowns_htm": 4504,
                        "purchases_htm": 4141,
                        "difference_purchases_htm": 520,
                        "page_number": 150,
                        "as_of_date": "2023-08-03"
                    }
                }
            }
        }
    }
}

import pandas as pd

# Your JSON structure (as example)
data = {"JPMORGAN CHASE & CO": {"2023": {"filing10Q": {"section_1": {"28014733": {"sales_afs": 34554,"difference_sales_afs": 34554,"paydowns_afs": 11018,"difference_paydowns_afs": 11018,"purchases_afs": -26490,"difference_purchases_afs": -26490,"paydowns_htm": 9258,"difference_paydowns_htm": 9258,"purchases_htm": 3621,"difference_purchases_htm": 3621,"page_number": 117,"as_of_date": "2023-05-03"},"78655005": {"sales_afs": 35221,"difference_sales_afs": 35321,"paydowns_afs": 24370,"difference_paydowns_afs": 12452,"purchases_afs": -52433,"difference_purchases_afs": -25943,"paydowns_htm": 13762,"difference_paydowns_htm": 4504,"purchases_htm": 4141,"difference_purchases_htm": 520,"page_number": 150,"as_of_date": "2023-08-03"}}}}}}

import pandas as pd

# JSON data (replace with your actual JSON loading method)
data = YOUR_JSON_DATA

# Convert nested JSON to DataFrame
sheet_name = "JPMORGAN CHASE & CO"
section_data = data[sheet_name]["2023"]["filing10Q"]["section_1"]

df = pd.DataFrame.from_dict(section_data, orient='index')

# Save DataFrame to Excel
excel_path = "jpmorgan_chase.xlsx"
with pd.ExcelWriter(excel_writer := 'output.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name=sheet_name)

print(f"Excel file saved with sheet '{sheet_name}'.")
