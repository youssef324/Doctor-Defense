import hashlib
import os

# pyrefly: ignore [missing-import]
from cryptography.exceptions import InvalidSignature
# pyrefly: ignore [missing-import]
from cryptography.hazmat.primitives import hashes, serialization
# pyrefly: ignore [missing-import]
from cryptography.hazmat.primitives.asymmetric import padding, rsa
# pyrefly: ignore [missing-import]
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

PRIVATE_KEY = os.environ.get('PRIVATE_KEY')
PUBLIC_KEY = os.environ.get('PUBLIC_KEY')


def init_keys(instance_path):
    global PRIVATE_KEY, PUBLIC_KEY
    key_path = os.path.join(instance_path, 'private_key.pem')
    if os.path.exists(key_path):
        with open(key_path, 'rb') as f:
            PRIVATE_KEY = serialization.load_pem_private_key(f.read(), password=None)
    else:
        PRIVATE_KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        with open(key_path, 'wb') as f:
            f.write(
                PRIVATE_KEY.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )
    PUBLIC_KEY = PRIVATE_KEY.public_key()


def encrypt_file(data: bytes, password: str) -> bytes:
    salt = os.urandom(16)
    key = hashlib.scrypt(password.encode(), salt=salt, n=16384, r=8, p=1, dklen=32)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, data, None)
    return salt + nonce + ct


def decrypt_file(encrypted_data: bytes, password: str) -> bytes:
    salt = encrypted_data[:16]
    nonce = encrypted_data[16:28]
    ct = encrypted_data[28:]
    key = hashlib.scrypt(password.encode(), salt=salt, n=16384, r=8, p=1, dklen=32)
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ct, None)


def sign_document(data: bytes):
    digest = hashlib.sha256(data).digest()
    signature = PRIVATE_KEY.sign(
        digest,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return signature.hex(), digest.hex()


def verify_signature(data: bytes, signature_hex: str):
    try:
        signature = bytes.fromhex(signature_hex)
        digest = hashlib.sha256(data).digest()
        PUBLIC_KEY.verify(
            signature,
            digest,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except (InvalidSignature, ValueError):
        return False
