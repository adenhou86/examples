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

data = []

# Process each block and structure it
for i, text in enumerate(string_list):
    current_data = {
        "Category": ["Proceeds from Sales:", "HTM", "AFS", "Proceeds from Paydowns and Maturities:", "HTM", "AFS", "Purchases:", "HTM", "AFS"]
    }
    period_key = f"Period_{i+1}"
    values = []

    for line in text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().replace(",", "").replace("(", "-").replace(")", "").replace("$", "")
            if value == "":
                values.append(None)
            else:
                values.append(float(value))
    
    data.append(values)

df_dynamic = pd.DataFrame(data).T
df_dynamic.columns = [f"period_{i+1}" for i in range(len(string_list))]
df_dynamic.insert(0, "Category", ["Proceeds from Sales:", "HTM", "AFS", "Proceeds from Paydowns and Maturities:", "HTM", "AFS", "Purchases:", "HTM", "AFS"])

import ace_tools as tools
tools.display_dataframe_to_user(name="Corrected Output", dataframe=df_dynamic)


# Compute the differences between periods and insert new columns dynamically
for i in range(1, len(string_list)):
    df_corrected.insert(
        i * 2, 
        f"diff_period_{i}_{i+1}", 
        df_corrected[f"period_{i+1}"].replace("", 0).astype(float) - df_corrected[f"period_{i}"].replace("", 0).astype(float)
    )

# Replace computed 0s for empty values where original columns were empty
df_corrected = df_corrected.astype(str).replace("0.0", "")

# Display the updated DataFrame
tools.display_dataframe_to_user(name="Final DataFrame with Differences", dataframe=df_corrected)


# Compute the sum for each AFS row across all columns
afs_sum = df_corrected[df_corrected["Category"] == "AFS"].drop(columns=["Category"]).replace("", 0).astype(float).sum()

# Convert to string and replace 0 with empty string
afs_sum = afs_sum.astype(str).replace("0.0", "")

# Create a new row for AFS total
afs_total_row = pd.DataFrame([["AFS Total"] + afs_sum.tolist()], columns=df_corrected.columns)

# Append the new row to the dataframe
df_corrected = pd.concat([df_corrected, afs_total_row], ignore_index=True)

# Display the updated DataFrame with the AFS sum row
tools.display_dataframe_to_user(name="Final DataFrame with AFS Sum", dataframe=df_corrected)

