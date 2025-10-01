from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
def generate_public_private_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return public_key,private_key

def public_key_to_bytes(public_key):
    public_pem = public_key.public_bytes(
       encoding=serialization.Encoding.PEM,
       format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return public_pem

def bytes_to_public_key(bytes):
    public_key_object_recreated = serialization.load_pem_public_key(
        bytes,
        backend=default_backend()
    )
    return public_key_object_recreated

    # 3. ENCRYPT THE MESSAGE WITH THE PUBLIC KEY
# The padding scheme used here MUST MATCH the one the server uses for decryption.

def encrypt_text( message , public_key):

    encrypted_message = public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_message

def decrypt_text(encrypted_message , private_key):
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_message