from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import render_template
import budget

app = Flask(__name__)
CORS(app)

@app.route ('/')
def index():
    return render_template('index.html')

@app.route ('/api/status', methods=['GET'])
def home():
    return jsonify({"message": "Budget API is running successfully!"})

if __name__ == '__main__':
    app.run(debug=True)

