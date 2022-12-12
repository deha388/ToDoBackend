from cryptography.fernet import Fernet

from config import load_config_yaml

cfg=load_config_yaml()

def get_encrypt_payload(user):
    secret_key = cfg["app"]["encrypt_key"].encode()
    fernet_obj = Fernet(secret_key)
    enc_message = fernet_obj.encrypt(user.username.encode())
    return enc_message.decode()


def get_decrypt_payload(payload_str):
    secret_key = cfg["app"]["encrypt_key"].encode()
    fernet_obj = Fernet(secret_key)
    denc_message = fernet_obj.decrypt(payload_str)
    return denc_message