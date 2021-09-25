from constants import ETHERSCAN_API_KEY
from web3 import Web3
import requests
import json

def get_abi(contract_address):
    base_etherscan_url = "https://api.etherscan.io/api?module=contract&action=getabi&address={0}&apikey={1}"
    etherscan_url = base_etherscan_url.format(contract_address, ETHERSCAN_API_KEY)
    etherscan_response = requests.get(etherscan_url)
    if etherscan_response.status_code == 200:
        contract_abi = etherscan_response.json()['result']
        return contract_abi
    else:
        raise Exception('get_abi() API call failed. return code is {}.'.format(etherscan_response.status_code))


def get_contract_methods(contract_address):
    contract_abi = get_abi(contract_address)
    contract_abi_dict = json.loads(contract_abi)
    contract_methods = dict()
    for i in range(len(contract_abi_dict)):
        contract_function = contract_abi_dict[i]
        for key in contract_function.keys():
            if key == 'name':
                contract_methods[i] = contract_function['name']
    return contract_methods, contract_abi_dict