# # container2/app.py
# from flask import Flask, request, jsonify
# import csv
# import os
# from collections import OrderedDict

# app = Flask(__name__)

# @app.route('/sum', methods=['POST'])
# def sum_product():
#     data = request.json
#     file_name = data['file']
#     product = data['product']
    
#     # Construct the file path relative to current directory
#     file_path = os.path.join('/judith_PV_dir', file_name)
#     # Check if the file exists
#     if not os.path.exists(file_path):
#         return jsonify(OrderedDict([("error", "File not found."), ("file", file_name)]))
    
#     try:
#         with open(file_path, 'r') as file:
#             reader = csv.reader(file)

#             # Check if the file is in CSV format by attempting to read the header
#             try:
#                 header = next(reader)
#             except Exception:
#                 return jsonify(OrderedDict([("error", "Input file not in CSV format."), ("file", file_name)]))
            
#             # Check if the header contains 'product' and 'amount'
#             if 'product' not in header or 'amount' not in header:
#                 return jsonify(OrderedDict([("error", "Input file not in CSV format."), ("file", file_name)]))
            
#             # Reset reader to start from the beginning again and use DictReader for processing rows
#             file.seek(0)
#             reader = csv.DictReader(file)
            
#             total_sum = 0
#             for row in reader:
#                 # Check if each row contains the correct number of columns
#                 if len(row) != 2 or 'product' not in row or 'amount' not in row:
#                     return jsonify(OrderedDict([("error", "Input file not in CSV format."), ("file", file_name)]))
                
#                 # Validate if the 'amount' field can be converted to an integer
#                 try:
#                     if row['product'] == product:
#                         total_sum += int(row['amount'])
#                 except ValueError:
#                     return jsonify(OrderedDict([("error", "Input file not in CSV format."), ("file", file_name)]))
            
#             return {"file": file_name, "sum": total_sum}
    
#     except Exception as e:
#         return jsonify(OrderedDict([("error", "Input file not in CSV format."), ("file", file_name)]))

# if __name__ == '__main__':
#     app.run(host="0.0.0.0",port=7000)

from flask import Flask, request, jsonify
import os
import csv
import re

app = Flask(__name__)
port = 7000

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        inputJSON = request.json;
        fileName = inputJSON.get('file')
        inputProduct = inputJSON.get('product')
        print(fileName, inputProduct)
        #parent_dir = os.path.dirname(app.root_path)  # Get the parent directory of the application root
        file_path = os.path.join("/judith_PV_dir", fileName)
        print('filepath in container2', file_path)
        #return jsonify({"file": fileName, "path exists": os.path.exists(file_path)})
        #return jsonify(response.json())
        with open(file_path, 'r') as file:
            sum = 0
            for line_number, line in enumerate(file, start=2):
                parts = line.strip().split(",")
                if len(parts) != 2:
                    return jsonify({"file": fileName, "error": "Input file not in CSV format."})
                else:
                    product, amount = parts
                    if product == inputProduct:
                        sum += int(amount.strip())
            print('file', fileName, 'sum', sum)
            return jsonify({"file": fileName, "sum": sum})
    except:
        return jsonify({"file": fileName, "error": "Input file not in CSV format."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)