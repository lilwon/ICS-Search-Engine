from flask import Flask
app = Flask(__name__)

@app.route('/')
def search_page():
    return 'search page' 
