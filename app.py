import streamlit as st
import pandas as pd

# Title of the app
st.title("Upload File 1")

# Button to upload the file
uploaded_file = st.file_uploader("Choose a file", type=["xlsx", "csv"])

# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the file based on its type
    try:
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)

        # Display the uploaded file content
        st.write("File Uploaded Successfully!")
        st.dataframe(df)
    except Exception as e:
        st.write("Error:", e)
else:
    st.write("Please upload a file.")
