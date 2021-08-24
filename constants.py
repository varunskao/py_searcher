# Infura API URLs
infura_api = {
    'rinkeby': r'https://rinkeby.infura.io/v3/{INSERT_API_KEY_HERE}',
    'mainnet': r'https://mainnet.infura.io/v3/{INSERT_API_KEY_HERE}',
    'polygon_mainnet': r'https://polygon-mainnet.infura.io/v3/{INSERT_API_KEY_HERE}'
}

# Factory contract addresses
factory_contract_addresses = {
    'uniswap': '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f',
    'sushi_swap': '0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac',
}

# Token Addresses
token_addresses = {
    'eth_dai': '0x6B175474E89094C44Da98b954EedeAC495271d0F', # contract address for dai
    'eth_weth': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
    'eth_usdc': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 
    'eth_fei': '0x956F47F50A910163D8BF957Cf5846D573E7f87CA',
    'eth_usdt': '0xdAC17F958D2ee523a2206206994597C13D831ec7',
    'eth_hex': '0x2b591e99afE9f32eAA6214f7B7629768c40Eeb39',
    'eth_wbtc': '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599',
    'eth_wise': '0x66a0f676479Cee1d7373f3DC2e2952778BfF5bd6',
    'eth_uni': '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984',
    'eth_ufo': '0x249e38Ea4102D0cf8264d3701f1a0E39C4f2DC3B'
}

# Pair contract addresses
pair_contract_addresses = {
    'dai_weth': dict(),
    'usdt_weth': dict(),
    'fei_weth': dict(),
    'wise_weth': dict(),
    'usdc_weth': dict(),
    'ufo_weth': dict()
}

# Token decimal values
decimals = {
    'dai': 10 ** 18,
    'weth': 10 ** 18,
    'usdc': 10 ** 6,
    'fei': 10 ** 18,
    'usdt': 10 ** 6,
    'hex': 10 ** 8,
    'wbtc': 10 ** 8,
    'wise': 10 ** 18,
    'uni': 10 ** 18,
    'ufo': 10 ** 18
}

# MetaMask mneumonic
eth_mmm = 'INSERT_MNEUMONIC_HERE'
dot_mmm = 'INSERT_MNEUMONIC_HERE'

# Etherscan API Key
ETHERSCAN_API_KEY = '{INSERT_ETHERSCAN_API_KEY_HERE}'
POLYSCAN_API_KEY = '{INSERT_POLYSCAN_API_KEY_HERE}'

# Precursors used for referencing token addresses based on protocol
eth_precursor = 'eth'

# Null address for reference
null_address = '0x0000000000000000000000000000000000000000'

# Exchange transaction fees
uniswap_v2_fee = 0.003
sushi_swap_fee = 0.0025