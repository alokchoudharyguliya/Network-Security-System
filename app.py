import os,sys, certifi
cs=certifi.where()
from dotenv import load_dotenv
load_dotenv()
mongo_db_url=os.getenv("MONGO_DB_URI")
print(mongo_db_url)
import pymongo
from network_security.exception.exception import NetworkSecurityException
from network_security.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME,DATA_INGESTION_DATABASE_NAME
from network_security.logging.logger import logging as logger
from network_security.utils.ml_utils.model.estimator import NetworkModel
from network_security.pipeline.training_pipeline import TrainingPipeline
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request,HTTPException
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd


from network_security.utils.main_utils.utils import load_object
client=pymongo.MongoClient(mongo_db_url,tlsCAFile=cs)
database=client[DATA_INGESTION_DATABASE_NAME]
collection=database[DATA_INGESTION_COLLECTION_NAME]
app=FastAPI()
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        training_pipeline=TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Endpoint to receive a CSV file, make predictions using the trained model,
    and return the results as JSON.
    """
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400, 
            detail="Only CSV files are supported"
        )
    
    try:
        # Read the uploaded CSV file
        logger.info(f"Processing file: {file.filename}")
        df = pd.read_csv(file.file)
        
        # Log basic info about the received data
        logger.info(f"Received data shape: {df.shape}")
        logger.debug(f"Data columns: {list(df.columns)}")
        
        # Load the preprocessor and model
        logger.info("Loading preprocessor and model...")
        preprocessor = load_object("final_model/preprocessing.pkl")
        final_model = load_object("final_model/model.pkl")
        
        # Create network model and make predictions
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)
        logger.info("Making predictions...")
        
        y_pred = network_model.predict(df)
        
        # Add predictions to the dataframe
        df['predicted_column'] = y_pred
        
        # Log prediction summary
        logger.info(f"Predictions completed. Shape: {y_pred.shape}")
        logger.debug(f"Prediction range: {y_pred.min():.4f} - {y_pred.max():.4f}")
        
        # Convert DataFrame to JSON-serializable format
        # 'orient='records'' creates a list of dictionaries, perfect for JSON response
        predictions_data = df.to_dict(orient='records')
        
        # Prepare success response
        response_data = {
            "status": "success",
            "filename": file.filename,
            "data_shape": {
                "rows": df.shape[0],
                "columns": df.shape[1],
                "columns_with_predictions": df.shape[1]  # +1 for the new predicted_column
            },
            "prediction_stats": {
                "min": float(y_pred.min()),
                "max": float(y_pred.max()),
                "mean": float(y_pred.mean()),
                "std": float(y_pred.std())
            },
            "predictions": predictions_data
        }
        
        logger.info(f"Successfully processed {len(predictions_data)} records")
        return response_data
        
    except pd.errors.EmptyDataError:
        logger.error("Uploaded CSV file is empty")
        raise HTTPException(status_code=400, detail="The CSV file is empty")
        
    except pd.errors.ParserError:
        logger.error("Uploaded file is not a valid CSV")
        raise HTTPException(status_code=400, detail="Invalid CSV format")
        
    except FileNotFoundError as e:
        logger.error(f"Model file not found: {e}")
        raise HTTPException(
            status_code=500,
            detail="Model files not found. Please ensure the model is properly deployed."
        )
        
    except Exception as e:
        logger.error(f"Unexpected error during prediction: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during prediction: {str(e)}"
        )
# async def predict(request:Request,file:UploadFile=File(...)):
#     try:
#         df=pd.read_csv(file.file)
#         preprocessor=load_object("final_model/preprocessing.pkl")
#         final_model=load_object("final_model/model.pkl")
#         network_model=NetworkModel(preprocessor=preprocessor,model=final_model)
#         print(df.iloc[0])
#         y_pred=network_model.predict(df)
#         print(y_pred)
#         df['predicted_column']=y_pred
#         print(df["predicted_column"])
#         # df.to_csv("prediction/output.csv")
#         table_html=df.to_html(classes="table table-striped")

#         # return templates.TemplateResponse("table.html",{"request":request,"table":table_html})
        
#     except Exception as e:
#         raise NetworkSecurityException(e,sys)
 
if __name__=="__main__":
    app_run(app,host="localhost",port=8000)