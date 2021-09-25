from constants import *
from web3 import Web3
import requests
import time

# Initialize instance of web3 provder using an infura mainnet node.
web3 = Web3(Web3.HTTPProvider(infura_api['mainnet']))

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

# Can only be used with a Etherscan PRO account. Removes the need to hardcode token decimal values.
# def get_divisor(contract_address):
#     base_etherscan_url = "https://api.etherscan.io/api?module=token&action=tokeninfo&contractaddress={0}&apikey={1}"
#     etherscan_url = base_etherscan_url.format(contract_address, ETHERSCAN_API_KEY)
#     etherscan_response = requests.get(etherscan_url)
#     if etherscan_response.status_code == 200:
#         contract_divisor = etherscan_response.json()['result']['divisor']
#         return contract_divisor
#     else:
#         raise Exception('get_divisor() API call failed. return code is {}.'.format(etherscan_response.status_code))

# Method to obtain the instance of a contract on ethereum
def get_contract(factory_contract_address):
    factory_contract_abi = get_abi(factory_contract_address)
    factory_contract = web3.eth.contract(
        abi=factory_contract_abi,
        address=factory_contract_address
    )
    return factory_contract

# Initialize empty dictionary to store factory contract instances. 
# This variable represents the DEXs that are used to arbitrage against each other
factory_contracts = dict() 
for key, value in factory_contract_addresses.items():
    factory_contracts[key] = get_contract(value)

# Retrieve the pair contract addresses for each contract factory for the crypto currency pairs being arbitraged.
for key in pair_contract_addresses.keys():
    for exchange in factory_contract_addresses.keys():
        token0_address = token_addresses['{}_{}'.format(eth_precursor, key.split('_')[0])]
        token1_address = token_addresses['{}_{}'.format(eth_precursor, key.split('_')[1])]
        pair_contract_address = factory_contracts[exchange].functions.getPair(token0_address, token1_address).call()
        if pair_contract_address != null_address:
            pair_contract_addresses[key][exchange] = pair_contract_address
        else:
            pair_contract_addresses[key][exchange] = None

# Initialize dictionary containing the pairs defined in pair_contract_addresses
pair_contracts = {key: dict() for key in pair_contract_addresses.keys()}

# Initialize pair contract instances
for key, val in pair_contract_addresses.items():
    for exchange in val.keys():
        pair_contract_address = pair_contract_addresses[key][exchange]
        if pair_contract_address != None: 
            pair_contracts[key][exchange] = get_contract(pair_contract_address)
        else:
            pair_contracts[key][exchange] = None
            
# QUESTION: kLast = dai_weth_contract.functions.kLast().call() # Always outputs 0. Why?

# Get price of token1 in the currency of token0
# Ex: Get the price of eth in usdc
# Still need to check for token ordering by pair.
def get_token_price(pair_contract, token0_decimals, token1_decimals):
    reserve_array = pair_contract.functions.getReserves().call()
    token0 = reserve_array[0] / token0_decimals
    token1 = reserve_array[1] / token1_decimals
    return token0 / token1

# get_token_price(pair_contracts['usdc_weth']['uniswap'], decimals['usdc'], decimals['weth']) # Example 1
# get_token_price(pair_contracts['usdc_weth']['sushi_swap'], decimals['usdc'], decimals['weth']) # Example 2

# Get the amount of token1 given a set amount of token0 - i.e. Amount of ETH returned given a set number of USDC tokens.
# Decimal transfomration takes place inside method 
# Example: uni_eth_returns = returned_token_1(pair_contracts['usdc_weth']['uniswap'], 1000, uniswap_v2_fee, decimals['usdc'], decimals['weth'])
def returned_token_1(pair_contract, token0_amount, exchange_fee, token0_decimals, token1_decimals):
    token0_amount_with_decimals = token0_amount * token0_decimals
    reserve_array = pair_contract.functions.getReserves().call()
    token0_balance = reserve_array[0] # x
    token1_balance = reserve_array[1] # y
    ydx = (token0_amount_with_decimals * token1_balance) * (1 - exchange_fee)
    x_plus_dx = token0_balance + (token0_amount_with_decimals * (1 - exchange_fee))
    withdraw_token_amount = ydx / x_plus_dx
    return withdraw_token_amount / token1_decimals

# Get the amount of token0 given a set amount of token1 - i.e. Amount of USDC returned given a set number of ETH tokens.
# Decimal transfomration takes place inside method
def returned_token_0(pair_contract, token1_amount, exchange_fee, token0_decimals, token1_decimals):
    token1_amount_with_decimals = token1_amount * token1_decimals
    reserve_array = pair_contract.functions.getReserves().call()
    token0_balance = reserve_array[0] # x
    token1_balance = reserve_array[1] # y
    ydx = (token1_amount_with_decimals * token0_balance) * (1 - exchange_fee)
    x_plus_dx = token1_balance + (token1_amount_with_decimals * (1 - exchange_fee))
    withdraw_token_amount = ydx / x_plus_dx
    return withdraw_token_amount / token0_decimals

# Examples
uni_usdc_returns = returned_token_0(pair_contracts['usdc_weth']['uniswap'], 1, uniswap_v2_fee, decimals['usdc'], decimals['weth'])
sushi_eth_returns = returned_token_1(pair_contracts['usdc_weth']['sushi_swap'], uni_usdc_returns, sushi_swap_fee, decimals['usdc'], decimals['weth'])

# Check for profits - WARNING: DOES NOT INCLUDE GAS FEES
for i in range(2880):
    for pair in pair_contracts.keys():
        try:
            uni_token0 = returned_token_0(pair_contracts[pair]['uniswap'], 1, uniswap_v2_fee, decimals['usdc'], decimals['weth'])
            sushi_token1_returns = returned_token_1(pair_contracts[pair]['sushi_swap'], uni_token0, sushi_swap_fee, decimals['usdc'], decimals['weth'])
            buy_uni_sell_sushi_profit_token1 = sushi_token1_returns - 1
            #
            sushi_token0 = returned_token_0(pair_contracts[pair]['sushi_swap'], 1, sushi_swap_fee, decimals['usdc'], decimals['weth'])
            uni_token1_returns = returned_token_1(pair_contracts[pair]['uniswap'], sushi_token0, uniswap_v2_fee, decimals['usdc'], decimals['weth'])
            buy_sushi_sell_uni_profit_token1 = uni_token1_returns - 1
            #
            if buy_uni_sell_sushi_profit_token1 > 0:
                print(f"Buy USDC/ETH on Uniswap and sell USDC/ETH on Sushiswap. Profit: USD {buy_uni_sell_sushi_profit_token1}")
            elif buy_sushi_sell_uni_profit_token1 > 0:
                print(f"Buy USDC/ETH on Sushiswap and sell USDC/ETH on Uniswap. Profit: USD {buy_sushi_sell_uni_profit_token1}")
            else: pass
            #
            uni_token1 = returned_token_1(pair_contracts[pair]['uniswap'], 5000, uniswap_v2_fee, decimals['usdc'], decimals['weth'])
            sushi_token0_returns = returned_token_0(pair_contracts[pair]['sushi_swap'], uni_token1, sushi_swap_fee, decimals['usdc'], decimals['weth'])
            buy_uni_sell_sushi_profit_token0 = sushi_token0_returns - 5000
            #
            sushi_token1 = returned_token_1(pair_contracts[pair]['sushi_swap'], 5000, sushi_swap_fee, decimals['usdc'], decimals['weth'])
            uni_token0_returns = returned_token_0(pair_contracts[pair]['uniswap'], sushi_token1, uniswap_v2_fee, decimals['usdc'], decimals['weth'])
            buy_sushi_sell_uni_profit_token0 = uni_token0_returns - 5000
            #
            if buy_uni_sell_sushi_profit_token0 > 0:
                print(f"Buy USDC/ETH on Uniswap and sell USDC/ETH on Sushiswap. Profit: USD {buy_uni_sell_sushi_profit_token0}")
            elif buy_sushi_sell_uni_profit_token0 > 0:
                print(f"Buy USDC/ETH on Sushiswap and sell USDC/ETH on Uniswap. Profit: USD {buy_sushi_sell_uni_profit_token0}")
            else: pass
        except AttributeError: pass
    time.sleep(1)