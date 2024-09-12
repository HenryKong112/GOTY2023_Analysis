from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine
import vader as v

# Load environment variables
load_dotenv()
SERVER = os.getenv("SERVER")
DATABASE = os.getenv("DATABASE")
USERNAME = os.getenv("UID")
PASSWORD = os.getenv("PWD")

# Create SQLAlchemy engine for connection to Azure SQL
connection_string = f'mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver=ODBC+Driver+18+for+SQL+Server'
engine = create_engine(connection_string)

# Assuming v.df_sentiment is a pandas DataFrame
# Replace `v.df_sentiment` with your DataFrame, if it is named differently
df_sentiment = v.df_sentiment  # Ensure this is a pandas DataFrame

# Write the DataFrame to the Azure SQL database
df_sentiment.to_sql('sentiment_comments', engine, if_exists='replace', index=False)
