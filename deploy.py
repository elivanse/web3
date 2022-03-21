import json

from solcx import compile_standard, install_solc
from web3 import Web3

install_solc("0.6.0")

with open("SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# compile our solidity

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "SimpleStorage.sol": {
                "content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}

            }
        },
    },
    solc_version="0.6.0",
)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)
# print(compiled_sol)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# web3
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337
my_address = "0x211E024F0cAeDA202fA13538fd42D79C218b4DaD"
private_key = "0x510147c1c835c1efd6c461cf9c060b6d2084fc1ae8edd03b8e09b6694c671359"

# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get latest transaction nonce cant de transacciones hechas con la cuenta
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)

# Build a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address, 
        "nonce": nonce
    }
)
print(transaction)

# Sign a transaction
signed_txn = w3.eth.account.sign_transaction(transaction,private_key=private_key)

# Send a transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# para trabajar con contratos  siempre necesitamos
# address del contrato
# ABI  del contrato
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Call -> Simulate making the call and getting a return value
# Transact -> Actually make a state change

# print(simple_storage.functions.retrieve().call)
# creamos la transaccion
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId":chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address, 
        "nonce": nonce + 1
    }
)
# firmamos la transaccion
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction,private_key=private_key
)
# enviamos la transaccion
send_store_tx = w3.eth.send_transaction(signed_store_txn.rawTransaction)

# esperamos 

tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print(simple_storage.functions.retrieve().call())

#
