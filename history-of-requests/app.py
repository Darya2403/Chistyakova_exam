from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/add_to_history', methods=['POST'])
def add_to_history():
    data = request.json
    with open('requests_log.txt', 'a') as f:
        f.write(str(data) + '\n')
    return jsonify({'message': 'Log entry added'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
