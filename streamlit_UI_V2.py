import streamlit as st
import pandas as pd

# Set Streamlit page layout for wide display
st.set_page_config(page_title="Financial Data Dashboard", layout="wide")

# File Upload
uploaded_file = st.file_uploader("Upload an Excel File (.xlsx)", type=["xlsx"])

if uploaded_file:
    # Load the Excel file and read all sheets
    sheets_data = pd.read_excel(uploaded_file, sheet_name=None, engine="openpyxl")  # Load all sheets
    company_names = list(sheets_data.keys())  # List of sheet names (companies)

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
        if status == "✔":
            st.sidebar.markdown(f"- {company} ✅")
        elif status == "✘":
            st.sidebar.markdown(f"- {company} ❌")
        else:
            st.sidebar.markdown(f"- {company}")

    # Add Export Data button in the sidebar
    st.sidebar.markdown("---")
    st.sidebar.download_button(
        label="Export Data",
        data=sheets_data[current_company].to_csv(index=False).encode("utf-8"),
        file_name=f"{current_company}_financial_data.csv",
        mime="text/csv",
    )

    # Main Title
    st.title(f"Financial Data for {current_company}")

    # Get data for the current company
    data = sheets_data[current_company]
    data = data.fillna("")  # Replace NaN with empty strings

    # Custom CSS for centering elements
    st.markdown(
        """
        <style>
        .center-container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .centered-table {
            width: 70%;
        }
        .centered-buttons {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        .centered-buttons button {
            margin: 0 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Center the table and buttons
    st.markdown('<div class="center-container">', unsafe_allow_html=True)

    # Display the table centered
    st.markdown('<div class="centered-table">', unsafe_allow_html=True)
    st.dataframe(data, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Buttons for "Incorrect" and "Validate" centered
    st.markdown('<div class="centered-buttons">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Incorrect"):
            # Mark the current company as incorrect
            st.session_state.company_status[current_company] = "✘"
            # Move to the next company
            st.session_state.current_index = (st.session_state.current_index + 1) % len(company_names)
            st.experimental_rerun()
    with col2:
        if st.button("Validate"):
            # Mark the current company as validated
            st.session_state.company_status[current_company] = "✔"
            # Move to the next company
            st.session_state.current_index = (st.session_state.current_index + 1) % len(company_names)
            st.experimental_rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # Close the center-container div

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
