from flask import Flask, render_template, request, send_file
from crypto_utils import *
from stego_utils import *
import os

app = Flask(__name__)

KEY = generate_key()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    file = request.files['image']
    message = request.form['message']

    file_path = 'input.png'
    file.save(file_path)

    hash_val = generate_hash(message)
    full_message = message + "||" + hash_val

    encrypted = encrypt_message(full_message, KEY).decode()

    output_path = 'encoded.png'
    embed_data(file_path, encrypted, output_path)

    return send_file(output_path, as_attachment=True)

@app.route('/decode', methods=['POST'])
def decode():
    file = request.files['image']
    file_path = 'encoded.png'
    file.save(file_path)

    extracted = extract_data(file_path)
    decrypted = decrypt_message(extracted.encode(), KEY)

    message, hash_val = decrypted.split("||")

    if generate_hash(message) == hash_val:
        return f"Message: {message} (Integrity Verified)"
    else:
        return "Tampered Data!"

if __name__ == '__main__':
    app.run(debug=True)
