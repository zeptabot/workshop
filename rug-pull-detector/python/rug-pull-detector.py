from web3 import Web3
import datetime
import io
import sys

uniswap_v2_factory_abi = [  # Minimal ABI for Factory contract
    {
        "constant": True,
        "inputs": [{"name": "tokenA", "type": "address"}, {"name": "tokenB", "type": "address"}],
        "name": "getPair",
        "outputs": [{"name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "allPairsLength",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "uint", "type": "uint256"}],
        "name": "allPairs",
        "outputs": [{"name": "pair", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]

pair_abi = [
    {"constant": True, "inputs": [], "name": "token0", "outputs": [{"name": "", "type": "address"}],
     "stateMutability": "view", "type": "function"},
    {"constant": True, "inputs": [], "name": "token1", "outputs": [{"name": "", "type": "address"}],
     "stateMutability": "view", "type": "function"},
    {"constant": True, "inputs": [], "name": "totalSupply", "outputs": [{"name": "", "type": "uint256"}],
     "stateMutability": "view", "type": "function"},
    {"constant": True, "inputs": [], "name": "getReserves",
     "outputs": [{"name": "reserve0", "type": "uint112"}, {"name": "reserve1", "type": "uint112"},
                 {"name": "blockTimestampLast", "type": "uint32"}], "stateMutability": "view", "type": "function"}
]

token_abi = [
    {"constant": True, "inputs": [], "name": "name", "outputs": [{"name": "", "type": "string"}],
     "stateMutability": "view", "type": "function"},
    {"constant": True, "inputs": [], "name": "symbol", "outputs": [{"name": "", "type": "string"}],
     "stateMutability": "view", "type": "function"},
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]

BASE_RPC_URL = "https://base.drpc.org"  # Base RPC URL
web3 = Web3(Web3.HTTPProvider(BASE_RPC_URL))

# Ensure the connection to the Base chain
if web3.is_connected():
    print("Connected to Base Chain")

# Input token address 
input_token_address = "0x768be13e1680b5ebe0024c42c896e3db59ec0149"

# Uniswap V2 Factory contract address 
uniswap_v2_factory_address = "0x8909Dc15e40173Ff4699343b6eB8132c65e18eC6"

# Do not change these. Will be used to find the pair with USDC or WETH
USDC_contract = '0xd9AA594F65d163C22072c0eDFC7923A7F3470cC1'
WETH_contract = '0x4200000000000000000000000000000000000006'

# Create contract instance for the Uniswap V2 Factory
factory_contract = web3.eth.contract(address=web3.to_checksum_address(uniswap_v2_factory_address),
                                     abi=uniswap_v2_factory_abi)

def calculate_market_cap(token_contract, token_symbol, reserve0, reserve1):
    """
    Calculate the market cap of a token based on its liquidity reserves.
    This is an example function to show how to interact with token contracts.
    """
    try:
        # Fetch total supply
        total_supply = token_contract.functions.totalSupply().call()

        # Determine price based on liquidity reserves
        price_per_token = reserve1 / reserve0 if reserve0 > 0 else 0

        # Calculate market cap
        market_cap = total_supply * price_per_token

        print(f"{token_symbol} Market Cap: ${market_cap:,.2f}")
    except Exception as e:
        print(f"Error calculating market cap: {e}")

def check_minting_ability(token_contract, token_name):
    """
    Check if a token contract has minting capabilities.
    This is an example function to show how to check contract functionality.
    """
    try:
        token_contract.functions.mint().call()
        print(f"Mint status: MINTABLE")
        print(f"Total Supply Status: NOT FIXED")
    except:
        print(f"Mint status: NOT MINTABLE")
        print(f"Total Supply Status: FIXED")

def new_check_one():
    """
    TODO: Implement another check
    pass
    """

def new_check_two():
    """
    TODO: Implement another check
    pass
    """


def find_pair_by_token(token_address):
    pair_address = factory_contract.functions.getPair(web3.to_checksum_address(token_address),
                                                      web3.to_checksum_address(USDC_contract)).call()
    if pair_address == '0x0000000000000000000000000000000000000000':
        pair_address = factory_contract.functions.getPair(web3.to_checksum_address(token_address),
                                                          web3.to_checksum_address(WETH_contract)).call()
    if pair_address == '0x0000000000000000000000000000000000000000':
        print(f"Pair could not be found for {token_address} backed by WETH or USDC.")
        return
    return pair_address



pair_address = find_pair_by_token(token_address=input_token_address)
if pair_address is None:
    print("Pair could not be found! Quit execution of the algorithm...")
    quit()

buffer = io.StringIO()
sys.stdout = buffer

# Add header and timestamp
print("=" * 80)
print("🔍 TOKEN ANALYSIS REPORT")
print("=" * 80)
print(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("-" * 80)
print("\n📊 TOKEN INFORMATION")
print("-" * 40)
print(f"Token Address: {input_token_address}")

pair_contract = web3.eth.contract(address=web3.to_checksum_address(pair_address), abi=pair_abi)

# Get total supply of LP tokens
total_lp_tokens = pair_contract.functions.totalSupply().call()
print(f"Total Supply of LP Tokens: {total_lp_tokens}")

# Get token addresses
token_0 = pair_contract.functions.token0().call()
token_1 = pair_contract.functions.token1().call()
if token_0 != USDC_contract and token_0 != WETH_contract:
    input_token = token_0
else:
    input_token = token_1
token_contract = web3.eth.contract(address=input_token, abi=token_abi)

# Get token names and symbols
token_name = token_contract.functions.name().call()
token_symbol = token_contract.functions.symbol().call()
print(f"Token Name: {token_name}")
print(f"Token Symbol: {token_symbol}")

print("\n💧 LIQUIDITY INFORMATION")
print("-" * 40)
print(f"Liquidity Pair Address: {pair_address}")
print(f"Total Supply of LP Tokens: {total_lp_tokens}")

print("\n💰 MARKET ANALYSIS")
print("-" * 40)

# Calculate market cap
reserves = pair_contract.functions.getReserves().call()
calculate_market_cap(token_contract=token_contract, token_symbol=token_symbol,
                                    reserve0=reserves[0],
                                    reserve1=reserves[1])

print("\n🪄 SUPPLY ANALYSIS")
print("-" * 40)
# Check if each token from the pair is mintable
check_minting_ability(token_contract, token_name)

print("\n" + "=" * 80)
print("End of Report")
print("=" * 80)

sys.stdout = sys.__stdout__

output_text = buffer.getvalue()

# Save to text file
txt_filename = '/data/outputs/report.txt'
with open(txt_filename, 'w') as f:
    f.write(output_text)

print(f"✅ Output saved to {txt_filename} \n")
print(output_text)
