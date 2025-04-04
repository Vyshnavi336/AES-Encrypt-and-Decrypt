from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

app = Flask(__name__)
CORS(app)

def encrypt(plain_text, key):
    key = key.encode()
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    encrypted_bytes = cipher.encrypt(pad(plain_text.encode(), AES.block_size))
    return base64.b64encode(iv + encrypted_bytes).decode()

def decrypt(encrypted_text, key):
    key = key.encode()
    encrypted_data = base64.b64decode(encrypted_text)
    iv = encrypted_data[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_bytes = unpad(cipher.decrypt(encrypted_data[AES.block_size:]), AES.block_size)
    return decrypted_bytes.decode()

# 🌐 Serve HTML file
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encrypt')
def encrypt_page():
    return render_template('encrypt.html')

@app.route('/decrypt')
def decrypt_page():
    return render_template('decrypt.html')


# 🔐 Encrypt endpoint
@app.route('/encrypt', methods=['POST'])
def encrypt_api():
    data = request.get_json()
    message = data.get('message')
    key = data.get('key')

    if not key or len(key) not in [16, 24, 32]:
        return jsonify({"error": "Key must be 16, 24, or 32 characters long."}), 400
    try:
        encrypted = encrypt(message, key)
        return jsonify({"encrypted": encrypted})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔓 Decrypt endpoint
@app.route('/decrypt', methods=['POST'])
def decrypt_api():
    data = request.get_json()
    encrypted = data.get('encrypted')
    key = data.get('key')

    if not key or len(key) not in [16, 24, 32]:
        return jsonify({"error": "Key must be 16, 24, or 32 characters long."}), 400
    try:
        decrypted = decrypt(encrypted, key)
        return jsonify({"decrypted": decrypted})
    except Exception as e:
        return jsonify({"error": "Decryption failed. Please check the key and input."}), 500

if __name__ == '__main__':
    app.run(debug=True)
