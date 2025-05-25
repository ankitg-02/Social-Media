from flask import Flask, render_template, redirect, url_for
import webbrowser
import threading
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    os.system("python app.py")
    return "Redirecting to dashboard..."

@app.route('/predict')
def predict():
    threading.Thread(target=lambda: os.system("streamlit run pred_app.py")).start()
    return "Opening prediction app..."

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=True)
