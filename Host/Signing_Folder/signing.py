from ecdsa import SigningKey, VerifyingKey, BadSignatureError, NIST256p
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from ecdsa.util import sigdecode_string
import hashlib
from binary_to_hex_text import convert_binary_to_hex

class Ed25519Signer:
    def __init__(self, key_path: str, public_key_path: str):
        self.private_key = self._load_private_key(key_path)
        self.public_key = self._load_public_key(public_key_path)

    def _load_private_key(self, path: str) -> SigningKey:
        with open(path, "r") as f:
            sk = f.read()
            sk_bytes = bytes.fromhex(sk)
        return SigningKey.from_string(sk_bytes, curve = NIST256p)

    def _load_public_key(self, path: str) -> VerifyingKey:
        with open(path, "r") as f:
            hex_key = f.read().strip()
        key_bytes = bytes.fromhex(hex_key)
        write_hex_file(key_bytes, "public_key.bin")
        return VerifyingKey.from_string(key_bytes, curve=NIST256p)

    def sign(self, message: bytes) -> bytes:
        return self.private_key.sign(message, hashfunc=hashlib.sha256)

    def convert_to_bytes(self, signature: bytes):
        r, s = sigdecode_string(signature, self.private_key.curve.order)
        r_bytes = r.to_bytes((r.bit_length() + 7) // 8, byteorder='big')
        s_bytes = s.to_bytes((s.bit_length() + 7) // 8, byteorder='big')
        final_sig = r_bytes + s_bytes
        return final_sig

    def verify(self, message: bytes, signature: bytes) -> bool:
        try:
            return self.public_key.verify(signature, message, hashfunc=hashlib.sha256)
        except BadSignatureError:
            return False

def read_hex_file(file_path: str) -> bytes:
    with open(file_path, "rb") as f:
        return f.read()

def write_hex_file(data: bytes, file_path: str):
    with open(file_path, "wb") as f:
        f.write(data)

def convert_to_text(file_path: str, file_path_out: str):
    with open(file_path, 'rb') as bin_file:
        binary_data = bin_file.read()
    hex_data = binary_data.hex()
    with open(file_path_out, 'w') as f:
        f.write(hex_data)

def main():
    message = read_hex_file("../Application.bin")
    signer = Ed25519Signer("ecdsa_private.txt", "ecdsa_public.txt")
    signature = signer.sign(message)
    write_hex_file(signature, "../Application.sig")
    Verify = signer.verify(message, signature)
    print(Verify)

if __name__ == "__main__":
    main()