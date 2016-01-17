import requests
import json

from bitcoinlib.core.key import CPubKey
from wallet import PlainWallet
from bitcoinlib.wallet import P2PKHBitcoinAddress
from message import SecureMessage
import hashfile
import configuration

config = configuration.NotaryConfiguration('../notaryconfig.ini')
if config.is_remote_testing():
    notary_url = config.get_remote_server_url()
else:
    notary_url = config.get_local_server_url()

requests.packages.urllib3.disable_warnings()

wallet = PlainWallet()
secure_message = SecureMessage(wallet)

## Test GET pubkey
pubkey_response = requests.get(notary_url+'/api/v1/pubkey', verify=False)
data = pubkey_response.json()
other_party_public_key_hex = data['public_key']
print data['public_key']
other_party_public_key_decoded = other_party_public_key_hex.decode("hex")
other_party_public_key = CPubKey(other_party_public_key_decoded)
other_party_address = P2PKHBitcoinAddress.from_pubkey(other_party_public_key)
address = str(wallet.get_bitcoin_address())

## Test GET challenge

response = requests.get(notary_url+'/api/v1/challenge/' + address, verify=False)
payload = json.loads(response.content)
if secure_message.verify_secure_payload(other_party_address, payload):
    message = secure_message.get_message_from_secure_payload(payload)
    print(message)

payload = secure_message.create_secure_payload(other_party_public_key_hex, message)
response = requests.put(notary_url+'/api/v1/challenge/' + address, data=payload, verify=False)
cookies = requests.utils.dict_from_cookiejar(response.cookies)

metadata = {
    'title': 'Stillwater Shame',
    'creator': 'Ploughman, J.J.',
    'subject': 'Rock Music',
    'description': 'A song about lying politicians',
    'publisher': 'J.J. Ploughman',
    'contributor': 'J.J. Ploughman',
    'date': '2001-08-03T03:00:00.000000',
    'type': 'Music',
    'format': 'm4a',
    'source': 'Green Beans Album',
    'language': 'en',
    'relation': 'Unknown',
    'coverage': 'Unknown',
    'rights': 'Unknown'
}


document_hash = hashfile.hash_file('/Users/tssbi08/govern8r/IP/README.txt')
metadata['document_hash'] = document_hash

response = requests.get(notary_url+'/api/v1/account/' + address + '/notarization/' + document_hash + '/status', cookies=cookies, verify=False)
if response.status_code == 404:
    cookies = requests.utils.dict_from_cookiejar(response.cookies)
    notarization_payload = secure_message.create_secure_payload(other_party_public_key_hex, json.dumps(metadata))
    response = requests.put(notary_url+'/api/v1/account/' + address + '/notarization/' + document_hash,
                    cookies=cookies, data=notarization_payload, verify=False)
    if response.content is not None:
        payload = json.loads(response.content)
        if secure_message.verify_secure_payload(other_party_address, payload):
            message = secure_message.get_message_from_secure_payload(payload)
            print(message)

