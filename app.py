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
    
    # Display a "Process" button after confirmation
    if st.button("Process"):
        st.write("Processing files...")
        processed_dfs = []  # List to store processed DataFrames
        common_header = None  # Variable to store the header

        # Process each uploaded file
        for index, file in enumerate(st.session_state['uploaded_files'], start=1):
            try:
                # Read the file
                if file.name.endswith('.xlsx'):
                    df = pd.read_excel(file, engine='openpyxl', header=None)
                elif file.name.endswith('.csv'):
                    df = pd.read_csv(file, header=None)

                # Find the header row containing 'No'
                header_row_index = df.apply(lambda row: row.astype(str).str.contains('No', case=False, na=False)).any(axis=1).idxmax()

                # Set the row as header
                if common_header is None:
                    common_header = df.iloc[header_row_index]  # Use this as the common header

                # Set the DataFrame columns and remove rows above the header
                df.columns = common_header
                df = df[header_row_index + 1:].reset_index(drop=True)

                # Remove empty columns
                df = df.dropna(axis=1, how='all')

                # Remove empty rows
                df = df.dropna(axis=0, how='all')

                processed_dfs.append(df)  # Store the processed DataFrame
                st.write(f"File {index} processed successfully!")

            except Exception as e:
                st.write(f"Error with file {index}: {e}")
        
        # Concatenate the processed DataFrames if there are any
        if processed_dfs:
            concatenated_df = pd.concat(processed_dfs, ignore_index=True)
            st.write("Displaying concatenated data:")
            st.dataframe(concatenated_df)
        else:
            st.write("No valid files were processed.")
else:
    st.info("Please continue uploading files.")
