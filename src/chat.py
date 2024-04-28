# libraries   
import warnings
warnings.filterwarnings("ignore")

from sqlalchemy import create_engine

from langchain import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import OpenAI
from langchain_openai.chat_models import ChatOpenAI   

import pandas as pd

import argparse
from tools import logger
import os                          
from dotenv import load_dotenv  

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


LANGUAGE = "mysql+pymysql"
USER = "root"
PASSWORD = "password"
SERVER = "localhost:3306"
DATABASE = "sakila"


URI = f"{LANGUAGE}://{USER}:{PASSWORD}@{SERVER}/{DATABASE}"


# query argparsing
argparser = argparse.ArgumentParser(description="User Question")
argparser.add_argument("-p", "--prompt", type=str, help="User query input")
parse_args = argparser.parse_args()
prompt = parse_args.prompt




def get_sql_response(prompt: str) -> str:

    """
    Function for automate SQL queries.

    Params: promt , string, our question

    Return: string, chat response
    """

    global OPENAI_API_KEY, URI

    logger.info("SQL Connection")
    cursor = create_engine(URI).connect()

    logger.info("Extracting tables...")
    tables = cursor.execute("show tables;").fetchall()
    tables = [e[0] for e in tables]

    logger.info("Generating SQL query...")
    db = SQLDatabase.from_uri(URI,
                            sample_rows_in_table_info=1, 
                            include_tables=tables)

    input_model = OpenAI(temperature=0)


    database_chain = create_sql_query_chain(input_model, db)

    sql_query = database_chain.invoke({"question": prompt})

    logger.info("SQL Querying...")
    response = cursor.execute(sql_query).fetchall()

    context = pd.DataFrame(response).to_markdown()

    logger.info("Generating final response...")
    output_model = ChatOpenAI(model="gpt-4-turbo")

    final_prompt = f"""Given the next context, answer the cuestion: 
                    
                   context: {context}, 
                    
                   question: {prompt}
                    
                   """
    
    return output_model.invoke(final_prompt).content



if __name__=="__main__":
    logger.info(f"Chat Response: {get_sql_response(prompt)}")