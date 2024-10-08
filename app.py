import streamlit as st
import pandas as pd

# Title of the app
st.title("Upload Files")

# Initialize an empty list to store uploaded files
uploaded_files = []

# Upload files until the user indicates they are done
uploaded_file = st.file_uploader("Upload a file", type=["xlsx", "csv"])

# Add the uploaded file to the list if it's not None
if uploaded_file is not None:
    uploaded_files.append(uploaded_file)

# Display the total number of uploaded files
st.write(f"Total files uploaded: {len(uploaded_files)}")

# Confirmation radio button to check if the user is done
confirmation = st.radio("Have you finished uploading files?", ("No", "Yes"))

if confirmation == "Yes":
    st.success("You have indicated that you have finished uploading files.")
    # Process each uploaded file
    for index, file in enumerate(uploaded_files, start=1):
        try:
            if file.name.endswith('.xlsx'):
                df = pd.read_excel(file, engine='openpyxl')
            elif file.name.endswith('.csv'):
                df = pd.read_csv(file)

            st.write(f"File {index} uploaded successfully!")
            st.dataframe(df)
        except Exception as e:
            st.write(f"Error with file {index}: {e}")
else:
    st.info("Please continue uploading files.")
