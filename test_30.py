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

# Initialize the dataframe storage
data = []
columns = ["Category"] + [f"Period_{i+1}" for i in range(len(string_list))]

# Process each block and structure it
for i, text in enumerate(string_list):
    current_category = None
    period_data = {}

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
                period_data[current_category] = None
            else:
                period_data[key] = float(value)

    # Merge the data into structured form
    if i == 0:
        data.append(["Proceeds from Sales", period_data.get("HTM", None), period_data.get("AFS", None)])
        data.append(["Proceeds from Paydowns and Maturities", period_data.get("HTM", None), period_data.get("AFS", None)])
        data.append(["Purchases", period_data.get("HTM", None), period_data.get("AFS", None)])
    else:
        data[0].append(period_data.get("HTM", None))
        data[0].append(period_data.get("AFS", None))
        data[1].append(period_data.get("HTM", None))
        data[1].append(period_data.get("AFS", None))
        data[2].append(period_data.get("HTM", None))
        data[2].append(period_data.get("AFS", None))

# Convert the structured data to a DataFrame
df_final = pd.DataFrame(data, columns=columns)

# Display the DataFrame
import ace_tools as tools
tools.display_dataframe_to_user(name="Consolidated Financial Data", dataframe=df_final)
