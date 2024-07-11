# container2/app.py
from flask import Flask, request, jsonify
import csv
import os
from collections import OrderedDict

app = Flask(__name__)

@app.route('/sum', methods=['POST'])
def sum_product():
    data = request.json
    file_name = data['file']
    product = data['product']
    print("entered service 2")
    
    # Construct the file path relative to current directory
    file_path = os.path.join('/judith_PV_dir/', file_name)
    # Check if the file exists
    if not os.path.exists(file_path):
        return jsonify(OrderedDict([("error", "File not found."), ("file", file_name)]))
    
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)

            # Check if the file is in CSV format by attempting to read the header
            try:
                header = next(reader)
            except Exception:
                return jsonify(OrderedDict([("error", "Input file not in CSV format."), ("file", file_name)]))
            
            # Check if the header contains 'product' and 'amount'
            if 'product' not in header or 'amount' not in header:
                return jsonify(OrderedDict([("error", "Input file not in CSV format."), ("file", file_name)]))
            
            # Reset reader to start from the beginning again and use DictReader for processing rows
            file.seek(0)
            reader = csv.DictReader(file)
            
            total_sum = 0
            for row in reader:
                # Check if each row contains the correct number of columns
                if len(row) != 2 or 'product' not in row or 'amount' not in row:
                    return jsonify(OrderedDict([("error", "Input file not in CSV format."), ("file", file_name)]))
                
                # Validate if the 'amount' field can be converted to an integer
                try:
                    if row['product'] == product:
                        total_sum += int(row['amount'])
                except ValueError:
                    return jsonify(OrderedDict([("error", "Input file not in CSV format."), ("file", file_name)]))
            
            return {"file": file_name, "sum": total_sum}
    
    except Exception as e:
        return jsonify(OrderedDict([("error", "Input file not in CSV format."), ("file", file_name)]))

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=7000)