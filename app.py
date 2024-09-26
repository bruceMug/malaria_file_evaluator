import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the original file
original_file = pd.read_csv('Test.csv')

# Function to check the uploaded file
def check_uploaded_file(uploaded_file):
    # Check if the number of columns is the same
    if len(uploaded_df.columns) != len(original_file.columns):
        return f"Error: The number of columns in the uploaded file does not match the Test.csv file. Test file has {len(original_file.columns)} columns while your file has {len(uploaded_df.columns)} columns."
    
    # Check if the column names are the same
    if list(uploaded_df.columns) != list(original_file.columns):
        return f"Error: The column names in the uploaded file do not match the Test.csv file. Test file has columns {list(original_file.columns)} while your file has columns {list(uploaded_df.columns)}."
    
    # Check if the number of unique rows in 'Image_ID' column is the same
    if uploaded_df['Image_ID'].nunique() != original_file['Image_ID'].nunique():
        missing_ids = set(original_file['Image_ID']) - set(uploaded_df['Image_ID'])
        return f"Error: The number of unique images in the 'Image_ID' column does not match the Test file. Test.csv has {original_file['Image_ID'].nunique()} unique images while your file has {uploaded_df['Image_ID'].nunique()} unique images. Missing images: {missing_ids}"
    
    # If all checks pass, return None
    return None

# Function to display statistics for the uploaded file
def display_statistics(uploaded_df):
    st.write(f"Number of rows: {len(uploaded_df)}")
    st.write("Number of unique classes in 'class' column and their counts:")
    st.write(uploaded_df['class'].value_counts())

    # Display confidence value distribution
    fig, ax = plt.subplots()
    uploaded_df['confidence'].hist(bins=10, ax=ax)
    ax.set_xlabel('Confidence')
    ax.set_ylabel('Count')
    ax.set_title('Distribution of Confidence Values')
    st.pyplot(fig)

st.title("Malaria Challenge File Evaluator")
st.image('header.png', use_column_width=True)
st.write("Before one submits a submission.csv to zindi for the challenge. Run the file through this application and if it passes all the tests, then you are good to go. ")
st.write("The application will check for the following: ")
st.write("1. The file should have the same number of columns as the test data")
st.write("2. The file should have the same column names as the test data")
st.write("3. The file should have the same number of unique values as the test data. !important")

st.write("")
st.write("Upload a file for processing")

uploaded_file = st.file_uploader("Choose a file", type=["csv"])

if uploaded_file is not None:
    with st.spinner("Processing your file..."):
        try:
            uploaded_df = pd.read_csv(uploaded_file)
            error_message = check_uploaded_file(uploaded_file)
            if error_message:
                st.error(error_message)
            else:
                display_statistics(uploaded_df)
                st.success("All tests passed. Submit to the zindi platform at `https://zindi.africa/competitions/lacuna-malaria-detection-challenge/submissions`")
        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")