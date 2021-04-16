from base64 import b64encode
from nacl import encoding, public
import requests
import os
import subprocess
import json


def encrypt(raw_public_key: str, secret_value: str) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(raw_public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")


if __name__ == '__main__':

    get_public_key = requests.get(f'https://api.github.com/repos/knoldus-test/ecr-demo/actions/secrets/public-key',
                                  headers={'Accept': 'application/vnd.github.v3+json',
                                           'Authorization': 'token ' + os.environ['SAKSHI_GH_API_ACCESS_TOKEN']})
    if get_public_key.ok is False:
        print('could not retrieve public key')
        print(get_public_key.text)
        exit(1)
    get_public_key_response = get_public_key.json()
    public_key_value = get_public_key_response['key']
    public_key_id = get_public_key_response['key_id']

    password = subprocess.run(['aws', 'ecr', 'get-login-password'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    encrypted_password = encrypt(public_key_value, password)
    update_password = requests.put('https://api.github.com/repos/knoldus-test/ecr-demo/actions/secrets/REGISTRY_PASSWORD',
                                   headers={'Accept': 'application/vnd.github.v3+json',
                                            'Authorization': 'token ' + os.environ['SAKSHI_GH_API_ACCESS_TOKEN']},
                                   data=json.dumps({'encrypted_value': encrypted_password, 'key_id': public_key_id}))
    if update_password.ok is False:
        print('could not update password')
        print(update_password.text)
        exit(1)
