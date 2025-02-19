import pandas as pd

# List of string blocks
string_list = [
    """
    Proceeds from Sales:
    HTM:
    AFS: 61,211

    Proceeds from Paydowns and Maturities:
    HTM: 46,800
    AFS: 16,742

    Purchases:
    HTM: (1,034)
    AFS: (146,232)
    """,
    """
    Proceeds from Sales:
    HTM:
    AFS: 84,394

    Proceeds from Paydowns and Maturities:
    HTM: 72,354
    AFS: 22,409

    Purchases:
    HTM: (2,358)
    AFS: (233,063)
    """,
    """
    Proceeds from Sales:
    HTM: ($4,709)
    AFS: $104,625

    Proceeds from Paydowns and Maturities:
    HTM: $99,363
    AFS: $38,499

    Purchases:
    HTM: ($4,709)
    AFS: ($352,712)
    """
]

# Define column names dynamically based on the number of periods
columns = ["Category"] + [f"Period_{i+1}" for i in range(len(string_list))]

# Initialize storage for data
structured_data = {}

# Process each block and structure it
for i, text in enumerate(string_list):
    current_category = None

    for line in text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().replace(",", "").replace("(", "-").replace(")", "").replace("$", "")

            if value == "":
                current_category = key
                if current_category not in structured_data:
                    structured_data[current_category] = [None] * len(string_list)
            else:
                if key not in structured_data:
                    structured_data[key] = [None] * len(string_list)
                structured_data[key][i] = float(value)

# Convert the structured data into a DataFrame
df_fixed = pd.DataFrame.from_dict(structured_data, orient="index", columns=[f"Period_{i+1}" for i in range(len(string_list))])
df_fixed.reset_index(inplace=True)
df_fixed.rename(columns={"index": "Category"}, inplace=True)

# Display the DataFrame
import ace_tools as tools
tools.display_dataframe_to_user(name="Fixed Financial Data Table", dataframe=df_fixed)
