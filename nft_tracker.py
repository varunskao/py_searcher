## NFT Tracker

# Default modules
from constants import *
from web3 import Web3
import requests
import time

# Email modules
import smtplib
import ssl


# Initialize instance of web3 provder using an infura mainnet node.
web3 = Web3(Web3.HTTPProvider(infura_api['mainnet']))
adventurer_0x_contract_address = '0x329Fd5E0d9aAd262b13CA07C87d001bec716ED39'

# Email constants
port = 465
password = 'ENTER PASSWORD HERE'
context = ssl.create_default_context()

# Email context information
sender_email = "ENTER EMAIL HERE"
receiver_email = "ENTER EMAIL HERE"
message = """
Subject: MINT NFTs - PublicMax Increased

Start minting the Adventure Cards. 
Link here: https://etherscan.io/address/0x329Fd5E0d9aAd262b13CA07C87d001bec716ED39#readContract
Contract Address: '0x329Fd5E0d9aAd262b13CA07C87d001bec716ED39'
Connect your MetaMask wallet and start minting.
"""

# Method to access the abi for any contract on ethereum.
def get_abi(contract_address):
    base_etherscan_url = "https://api.etherscan.io/api?module=contract&action=getabi&address={0}&apikey={1}"
    etherscan_url = base_etherscan_url.format(contract_address, ETHERSCAN_API_KEY)
    etherscan_response = requests.get(etherscan_url)
    if etherscan_response.status_code == 200:
        contract_abi = etherscan_response.json()['result']
        return contract_abi
    else:
        raise Exception('get_abi() API call failed. return code is {}.'.format(etherscan_response.status_code))

# Retreive ABI
adventurer_0x_contract_abi = get_abi(adventurer_0x_contract_address)

adventurer_0x_contract = web3.eth.contract(
    abi=adventurer_0x_contract_abi,
    address=adventurer_0x_contract_address
)

current_max = 4000

count = 0
for i in range(24 * 60 * 12):
    new_max = adventurer_0x_contract.functions.publicMax().call()
    if new_max > current_max:
        count += 1
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login("ENTER EMAIL HERE", password)
            server.sendmail(sender_email, receiver_email, message)
            if count == 5:
                break
    else: 
        time.sleep(5)

