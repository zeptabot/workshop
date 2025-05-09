const { Web3 } = require("web3");
const fs = require("fs");
const path = require("path");

// Contract ABIs
const uniswapV2FactoryAbi = [
  {
    constant: true,
    inputs: [
      { name: "tokenA", type: "address" },
      { name: "tokenB", type: "address" },
    ],
    name: "getPair",
    outputs: [{ name: "", type: "address" }],
    payable: false,
    stateMutability: "view",
    type: "function",
  },
  {
    constant: true,
    inputs: [],
    name: "allPairsLength",
    outputs: [{ name: "", type: "uint256" }],
    payable: false,
    stateMutability: "view",
    type: "function",
  },
  {
    constant: true,
    inputs: [{ name: "uint", type: "uint256" }],
    name: "allPairs",
    outputs: [{ name: "pair", type: "address" }],
    payable: false,
    stateMutability: "view",
    type: "function",
  },
];

const pairAbi = [
  {
    constant: true,
    inputs: [],
    name: "token0",
    outputs: [{ name: "", type: "address" }],
    stateMutability: "view",
    type: "function",
  },
  {
    constant: true,
    inputs: [],
    name: "token1",
    outputs: [{ name: "", type: "address" }],
    stateMutability: "view",
    type: "function",
  },
  {
    constant: true,
    inputs: [],
    name: "totalSupply",
    outputs: [{ name: "", type: "uint256" }],
    stateMutability: "view",
    type: "function",
  },
  {
    constant: true,
    inputs: [],
    name: "getReserves",
    outputs: [
      { name: "reserve0", type: "uint112" },
      { name: "reserve1", type: "uint112" },
      { name: "blockTimestampLast", type: "uint32" },
    ],
    stateMutability: "view",
    type: "function",
  },
];

const tokenAbi = [
  {
    constant: true,
    inputs: [],
    name: "name",
    outputs: [{ name: "", type: "string" }],
    stateMutability: "view",
    type: "function",
  },
  {
    constant: true,
    inputs: [],
    name: "symbol",
    outputs: [{ name: "", type: "string" }],
    stateMutability: "view",
    type: "function",
  },
  {
    constant: true,
    inputs: [],
    name: "totalSupply",
    outputs: [{ name: "", type: "uint256" }],
    stateMutability: "view",
    type: "function",
  },
];

// Constants
const BASE_RPC_URL = "https://base.drpc.org";
const USDC_CONTRACT = "0xd9AA594F65d163C22072c0eDFC7923A7F3470cC1";
const WETH_CONTRACT = "0x4200000000000000000000000000000000000006";
const UNISWAP_V2_FACTORY_ADDRESS = "0x8909Dc15e40173Ff4699343b6eB8132c65e18eC6";

// Initialize Web3
const web3 = new Web3(BASE_RPC_URL);

// Create factory contract instance
const factoryContract = new web3.eth.Contract(
  uniswapV2FactoryAbi,
  UNISWAP_V2_FACTORY_ADDRESS
);

async function calculateMarketCap(
  tokenContract,
  tokenSymbol,
  reserve0,
  reserve1
) {
  try {
    const totalSupply = await tokenContract.methods.totalSupply().call();
    const pricePerToken = reserve0 > 0 ? reserve1 / reserve0 : 0;
    const marketCap = totalSupply * pricePerToken;
    console.log(
      `${tokenSymbol} Market Cap: $${marketCap.toLocaleString(undefined, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      })}`
    );
  } catch (error) {
    console.log(`Error calculating market cap: ${error.message}`);
  }
}

async function checkMintingAbility(tokenContract, tokenName) {
  try {
    await tokenContract.methods.mint().call();
    console.log("Mint status: MINTABLE");
    console.log("Total Supply Status: NOT FIXED");
  } catch {
    console.log("Mint status: NOT MINTABLE");
    console.log("Total Supply Status: FIXED");
  }
}

async function findPairByToken(tokenAddress) {
  try {
    let pairAddress = await factoryContract.methods
      .getPair(
        web3.utils.toChecksumAddress(tokenAddress),
        web3.utils.toChecksumAddress(USDC_CONTRACT)
      )
      .call();

    if (pairAddress === "0x0000000000000000000000000000000000000000") {
      pairAddress = await factoryContract.methods
        .getPair(
          web3.utils.toChecksumAddress(tokenAddress),
          web3.utils.toChecksumAddress(WETH_CONTRACT)
        )
        .call();
    }

    if (pairAddress === "0x0000000000000000000000000000000000000000") {
      console.log(
        `Pair could not be found for ${tokenAddress} backed by WETH or USDC.`
      );
      return null;
    }
    return pairAddress;
  } catch (error) {
    console.error("Error finding pair:", error);
    return null;
  }
}

async function generateReport(inputTokenAddress) {
  const output = [];

  // Header
  output.push("=".repeat(80));
  output.push("🔍 TOKEN ANALYSIS REPORT");
  output.push("=".repeat(80));
  output.push(`Generated on: ${new Date().toLocaleString()}`);
  output.push("-".repeat(80));

  // Token Information
  output.push("\n📊 TOKEN INFORMATION");
  output.push("-".repeat(40));
  output.push(`Token Address: ${inputTokenAddress}`);

  const pairAddress = await findPairByToken(inputTokenAddress);
  if (!pairAddress) {
    output.push("Pair could not be found! Quit execution of the algorithm...");
    return;
  }

  const pairContract = new web3.eth.Contract(pairAbi, pairAddress);
  const totalLpTokens = await pairContract.methods.totalSupply().call();
  output.push(`Total Supply of LP Tokens: ${totalLpTokens}`);

  const token0 = await pairContract.methods.token0().call();
  const token1 = await pairContract.methods.token1().call();
  const inputToken =
    token0 !== USDC_CONTRACT && token0 !== WETH_CONTRACT ? token0 : token1;
  const tokenContract = new web3.eth.Contract(tokenAbi, inputToken);

  const tokenName = await tokenContract.methods.name().call();
  const tokenSymbol = await tokenContract.methods.symbol().call();
  output.push(`Token Name: ${tokenName}`);
  output.push(`Token Symbol: ${tokenSymbol}`);

  // Liquidity Information
  output.push("\n💧 LIQUIDITY INFORMATION");
  output.push("-".repeat(40));
  output.push(`Liquidity Pair Address: ${pairAddress}`);
  output.push(`Total Supply of LP Tokens: ${totalLpTokens}`);

  // Market Analysis
  output.push("\n💰 MARKET ANALYSIS");
  output.push("-".repeat(40));
  const reserves = await pairContract.methods.getReserves().call();
  await calculateMarketCap(
    tokenContract,
    tokenSymbol,
    reserves[0],
    reserves[1]
  );

  // Supply Analysis
  output.push("\n🪄 SUPPLY ANALYSIS");
  output.push("-".repeat(40));
  await checkMintingAbility(tokenContract, tokenName);

  output.push("\n" + "=".repeat(80));
  output.push("End of Report");
  output.push("=".repeat(80));

  // Save to file
  const outputText = output.join("\n");
  const outputPath = path.join("/data/outputs");
  if (!fs.existsSync(outputPath)) {
    fs.mkdirSync(outputPath, { recursive: true });
  }

  const txtFilename = path.join(outputPath, "report.txt");
  fs.writeFileSync(txtFilename, outputText);

  console.log(`✅ Output saved to ${txtFilename}\n`);
  console.log(outputText);
}

// Example usage. You can change the input token address to analyze different tokens.
const inputTokenAddress = "0x768be13e1680b5ebe0024c42c896e3db59ec0149";
generateReport(inputTokenAddress).catch(console.error);
