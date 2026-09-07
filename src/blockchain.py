from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def get_web3():
    w3 = Web3(Web3.HTTPProvider(config.WEB3_RPC_URL))
    # Inject middleware for PoA networks (like testnets/Ganache)
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
    if not w3.is_connected():
        raise ConnectionError(f"Failed to connect to Web3 RPC URL: {config.WEB3_RPC_URL}")
    return w3

def get_contract(w3):
    if not config.CONTRACT_ADDRESS:
        raise ValueError("CONTRACT_ADDRESS is not set in config.")
    
    # Minimal ABI for RecordStore
    abi = [
        {
            "inputs": [{"internalType": "bytes32", "name": "hash", "type": "bytes32"}],
            "name": "storeRecord",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [{"internalType": "uint256", "name": "id", "type": "uint256"}],
            "name": "getRecord",
            "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "recordCount",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "anonymous": False,
            "inputs": [
                {"indexed": False, "internalType": "uint256", "name": "id", "type": "uint256"},
                {"indexed": False, "internalType": "bytes32", "name": "hash", "type": "bytes32"}
            ],
            "name": "RecordStored",
            "type": "event"
        }
    ]
    # FIXED: wrap address with Web3.to_checksum_address to resolve EIP-55 checksum error
    return w3.eth.contract(address=Web3.to_checksum_address(config.CONTRACT_ADDRESS), abi=abi)

def store_record(fingerprint_hex: str) -> int:
    w3 = get_web3()
    contract = get_contract(w3)
    
    if not config.PRIVATE_KEY or config.PRIVATE_KEY == "your_private_key_without_0x_prefix":
        raise ValueError("PRIVATE_KEY is not set or invalid in .env file.")

    account = w3.eth.account.from_key(config.PRIVATE_KEY)
    
    # Convert hex string to bytes32
    fingerprint_bytes = Web3.to_bytes(hexstr=fingerprint_hex)
    
    # Build transaction
    tx = contract.functions.storeRecord(fingerprint_bytes).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price
    })
    
    # Sign & send
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=config.PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    print(f"Transaction sent! Hash: {w3.to_hex(tx_hash)}")
    
    # Wait for receipt
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    if receipt.status != 1:
        raise RuntimeError("Transaction failed.")
    
    # Parse event logs to get the newly created record ID
    logs = contract.events.RecordStored().process_receipt(receipt)
    if logs:
        return logs[0]['args']['id']
    else:
        # Fallback if event is not found
        count = contract.functions.recordCount().call()
        return count - 1

def store_record_with_tx(fingerprint_hex: str) -> tuple:
    w3 = get_web3()
    contract = get_contract(w3)
    
    if not config.PRIVATE_KEY or config.PRIVATE_KEY == "your_private_key_without_0x_prefix":
        raise ValueError("PRIVATE_KEY is not set or invalid in .env file.")

    account = w3.eth.account.from_key(config.PRIVATE_KEY)
    
    # Convert hex string to bytes32
    fingerprint_bytes = Web3.to_bytes(hexstr=fingerprint_hex)
    
    # Build transaction
    tx = contract.functions.storeRecord(fingerprint_bytes).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price
    })
    
    # Sign & send
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=config.PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    tx_hash_hex = w3.to_hex(tx_hash)
    
    # Wait for receipt
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    if receipt.status != 1:
        raise RuntimeError("Transaction failed.")
    
    # Parse event logs to get the newly created record ID
    logs = contract.events.RecordStored().process_receipt(receipt)
    if logs:
        record_id = logs[0]['args']['id']
    else:
        # Fallback if event is not found
        count = contract.functions.recordCount().call()
        record_id = count - 1
        
    return record_id, tx_hash_hex

def get_record(record_id: int) -> str:
    w3 = get_web3()
    contract = get_contract(w3)
    
    fingerprint_bytes = contract.functions.getRecord(record_id).call()
    return Web3.to_hex(fingerprint_bytes)