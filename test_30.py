import pandas as pd
import re

# Input data
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

# Function to clean and extract values
def extract_values(text):
    # Remove dollar signs, commas, and parentheses, and convert to integers
    text = re.sub(r'[,\$\(\)]', '', text)
    return int(text) if text.strip() else None  # Return None for empty values

# Initialize a dictionary to store the data
data = {
    "category": [],
    **{f"period_{i+1}": [] for i in range(len(string_list))}
}

# Extract all unique categories in order of appearance
categories = []
for text in string_list:
    lines = text.strip().split('\n')
    for line in lines:
        if ':' in line:
            category = line.split(':')[0].strip()
            if category not in categories:
                categories.append(category)

# Extract data for each period
for i, text in enumerate(string_list):
    lines = text.strip().split('\n')
    for category in categories:
        found = False
        for line in lines:
            if line.strip().startswith(category + ':'):
                value = line.split(':')[-1].strip()
                if i == 0:
                    data["category"].append(category)
                data[f"period_{i+1}"].append(extract_values(value))
                found = True
                break
        if not found:
            if i == 0:
                data["category"].append(category)
            data[f"period_{i+1}"].append(None)  # Append None for missing values

# Create DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
print(df)
