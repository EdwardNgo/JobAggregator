from flask import Flask, Blueprint, flash, g, redirect, render_template, request, url_for


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)