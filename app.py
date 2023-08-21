from flask import Flask, request, jsonify, send_file
import csv
import subprocess
import os

app = Flask(__name__)

# Define your script and CSV filenames
SCRIPT_FILENAME = 'main.py'
CSV_FILENAME = 'datos_tiempo.csv'
MAP_FILENAME = 'index.nginx-debian.html'

# Endpoint check API
@app.route('/', methods=['GET'])
def check_api():
    return jsonify({"message": "Welcome to the Weather API"}), 200

# Endpoint to run the script
@app.route('/run_script', methods=['GET'])
def run_script():
    try:
        subprocess.run(['python', SCRIPT_FILENAME], check=True)
        return jsonify({"message": "Script executed successfully."}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to get all data from csv and send in json format
@app.route('/get_all_data', methods=['GET'])
def get_all_data():
    try:
        data_list = []
        with open(CSV_FILENAME, 'r', encoding='iso-8859-1') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            for row in csv_reader:
                data_list.append(row)
        return jsonify(data_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to get data for a specific number of locations
@app.route('/get_data_by_count/<int:num_locations>', methods=['GET'])
def get_data_by_count(num_locations):
    try:
        with open(CSV_FILENAME, 'r') as file:
            lines = file.readlines()
            data = lines[:num_locations + 1]  # Include header and the specified number of data lines
        return jsonify({"data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to get final static .html map 
@app.route('/get_map', methods=['GET'])
def get_map():
    try:
        return send_file(MAP_FILENAME, mimetype='text/html')
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)