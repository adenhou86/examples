import streamlit as st
import pandas as pd
import io
import json

# Set Streamlit page layout for wide display
st.set_page_config(page_title="Financial Data Dashboard", layout="wide")

# Load document information from JSON file
try:
    with open('doc_info.json', 'r') as f:
        doc_info = json.load(f)
except FileNotFoundError:
    st.error("doc_info.json file not found. Please ensure the file exists in the same directory.")
    st.stop()

# Function to format date string
def format_date_str(date_str):
    # Convert '2024-04-30' to '2024-04'
    return date_str[:7]

# File Upload
uploaded_file = st.file_uploader("Upload an Excel File (.xlsx)", type=["xlsx"])

if uploaded_file:
    # Load the Excel file and read all sheets
    if "sheets_data" not in st.session_state:
        st.session_state.sheets_data = pd.read_excel(uploaded_file, sheet_name=None, engine="openpyxl")
    
    company_names = list(st.session_state.sheets_data.keys())

    # Initialize session state for company status tracking
    if "company_status" not in st.session_state:
        st.session_state.company_status = {company: "" for company in company_names}

    # Ensure the current index is tracked
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0

    # Get the current company
    current_company = company_names[st.session_state.current_index]

    # Sidebar for displaying company list and navigation
    st.sidebar.title("Companies")
    for company in company_names:
        status = st.session_state.company_status[company]
        # Display company name with status
        status_icon = "✅" if status == "✔" else "❌" if status == "✘" else ""
        st.sidebar.markdown(f"- {company} {status_icon}")
        
        # Add dynamic document links if company exists in doc_info
        if company in doc_info:
            links_html = ""
            for doc in doc_info[company]:
                date = format_date_str(doc['AsOfDate'])
                page_links = ' | '.join([f'<a href="https://example.com/doc/{doc["DocId"]}/page/{p}">p. {p}</a>' for p in doc['pages_nb']])
                links_html += f'&nbsp;&nbsp;&nbsp;• <a href="https://example.com/doc/{doc["DocId"]}">{date}</a> [{page_links}]<br>'
            
            if links_html:
                st.sidebar.markdown(links_html, unsafe_allow_html=True)

    # Main Title
    st.title(f"Financial Data for {current_company}")

    # Get data for the current company
    data = st.session_state.sheets_data[current_company].copy()
    
    # Create a dictionary of column configurations
    column_config = {col: st.column_config.NumberColumn(col, default=0.0) 
                    for col in data.columns 
                    if data[col].dtype in ['float64', 'int64']}
    
    # Add text column configurations for non-numeric columns
    for col in data.columns:
        if col not in column_config:
            column_config[col] = st.column_config.TextColumn(col, default="")

    # Display editable DataFrame with column configuration
    edited_df = st.data_editor(
        data,
        use_container_width=True,
        num_rows="dynamic",
        column_config=column_config,
        key=f"editor_{current_company}",
        hide_index=True
    )

    # Store the edited data back in session state
    st.session_state.sheets_data[current_company] = edited_df

    # Buttons for "Incorrect", "Validate", and "Export All Data" centered
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        if st.button("❌ Incorrect", type="primary", key="incorrect_button"):
            # Save the edited data
            st.session_state.sheets_data[current_company] = edited_df
            # Mark the current company as incorrect
            st.session_state.company_status[current_company] = "✘"
            # Move to the next company
            st.session_state.current_index = (st.session_state.current_index + 1) % len(company_names)
            st.experimental_rerun()
    with col2:
        if st.button("✅ Validate", key="validate_button"):
            # Save the edited data
            st.session_state.sheets_data[current_company] = edited_df
            # Mark the current company as validated
            st.session_state.company_status[current_company] = "✔"
            # Move to the next company
            st.session_state.current_index = (st.session_state.current_index + 1) % len(company_names)
            st.experimental_rerun()
    
    with col3:
        # Get only validated companies
        validated_companies = [company for company in company_names 
                             if st.session_state.company_status[company] == "✔"]
        
        if validated_companies:  # Only show export button if there are validated sheets
            # Create Excel file in memory
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                for company in validated_companies:
                    st.session_state.sheets_data[company].to_excel(writer, sheet_name=company, index=False)
            
            # Add download button for Excel file
            st.download_button(
                label="📥 Export All Data",
                data=output.getvalue(),
                file_name="validated_financial_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            # Display disabled button or message when no data is validated
            st.button("📥 Export All Data", disabled=True)

    # Summary Table
    st.markdown("---")
    st.subheader("Summary of User Confirmation")
    summary_data = pd.DataFrame({
        "10Q": company_names,
        "User Confirm": [st.session_state.company_status[company] for company in company_names]
    })

    # Apply custom formatting to add colors
    def color_status(val):
        if val == "✔":
            return "color: green; font-weight: bold;"
        elif val == "✘":
            return "color: red; font-weight: bold;"
        return ""

    st.dataframe(
        summary_data.style.applymap(color_status, subset=["User Confirm"]),
        use_container_width=True,
    )

else:
    st.info("Please upload an Excel file to start.")
