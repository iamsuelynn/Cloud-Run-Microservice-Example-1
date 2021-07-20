from flask import Flask, request, make_response, jsonify
import pandas as pd
import gcsfs
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas_gbq
import os

app = Flask(__name__)

app.config["DEBUG"] = True #If the code is malformed, there will be an error shown when visit app

@app.route("/books", methods=["GET"])
def books_table_update():
    
    Title = request.args.get('title', None)
    Author = request.args.get('author', None)

    input_table = {'book_title':[Title],'book_author':[Author]}
    input_table = pd.DataFrame(input_table)
    input_table["book_title"]= input_table["book_title"].map(str)
    input_table["book_author"]= input_table["book_author"].map(str)
    
    #Push table to Google Big Query

    client = bigquery.Client()
    project_id = 'sue-gcp-learning-env'
    table_id = 'Books.books_title_author'
    pandas_gbq.to_gbq(input_table, table_id, project_id=project_id, if_exists='append')
    
    return "Table books_title_author has been Updated"