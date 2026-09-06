# Face Blockchain Verify

A pipeline to detect a face in an image, search the web for its occurrences using a reverse image search, generate a canonical JSON fingerprint, and securely store its hash on the blockchain for later verification.

**IMPORTANT ETHICAL LIMITATION:**
This tool is built strictly for verifying content about a **CONSENTING** subject (e.g., your own face). 
You **MUST NOT** use this software to search for, track, or identify non-consenting individuals. 

## Pipeline Steps
1. **Face Encoding**: Uses `deepface` to detect and encode a facial vector.
2. **Reverse Image Search**: Uses the Bing Visual Search API to find online matches.
3. **Fingerprinting**: Combines the original image hash and web search results into a canonical JSON and calculates a SHA-256 fingerprint.
4. **Blockchain Upload**: Deploys to a configured Ethereum network (e.g., Sepolia testnet or local Ganache) using Web3.py.
5. **Verification**: Reads the hash back from the smart contract to confirm it matches.

## Prerequisites
- Python 3.8+
- An Ethereum wallet with testnet funds (e.g., Sepolia) or a local Ganache instance.
- An RPC URL (e.g., Infura, Alchemy, or Ganache local URL).
- A Bing Search API key (for Visual Search).

## Setup
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Environment Variables:**
   Copy `.env.example` to `.env` and fill in your keys.
   ```bash
   cp .env.example .env
   ```
3. **Deploy the Smart Contract:**
   Make sure you have funds in your wallet (get Sepolia ETH from a faucet if using Sepolia).
   ```bash
   python scripts/deploy_contract.py
   ```
   Take the deployed contract address and add it to your `.env` file (`CONTRACT_ADDRESS=...`).

4. **Add a Sample Image:**
   Place your own (consented) photo at `sample_data/sample_face.jpg`. The dummy file provided is a placeholder.

## Usage
Run the main orchestrator:
```bash
python main.py
```

## Why Web3/Blockchain?
By storing the SHA-256 fingerprint on an immutable ledger, you create a verifiable, time-stamped proof of the discovery. Using a testnet like Sepolia requires gas (which you can get for free from a faucet). Using a local network like Ganache allows for instant, free testing.
