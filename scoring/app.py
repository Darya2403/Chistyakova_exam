from flask import Flask, request, jsonify, render_template
import joblib
import hashlib
import requests

app = Flask(__name__)
model = joblib.load('logistic_regression_model.pkl')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = [
        float(data['Annual_Income']),
        float(data['Age']),
        float(data['Num_Bank_Accounts']),
        float(data['Outstanding_Debt'])
    ]
    prediction = model.predict([features])[0]
    hash_sum = hashlib.sha256(str(model.coef_).encode()).hexdigest()
    return jsonify({'credit_score': int(prediction), 'hash_sum': hash_sum})

@app.route('/change_model', methods=['GET', 'POST'])
def change_model():
    if request.method == 'POST':
        fio = request.form['fio']
        hash_sum = hashlib.sha256(str(model.coef_).encode()).hexdigest()
        response = requests.post('http://security:5002/change_model', json={
            'fio': fio,
            'hash_sum': hash_sum
        })
        if response.status_code == 200:
            return render_template('index.html', message="Model change request sent.")
        else:
            return render_template('index.html', message="Failed to send model change request.")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
