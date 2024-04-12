from cryptography.fernet import Fernet
import base64
import hashlib
import os
import sys


def find_files(filename: str, is_build: bool) -> list[str]:
    matches = []

    path = ""
    if is_build:
        path = "./build"
    else:
        path = "./"

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(filename):
                matches.append(os.path.join(root, file))

    return matches


def encrypt_file(filename: str, key: str) -> None:
    fernet = Fernet(key)
    with open(filename, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(filename, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def decrypt_file(filename: str, key: str) -> None:
    fernet = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(filename, 'wb') as file:
        file.write(decrypted_data)


def run_all_files(mode: str, password: str, is_build: bool = True) -> None:
    key = hashlib.md5(password.encode("utf-8")).hexdigest()
    key_64 = base64.urlsafe_b64encode(key.encode("utf-8"))

    coach_files = find_files('_assessment.py', is_build)
    for file in coach_files:
        if mode == "encrypt":
            encrypt_file(file, key_64)
        else:
            decrypt_file(file, key_64)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError(
            'A config and password must be provided as an argument')

    mode = sys.argv[1]
    password = sys.argv[2]

    run_all_files(mode, password, is_build=False)
