from cryptography.fernet import Fernet
import hashlib

def generate_key():
    return Fernet.generate_key()

def encrypt_message(message, key):
    f = Fernet(key)
    return f.encrypt(message.encode())

def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode()

def generate_hash(message):
    return hashlib.sha256(message.encode()).hexdigest()
