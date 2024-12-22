from flask import Flask, request, render_template, jsonify
import requests
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        fio = request.form['fio']
        annual_income = request.form['annual_income']
        age = request.form['age']
        num_bank_accounts = request.form['num_bank_accounts']
        outstanding_debt = request.form['outstanding_debt']

        client_id = str(uuid.uuid4())
        data = {
            'Client_id': client_id,
            'Annual_Income': annual_income,
            'Age': age,
            'Num_Bank_Accounts': num_bank_accounts,
            'Outstanding_Debt': outstanding_debt
        }

        response = requests.post('http://scoring:5001/predict', json=data)
        if response.status_code == 200:
            scoring_result = response.json()
            validation_response = requests.post('http://security:5002/validate', json={
                'fio': fio,
                'request': data,
                'response': scoring_result
            })
            if validation_response.status_code == 200:
                if scoring_result['credit_score'] == 1:
                    return render_template('index.html', credit_score= "Поздравляем, вам одобрен кредит")
                else:
                    return render_template('index.html', credit_score="Извините, выдача кредита отклонена")
            else:
                return render_template('index.html', error_message="Извините, ваш запрос завершился с ошибкой, вам перезвонит специалист")
        else:
            return render_template('index.html', error_message="Извините, ваш запрос завершился с ошибкой, вам перезвонит специалист")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)