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
    """
    Initialize RSA keys for document signing and verification.
    
    Generates a 2048-bit RSA key pair if it doesn't exist.
    Private key is stored in PEM format in the instance directory.
    
    Args:
        instance_path: Directory to store keys
    """
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
        # Secure file permissions: readable only by owner
        os.chmod(key_path, 0o600)
    PUBLIC_KEY = PRIVATE_KEY.public_key()


def encrypt_file(data: bytes, password: str) -> bytes:
    """
    Encrypt file data using AES-256-GCM with scrypt key derivation.
    
    Process:
    1. Generate random 16-byte salt
    2. Derive 256-bit key from password using scrypt
    3. Generate random 12-byte nonce
    4. Encrypt data using AES-256-GCM
    
    Args:
        data: Raw file data to encrypt
        password: User-provided password for encryption
    
    Returns:
        Encrypted data in format: salt || nonce || ciphertext
    
    Security:
    - Scrypt parameters: n=16384, r=8, p=1 (resistant to GPU attacks)
    - Random salt and nonce prevent replay attacks
    - GCM mode provides authenticated encryption (AEAD)
    """
    salt = os.urandom(16)
    key = hashlib.scrypt(password.encode(), salt=salt, n=16384, r=8, p=1, dklen=32)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, data, None)
    return salt + nonce + ct


def decrypt_file(encrypted_data: bytes, password: str) -> bytes:
    """
    Decrypt file data using AES-256-GCM.
    
    Process:
    1. Extract salt (first 16 bytes)
    2. Extract nonce (bytes 16-28)
    3. Extract ciphertext (remaining bytes)
    4. Derive key from password using same scrypt parameters
    5. Decrypt using AES-256-GCM
    
    Args:
        encrypted_data: Encrypted data from encrypt_file()
        password: User-provided password for decryption
    
    Returns:
        Decrypted original file data
    
    Raises:
        cryptography.exceptions.InvalidTag: If password is wrong or data tampered
    
    Security:
    - GCM mode authenticates data (detects tampering)
    - Wrong password produces wrong key, causing authentication failure
    """
    salt = encrypted_data[:16]
    nonce = encrypted_data[16:28]
    ct = encrypted_data[28:]
    key = hashlib.scrypt(password.encode(), salt=salt, n=16384, r=8, p=1, dklen=32)
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ct, None)


def sign_document(data: bytes):
    """
    Sign document data using RSA-2048 with PSS padding.
    
    Process:
    1. Compute SHA-256 hash of document
    2. Sign hash using RSA private key with PSS padding
    3. Return signature and hash as hex strings
    
    Args:
        data: Document data to sign
    
    Returns:
        Tuple of (signature_hex, hash_hex)
    
    Security:
    - RSA-2048 key size provides ~112-bits of symmetric strength
    - PSS padding adds randomization, prevents signature forgery
    - SHA-256 is cryptographically secure
    - Random padding changes each signature even for same data
    """
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
    """
    Verify document signature and detect tampering.
    
    Process:
    1. Compute SHA-256 hash of current document
    2. Attempt to verify stored signature using RSA public key
    3. Return True if signature valid, False if invalid or tampered
    
    Args:
        data: Current document data to verify
        signature_hex: Stored signature from sign_document()
    
    Returns:
        bool: True if signature valid (document not tampered), False otherwise
    
    Security:
    - Any modification to document invalidates signature
    - Uses RSA public key for verification
    - Cannot forge signatures without private key
    - Returns False on any error (safe-fail approach)
    """
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
