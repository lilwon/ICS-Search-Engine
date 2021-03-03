from flask import Flask, request, redirect, render_template


app = Flask(__name__)

# GET - A GET msg is sent and server returns data
# POST -  Send HTML form data to server. Data received POST 
@app.route('/', methods=['GET', 'POST'])
def search_page():
    # create search form
    if request.method == 'POST':
        queries = request.form['query']


    return render_template("search_page.html")



# This is so you can just do py -3 webgui.py
if __name__ == '__main__':
    app.run(debug = True)