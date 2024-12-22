#Пример curl для вызова смены модели
#curl -X POST http://localhost:5002/change_model \
     #-H "Content-Type: application/json" \
     #-d '{"fio": "John Doe", "hash_sum": "abc123"}'


from flask import Flask, request, jsonify, render_template
import hashlib
from datetime import datetime
import uuid
import tempfile
import os
import requests
import ast

app = Flask(__name__)

# Функция для чтения данных из файла
def read_file(file_path, encoding='utf-8'):
    with open(file_path, 'r') as f:
        return [ast.literal_eval(line.strip()) for line in f.readlines()]

# Функция для записи данных в файл
def write_file(file_path, data):
    with open(file_path, 'a') as f:
        f.write(str(data) + '\n')

# Функция для обновления строки в файле
def update_line_in_file(file_path, request_id, new_data, encoding='utf-8'):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding=encoding) as temp_file:
        for line in lines:
            change = ast.literal_eval(line.strip())
            if change['request_id'] == request_id:
                temp_file.write(str(new_data) + '\n')
            else:
                temp_file.write(line)
        temp_file_path = temp_file.name
    os.replace(temp_file_path, file_path)

# Функция для записи ошибок в файл
def log_error(message):
    with open('error.txt', 'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

# Чтение данных из файла validated_models.txt
validated_models = read_file('validated_models.txt', encoding='windows-1251')

@app.route('/', methods=['GET'])
def index():
    pending_changes = read_file('pending_changes.txt', encoding='windows-1251')
    return render_template('index.html', pending_changes=pending_changes)

@app.route('/validate', methods=['POST'])
def validate():
    validated_models = read_file('validated_models.txt', encoding='windows-1251')
    data = request.json
    hash_sum = data['response']['hash_sum']
    validation_status = 'Failed'
    if validated_models and any(model['hash_sum'] == hash_sum for model in validated_models[-2:]):
        data['validation_status'] = 'Success'
        response = requests.post('http://history-of-requests:5003/add_to_history', json=data)
        if response.status_code == 200:
            return jsonify({'message': 'All OK'}), 200
        else:
            log_error(f"{data}")
            return jsonify({'message': 'Failed to log request'}), 500
    else:
        data['validation_status'] = 'Hash sum mismatch'
        response = requests.post('http://history-of-requests:5003/add_to_history', json=data)
        if response.status_code == 200:
            log_error(f"{data}")
            return jsonify({'message': 'Hash sum mismatch'}), 400
        else:
            log_error(f"{data}")
            return jsonify({'message': 'Failed to log request'}), 500

@app.route('/change_model', methods=['POST'])
def change_model():
    data = request.json
    request_id = str(uuid.uuid4())
    change_request = {
        'fio': data['fio'],
        'hash_sum': data['hash_sum'],
        'request_id': request_id,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    write_file('pending_changes.txt', change_request)
    return jsonify({'message': 'Change request received'}), 200

@app.route('/apply_change', methods=['POST'])
def apply_change():
    request_id = request.form['request_id']
    fio = request.form['fio']
    pending_changes = read_file('pending_changes.txt')
    for change in pending_changes:
        if change['request_id'] == request_id:
            change['checked_by'] = fio
            change['check_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            change['approve'] = 1
            update_line_in_file('pending_changes.txt', request_id, change)
            validated_change = {
                'fio': change['fio'],
                'hash_sum': change['hash_sum'],
                'request_id': change['request_id'],
                'date': change['date'],
                'approved_by': fio,
                'approval_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            write_file('validated_models.txt', validated_change)
            return jsonify({'message': 'Change applied.'}), 200
    return jsonify({'message': 'Change not found.'}), 404

@app.route('/reject_change', methods=['POST'])
def reject_change():
    request_id = request.form['request_id']
    fio = request.form['fio']
    pending_changes = read_file('pending_changes.txt')
    for change in pending_changes:
        if change['request_id'] == request_id:
            change['checked_by'] = fio
            change['check_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            change['approve'] = 0
            update_line_in_file('pending_changes.txt', request_id, change)
            return jsonify({'message': 'Change rejected.'}), 200
    return jsonify({'message': 'Change not found.'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
