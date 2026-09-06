import os
import sys
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
import solcx

# Add parent dir to path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def compile_source_file(file_path):
    print("Compiling smart contract... (may download solc compiler on first run)")
    # Install specific compiler version if needed
    solcx.install_solc('0.8.0')
    with open(file_path, 'r') as f:
        source = f.read()
    
    compiled_sol = solcx.compile_source(
        source,
        output_values=['abi', 'bin'],
        solc_version='0.8.0'
    )
    # Get the first contract interface
    contract_id, contract_interface = compiled_sol.popitem()
    return contract_interface['abi'], contract_interface['bin']

def deploy():
    w3 = Web3(Web3.HTTPProvider(config.WEB3_RPC_URL))
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
    
    if not w3.is_connected():
        print(f"Failed to connect to Web3 RPC URL: {config.WEB3_RPC_URL}")
        return

    if not config.PRIVATE_KEY or config.PRIVATE_KEY == "your_private_key_without_0x_prefix":
        print("PRIVATE_KEY is not set or invalid in .env file.")
        return

    account = w3.eth.account.from_key(config.PRIVATE_KEY)
    print(f"Deploying from account: {account.address}")
    
    contract_path = os.path.join(os.path.dirname(__file__), '..', 'contracts', 'RecordStore.sol')
    abi, bytecode = compile_source_file(contract_path)
    
    RecordStore = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    tx = RecordStore.constructor().build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 3000000,
        'gasPrice': w3.eth.gas_price
    })
    
    print("Sending deployment transaction...")
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=config.PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    print(f"Deployment transaction hash: {w3.to_hex(tx_hash)}")
    print("Waiting for receipt...")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    if receipt.status == 1:
        print(f"Contract deployed successfully at address: {receipt.contractAddress}")
        print(f"Update your .env file with: CONTRACT_ADDRESS={receipt.contractAddress}")
    else:
        print("Contract deployment failed.")

if __name__ == "__main__":
    deploy()
