# # import streamlit as st
# # import requests
# # import json

# # st.title("Prediction Dashboard")
# # st.write("Enter a value to get prediction from FastAPI")

# # # Input from user
# # input_value = st.number_input(
# #     "Enter a numerical value:",
# #     min_value=0.0,
# #     max_value=1000.0,
# #     value=10.0,
# #     step=0.1
# # )

# # if st.button("Get Prediction"):
# #     try:
# #         # Call FastAPI endpoint
# #         response = requests.get(f"http://localhost:8000/predict/{input_value}")
        
# #         if response.status_code == 200:
# #             data = response.json()
            
# #             # Display results
# #             st.success("Prediction successful!")
# #             st.metric(
# #                 label="Predicted Value",
# #                 value=f"{data['prediction']:.4f}",
# #                 delta=f"Input: {data['input_value']}"
# #             )
            
# #             # Show raw JSON response
# #             with st.expander("View API Response"):
# #                 st.json(data)
                
# #         else:
# #             st.error(f"Error: {response.status_code} - {response.text}")
            
# #     except requests.exceptions.ConnectionError:
# #         st.error("Cannot connect to FastAPI server. Make sure it's running on localhost:8000")
# #     except Exception as e:
# #         st.error(f"An error occurred: {str(e)}")

# # # Add some styling
# # st.markdown("---")
# # st.info("Make sure FastAPI server is running on port 8000")

# import streamlit as st
# import requests
# import json
# import io

# st.title("Prediction Dashboard")
# st.write("Upload a file to get prediction from FastAPI")

# # File upload section
# uploaded_file = st.file_uploader(
#     "Choose a file to upload",
#     type=['csv', 'txt', 'json', 'png', 'jpg', 'jpeg'],  # Add relevant file types
#     help="Select a file to send to the prediction API"
# )

# if uploaded_file is not None:
#     # Display file information
#     st.write(f"**File name:** {uploaded_file.name}")
#     st.write(f"**File type:** {uploaded_file.type}")
#     st.write(f"**File size:** {uploaded_file.size} bytes")
    
#     # Preview the file content if it's text-based
#     if uploaded_file.type.startswith('text') or uploaded_file.name.endswith('.csv'):
#         try:
#             content = uploaded_file.getvalue().decode('utf-8')
#             st.text_area("File Preview", content, height=150)
#         except:
#             st.info("Cannot preview binary file content")

# if st.button("Get Prediction") and uploaded_file is not None:
#     try:
#         # Prepare the file for upload
#         files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        
#         # Call FastAPI endpoint with file upload
#         response = requests.post(
#             "http://localhost:8000/predict",
#             files=files
#         )
        
#         print(response.json())
#         # if response.status_code == 200:
#         #     data = response.json()
            
#         #     # Display results
#         #     st.success("Prediction successful!")
#         #     print(data)
#             # # Display prediction results in a more flexible way
#             # if isinstance(data, dict):
#             #     if 'prediction' in data:
#             #         st.metric(
#             #             label="Predicted Value",
#             #             value=f"{data['prediction']:.4f}",
#             #         )
#             #     # Display other relevant data from response
#             #     for key, value in data.items():
#             #         if key != 'prediction':
#             #             st.write(f"**{key}:** {value}")
#             # else:
#             #     st.write("**Response:**", data)
            
#             # # Show raw JSON response
#             # with st.expander("View API Response"):
#             #     st.json(data)
                
#         # else:
#         #     st.error(f"Error: {response.status_code} - {response.text}")
            
#     except requests.exceptions.ConnectionError:
#         st.error("Cannot connect to FastAPI server. Make sure it's running on localhost:8000")
#     except Exception as e:
#         st.error(f"An error occurred: {str(e)}")
# # elif st.button("Get Predictio") and uploaded_file is None:
# #     st.warning("Please upload a file first!")

# # Add some styling and information
# st.markdown("---")
# st.info("""
# **Instructions:**
# 1. Make sure FastAPI server is running on port 8000
# 2. Upload a file using the file uploader above
# 3. Click 'Get Prediction' to send the file to the API
# 4. The API should accept a form field named 'file'
# """)

# # Optional: Add a section to show how to test with sample data
# with st.expander("Need test files?"):
#     st.write("""
#     You can create sample files for testing:
#     - **CSV**: Create a simple CSV with data rows
#     - **TXT**: Plain text file with content
#     - **JSON**: Structured data in JSON format
#     """)

import streamlit as st
import requests
import pandas as pd

# Page configuration
st.set_page_config(page_title="Prediction Dashboard", layout="wide")
st.title("📊 Prediction Dashboard")
st.write("Upload a CSV file to get predictions from the ML model API.")

# File upload section
uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=['csv'],
    help="Select a CSV file to send to the prediction API"
)

# Initialize session state to hold prediction results
if 'prediction_data' not in st.session_state:
    st.session_state.prediction_data = None
if 'df_original' not in st.session_state:
    st.session_state.df_original = None

# If a file is uploaded, show its preview
if uploaded_file is not None:
    try:
        # Read the CSV file
        df_preview = pd.read_csv(uploaded_file)
        st.session_state.df_original = df_preview.copy()
        
        # Display file information and preview
        st.write(f"**File name:** {uploaded_file.name}")
        st.write(f"**Shape:** {df_preview.shape[0]} rows, {df_preview.shape[1]} columns")
        
        # Show preview in an expander
        with st.expander("📋 Preview Uploaded Data", expanded=True):
            st.dataframe(df_preview.head(), use_container_width=True)
            
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        st.stop()

# Prediction button
if st.button("🚀 Get Prediction", type="primary") and uploaded_file is not None:
    # Reset previous results
    st.session_state.prediction_data = None
    
    # Show a spinner while the request is being processed
    with st.spinner("Sending data to API and getting predictions..."):
        try:
            # Important: Reset the file pointer to the beginning
            uploaded_file.seek(0)
            
            # Prepare the file for upload
            files = {"file": (uploaded_file.name, uploaded_file, "text/csv")}
            
            # Call FastAPI endpoint
            response = requests.post(
                "http://localhost:8000/predict",
                files=files
            )
            
            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'success':
                    st.success("✅ Prediction successful!")
                    
                    # Store the prediction data in session state
                    st.session_state.prediction_data = data['predictions']
                    
                    # Show a preview of the results
                    df_with_predictions = pd.DataFrame(st.session_state.prediction_data)
                    with st.expander("👉 Quick Results Preview", expanded=True):
                        st.dataframe(df_with_predictions.head(), use_container_width=True)
                        
                else:
                    st.error(f"API returned an error: {data.get('detail', 'Unknown error')}")
                    
            else:
                st.error(f"❌ API Error ({response.status_code}): {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot connect to the API server. Please make sure it's running on `http://localhost:8000`")
        except Exception as e:
            st.error(f"⚠️ An unexpected error occurred: {str(e)}")

# Display detailed results if predictions are available
if st.session_state.prediction_data:
    st.markdown("---")
    st.header("📈 Prediction Results")
    
    # Convert prediction data to DataFrame
    results_df = pd.DataFrame(st.session_state.prediction_data)
    
    # Create tabs for different views of the results
    tab1, tab2, tab3 = st.tabs(["📊 Data Table", "📉 Summary Statistics", "⬇️ Download Results"])
    
    with tab1:
        st.subheader("Full Results Table")
        # Use st.dataframe for an interactive table
        st.dataframe(results_df, use_container_width=True, height=400)
        
        # Show some quick metrics if you have a predicted column
        if 'predicted_column' in results_df.columns:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Predictions", len(results_df))
            with col2:
                avg_pred = results_df['predicted_column'].mean()
                st.metric("Average Prediction", f"{avg_pred:.4f}")
            with col3:
                st.metric("Range", f"{results_df['predicted_column'].min():.4f} - {results_df['predicted_column'].max():.4f}")
    
    with tab2:
        st.subheader("Statistical Summary")
        # Show statistics for numerical columns
        st.write("**Numerical Columns Summary:**")
        st.dataframe(results_df.describe(), use_container_width=True)
        
        # If you have the original data, you could show a comparison here
    
    with tab3:
        st.subheader("Download Results")
        
        # Convert DataFrame to CSV
        csv = results_df.to_csv(index=False)
        
        st.download_button(
            label="📥 Download Predictions as CSV",
            data=csv,
            file_name="predictions_results.csv",
            mime="text/csv",
            help="Click to download the full results with predictions"
        )
        
        st.write("The downloaded file will contain all your original data plus the new 'predicted_column'.")

# Add sidebar with information
with st.sidebar:
    st.header("ℹ️ Instructions")
    st.markdown("""
    1. **Start the API Server**
       ```bash
       uvicorn your_backend_file:app --reload
       ```
       
    2. **Upload a CSV file** using the uploader above
       
    3. **Click 'Get Prediction'** to send the data to the API
       
    4. **View results** in the interactive table
       
    **Note:** The API must be running on `http://localhost:8000`
    """)
    
    st.header("🔧 Expected API Response")
    st.json({
        "status": "success",
        "predictions": [
            {"feature1": 1.0, "feature2": 2.0, "predicted_column": 0.75},
            {"feature1": 3.0, "feature2": 4.0, "predicted_column": 0.82}
        ]
    })

# Footer
st.markdown("---")
st.caption("Built with Streamlit • Connected to FastAPI ML Model")