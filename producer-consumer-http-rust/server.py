from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

@app.route('/demo', methods=['GET', 'POST'])
def demo():
    print(request)
    req_json = request.get_json()
    print(f'request json: {req_json}')
    response_data = {
        "name": "xxx",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "id": 100
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
