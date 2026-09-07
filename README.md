# HH Goa 2026 — Face & Blockchain Verifier

## 1. Project Overview
A pipeline that takes an input face image, performs a genuine dynamic reverse image search to find candidate posts, encodes and matches faces to find the most accurate candidate, generates a cryptographic SHA-256 fingerprint of the matched content, stores it on a blockchain, and provides independent re-verification and tamper detection.

**Pipeline Flow:**
Face Scan/Input Image → Face Detection → Face Encoding → Genuine Web/Social Media Search → Dynamic Candidate Posts → Face Similarity Matching → Matching Post → Content Fingerprint (SHA-256) → Blockchain Record → On-chain Retrieval → Independent Re-verification → VERIFIED / TAMPERED

## 2. Architecture
```text
[Input Image]
      ↓
[FaceNet Model] → Extracts 1D embedding
      ↓
[Bing/Scrape.do] → Fetches dynamic web candidates
      ↓
[Face Matcher] → Compares embeddings (cosine similarity)
      ↓
[Best Match]
      ↓
[SHA-256 Fingerprint] → Hash of (Image Hash + Match Metadata)
      ↓
[Web3/Ethereum Contract] → Immutable record
      ↓
[Verification CLI] → Fetches on-chain hash & compares with recalculated hash
```

## 3. Tech Stack
- **Python**: 3.8+
- **Face Recognition**: `deepface` (FaceNet model)
- **Web Search**: Bing Visual Search (proxied via `scrape.do`)
- **Blockchain integration**: `web3.py`
- **Smart Contracts**: Solidity
- **Blockchain Network**: Local Ganache or Ethereum testnets (Sepolia)
- **Hashing**: SHA-256

## 4. Installation
1. Clone the repository and enter the directory.
2. Create and activate a virtual environment (optional but recommended).
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 5. Environment Variables
1. Copy the example configuration:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and fill in the required keys. Do NOT commit your `.env` file to version control.
   - `SCRAPE_DO_API_KEY`: Required for fetching reverse image search results.
   - `WEB3_RPC_URL`: URL to your Ethereum node or local Ganache (e.g., `http://127.0.0.1:8545`).
   - `PRIVATE_KEY`: Your wallet's private key (without `0x`).
   - `CONTRACT_ADDRESS`: The deployed contract address (see step 3 below).
   - `NETWORK`: e.g., `local` or `sepolia`.

3. Deploy the Smart Contract (make sure your network/Ganache is running):
   ```bash
   python scripts/deploy_contract.py
   ```
   *Take the output address and add it as `CONTRACT_ADDRESS` in `.env`.*

## 6. Running
Start the interactive CLI:
```bash
python main.py
```
You will be prompted to select an action:
- Run full pipeline
- Verify blockchain record
- Test tampered content

If you choose to run the pipeline, you can enter the path to a local image and its public URL (for reverse searching), or leave it blank to use the provided sample.

## 7. Blockchain Verification
The system stores the SHA-256 cryptographic fingerprint (a combination of the image file hash and the canonical JSON of the search result metadata) on the specified Ethereum-compatible blockchain. 
By placing only the hash on-chain, large media and private data remain off-chain, ensuring efficiency and privacy. Verification involves reading the stored `bytes32` hash from the contract and ensuring it matches the locally re-calculated fingerprint.

## 8. Verification
To verify the integrity of the latest run, choose option `2` from the CLI menu (`Verify blockchain record`). The system will load the saved local record metadata, re-calculate the SHA-256 fingerprint, retrieve the stored hash from the blockchain using the saved record ID, and compare them.

## 9. Tamper Detection
Choose option `3` (`Test tampered content`) in the CLI menu. This intentionally alters the title of the stored search result metadata and recalculates the hash. When compared to the blockchain record, it will correctly fail verification, proving that any modification to the discovered content can be detected.

## 10. Limitations
- **Search Provider Limitations**: Bing/Scrape.do rate limits and captchas may occasionally cause the search step to fail.
- **Face Recognition**: FaceNet is highly accurate but can produce false positives or fail to detect faces in low-light/low-quality images.
- **Public URL Requirement**: The reverse image search requires a publicly accessible URL of the face image.
- **Network Dependency**: Uploading to public testnets requires gas and network availability.

## 11. Security + Privacy
- **Responsible Use**: Use only images/data you have permission to process. This tool is built strictly for verifying content about a consenting subject.
- **Data Minimization**: Avoid storing unnecessary personal data.
- **On-chain Data**: Only irreversible cryptographic hashes/fingerprints are placed on the blockchain, protecting privacy.
- **False Positives**: Results from face recognition models should not be treated as definitive identity proof without human oversight.

## 12. Demo Instructions
To record a clean demonstration of the pipeline:
1. Ensure your local blockchain (Ganache) is running and `.env` is configured.
2. Run `python scripts/deploy_contract.py` and update `.env`.
3. Start the application: `python main.py`
4. **Choose Option 1 (Run full pipeline)**. Press Enter twice to use the default sample image.
5. Watch the CLI output as it detects the face, dynamically searches the web, downloads and compares candidates, and stores the hash on the blockchain.
6. **Choose Option 2 (Verify blockchain record)**. Show that the recalculated hash matches the on-chain hash (VERIFIED ✓).
7. **Choose Option 3 (Test tampered content)**. Show that modifying the local data causes a hash mismatch (VERIFICATION FAILED ✗).
8. Exit the CLI.
