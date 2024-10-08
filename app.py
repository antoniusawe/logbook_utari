import streamlit as st
import pandas as pd

# Title of the app
st.title("Upload File Logbook")

# Initialize session state for storing uploaded files
if 'uploaded_files' not in st.session_state:
    st.session_state['uploaded_files'] = []

# File uploader for uploading multiple files at once
uploaded_files = st.file_uploader("Upload files", type=["xlsx", "csv"], accept_multiple_files=True)

# Add the uploaded files to the session state if they are not already added
if uploaded_files:
    for uploaded_file in uploaded_files:
        if uploaded_file not in st.session_state['uploaded_files']:
            st.session_state['uploaded_files'].append(uploaded_file)

# Display the total number of uploaded files
st.write(f"Total file yang diupload: {len(st.session_state['uploaded_files'])}")

# Display each uploaded file for confirmation
if st.session_state['uploaded_files']:
    st.write("Uploaded files:")
    for i, file in enumerate(st.session_state['uploaded_files'], start=1):
        st.write(f"{i}. {file.name}")

# Confirmation radio button to check if the user is done
confirmation = st.radio("Apakah sudah selesai upload?", ("Belum", "Sudah"))

if confirmation == "Sudah":
    st.success("Anda sudah selesai melakukan upload semua file logbook.")
    
    # Display a "Process" button after confirmation
    if st.button("Proses"):
        st.write("File diproses...")
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

                # Set the row as header and clean the column names
                if common_header is None:
                    common_header = df.iloc[header_row_index].str.strip()  # Clean the header by stripping whitespace

                # Set the DataFrame columns and remove rows above the header
                df.columns = common_header
                df = df[header_row_index + 1:].reset_index(drop=True)

                # Remove empty columns
                df = df.dropna(axis=1, how='all')

                # Remove empty rows
                df = df.dropna(axis=0, how='all')

                # Clean and convert relevant columns to numeric (if they exist) for summing later
                columns_to_convert = ['Count', 'SUM Input From SRS', 'SUM Input From Confins']
                for col in columns_to_convert:
                    if col in df.columns:
                        # Remove any non-numeric characters (e.g., commas, spaces) and convert to numeric
                        df[col] = pd.to_numeric(df[col].astype(str).replace('[^0-9.-]', '', regex=True), errors='coerce')

                processed_dfs.append(df)  # Store the processed DataFrame
                st.write(f"File {index} processed successfully!")

            except Exception as e:
                st.write(f"Error with file {index}: {e}")
        
        # Concatenate the processed DataFrames if there are any
        if processed_dfs:
            concatenated_df = pd.concat(processed_dfs, ignore_index=True)

            # Remove the 'No' column if it exists
            if 'No' in concatenated_df.columns:
                concatenated_df = concatenated_df.drop(columns=['No'])

            st.write("Hasil penggabungan:")
            st.dataframe(concatenated_df)

            # Calculate and display the sum of the relevant columns
            total_count = concatenated_df['Count'].sum() if 'Count' in concatenated_df.columns else 0
            total_sum_srs = concatenated_df['SUM Input From SRS'].sum() if 'SUM Input From SRS' in concatenated_df.columns else 0
            total_sum_confins = concatenated_df['SUM Input From Confins'].sum() if 'SUM Input From Confins' in concatenated_df.columns else 0

            st.write("### Totals:")
            st.write(f"Total Count: {total_count}")
            st.write(f"Total SUM Input From SRS: {total_sum_srs}")
            st.write(f"Total SUM Input From Confins: {total_sum_confins}")
        else:
            st.write("Tidak ada file yang diproses.")
else:
    st.info("Silahkan upload file logbook.")
