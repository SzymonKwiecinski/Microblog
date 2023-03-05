from flask import Flask, render_template, request
import os
import datetime
from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()

def create_app():

    app = Flask(__name__)

    # export FLASK_APP=app.py
    # export FLASK_DEBUG=1

    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.microblog

    @app.route("/", methods=["GET", "POST"])
    def home():
        
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            
            app.db.entries.insert_one(
                {
                    "content": entry_content,
                    "date": formatted_date
                }
            )
            
        entries_with_correct_data = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
                
            ) 
            for entry in app.db.entries.find({})
        ]
        

        return render_template('home.html', entries=entries_with_correct_data)

    return app