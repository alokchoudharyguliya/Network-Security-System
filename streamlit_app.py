import streamlit as st
import requests
import json

st.title("Prediction Dashboard")
st.write("Enter a value to get prediction from FastAPI")

# Input from user
input_value = st.number_input(
    "Enter a numerical value:",
    min_value=0.0,
    max_value=1000.0,
    value=10.0,
    step=0.1
)

if st.button("Get Prediction"):
    try:
        # Call FastAPI endpoint
        response = requests.get(f"http://localhost:8000/predict/{input_value}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Display results
            st.success("Prediction successful!")
            st.metric(
                label="Predicted Value",
                value=f"{data['prediction']:.4f}",
                delta=f"Input: {data['input_value']}"
            )
            
            # Show raw JSON response
            with st.expander("View API Response"):
                st.json(data)
                
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to FastAPI server. Make sure it's running on localhost:8000")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Add some styling
st.markdown("---")
st.info("Make sure FastAPI server is running on port 8000")