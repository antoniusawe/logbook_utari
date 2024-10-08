import streamlit as st
import pandas as pd

# Title of the app
st.title("Upload Multiple Files")

# Initialize session state for storing uploaded files
if 'uploaded_files' not in st.session_state:
    st.session_state['uploaded_files'] = []

# File uploader for uploading files one by one
uploaded_file = st.file_uploader("Upload a file", type=["xlsx", "csv"])

# Add the uploaded file to the session state if it's not already added
if uploaded_file is not None and uploaded_file not in st.session_state['uploaded_files']:
    st.session_state['uploaded_files'].append(uploaded_file)

# Display the total number of uploaded files
st.write(f"Total files uploaded: {len(st.session_state['uploaded_files'])}")

# Display each uploaded file for confirmation
if st.session_state['uploaded_files']:
    st.write("Uploaded files:")
    for i, file in enumerate(st.session_state['uploaded_files'], start=1):
        st.write(f"{i}. {file.name}")

# Confirmation radio button to check if the user is done
confirmation = st.radio("Have you finished uploading files?", ("No", "Yes"))

if confirmation == "Yes":
    st.success("You have indicated that you have finished uploading files.")
    # Process each uploaded file
    for index, file in enumerate(st.session_state['uploaded_files'], start=1):
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
