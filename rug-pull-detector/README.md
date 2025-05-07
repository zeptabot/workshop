# 🧪 Uniswap V2 Liquidity Pool Analyzer

This tool is designed to analyze the token pairs characteristics using **Uniswap V2** smart contracts
on **Base chain**.

It inspects various characteristics of the tokens involved in each pair and prints key risk and health
indicators. The results are saved into a text report (`report.txt`) titled "TOKEN ANALYSIS REPORT".

## 🔍 What the Script Does

1. Connects to the Base chain via an RPC endpoint.
2. Interacts with the Uniswap V2 Factory contract.
3. Based on the input token address, it finds the corresponding pair backed up by WETH or USDC.
4. For each pair, it fetches:

   - Pair address
   - Token details (name, symbol, addresses)
   - Total Supply of LP Tokens
   - Market cap (calculated based on liquidity pool reserves)
   - Minting capabilities
   - Total Supply Status

5. Prints results to console and saves them to a text file.

## 📊 Parameters Analyzed Per Token or Pair

| Parameter                   | Description                                                |
| --------------------------- | :--------------------------------------------------------: |
| `Token Name / Symbol`       | Identity of the token in the pair                         |
| `Total Supply of LP Tokens` | How many LP tokens exist for the pair                     |
| `Market Cap`                | Estimated based on liquidity pool reserves                |
| `Minting Ability`           | Can new tokens be minted? `MINTABLE` or `NOT MINTABLE`    |
| `Total Supply Status`       | If minting is disabled, it's `FIXED`; otherwise `NOT FIXED` |

## 📁 Input

- Input token address
- Uniswap V2 Factory contract address **(no need to update this if using uniswap v2 on Base)**
- Base chain RPC endpoint **(no need to update for running on base)**

**Note:**
- You can use [The graph](https://thegraph.com/explorer/subgraphs/D31gzGUtVNhHNdnxeELUBdch5rzDRm5cddvae9GzhCLu?view=Query) to fetch new token addresses
```
{
  tokens(first: 5, orderBy: tradeVolumeUSD, orderDirection: desc) {
    id
    symbol
    name
    decimals
  }
}
``` 


## 📁 Output

- Console output with all parameters per pair
- A text report saved as `report.txt` in the `data/outputs` directory
- Title: `"TOKEN ANALYSIS REPORT"`

#  Python
##  Requirements

- Python 3.8+
- web3.py

### Install dependencies:

```bash
pip install web3
```

### Use existing docker image `oceanprotocol/c2d_examples:py-general`:

For running the algorithm seamlessly, use our already-built docker image within the VS Code extension:

- Docker image: `oceanprotocol/c2d_examples`
- Docker tag: `py-general`

#  JavaScript

##  Requirements

- Node.js
- web3.js

### Install dependencies:

```bash
npm install web3
```

### Use existing docker image `oceanprotocol/c2d_examples:js-general`:

For running the algorithm seamlessly, use our already-built docker image within the VS Code extension:

- Docker image: `oceanprotocol/c2d_examples`
- Docker tag: `js-general`

## 🔐 Disclaimer

This tool is for research and educational purposes. It is not a financial advice tool.
