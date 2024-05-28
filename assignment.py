# 1. write a function yo encrypt data usig fernet in flaskfrom flask import Flask, request, jsonify
from cryptography.fernet import Fernet
from flask import *


app = Flask(__name__)

# Generate a key for Fernet encryption
# Note: In a real application, you should store this key securely and not generate it every time.
key = Fernet.generate_key()
cipher_suite = Fernet(key)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json.get('data', '')
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Encrypt the data
    encrypted_data = cipher_suite.encrypt(data.encode('utf-8'))
    
    return jsonify({"encrypted_data": encrypted_data.decode('utf-8')})

if __name__ == '__main__':
    app.run(debug=True)



# how do you decrypt data using fernet in flask
from flask import Flask, request, jsonify
from cryptography.fernet import Fernet

app = Flask(__name__)

# In a real application, you should securely store and retrieve this key.
# This key should be the same key used for encryption.
key = Fernet.generate_key()
cipher_suite = Fernet(key)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json.get('data', '')
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Encrypt the data
    encrypted_data = cipher_suite.encrypt(data.encode('utf-8'))
    
    return jsonify({"encrypted_data": encrypted_data.decode('utf-8')})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    encrypted_data = request.json.get('encrypted_data', '')
    
    if not encrypted_data:
        return jsonify({"error": "No encrypted data provided"}), 400
    
    try:
        # Decrypt the data
        decrypted_data = cipher_suite.decrypt(encrypted_data.encode('utf-8'))
        return jsonify({"decrypted_data": decrypted_data.decode('utf-8')})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
