from web3 import Web3
import json

# Connect to Ethereum network (use Ganache, Infura, or local node)
infura_url = "https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Check connection
if not web3.is_connected():
    raise Exception("Failed to connect to Ethereum network")

# Contract details (replace with your compiled ABI & contract address)
contract_address = "YOUR_DEPLOYED_CONTRACT_ADDRESS"
with open("TodoList_abi.json") as f:
    contract_abi = json.load(f)

# Load contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Private key and sender address
private_key = "YOUR_PRIVATE_KEY"
sender_address = web3.eth.account.from_key(private_key).address

def add_task(description):
    """Add a new task to the blockchain."""
    nonce = web3.eth.get_transaction_count(sender_address)
    txn = contract.functions.addTask(description).build_transaction({
        'from': sender_address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': web3.to_wei('10', 'gwei')
    })
    
    signed_txn = web3.eth.account.sign_transaction(txn, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print("Task added! TX Hash:", web3.to_hex(tx_hash))

def get_task(task_id):
    """Retrieve a specific task by ID."""
    description, completed = contract.functions.getTask(task_id).call()
    status = "Completed" if completed else "Pending"
    print(f"Task {task_id}: {description} - {status}")

def complete_task(task_id):
    """Mark a task as completed."""
    nonce = web3.eth.get_transaction_count(sender_address)
    txn = contract.functions.completeTask(task_id).build_transaction({
        'from': sender_address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': web3.to_wei('10', 'gwei')
    })
    
    signed_txn = web3.eth.account.sign_transaction(txn, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"Task {task_id} marked as completed! TX Hash:", web3.to_hex(tx_hash))

def get_all_tasks():
    """Fetch all tasks from the blockchain."""
    tasks = contract.functions.getAllTasks().call()
    for task in tasks:
        status = "Completed" if task[2] else "Pending"
        print(f"Task {task[0]}: {task[1]} - {status}")

# Example Usage
if __name__ == "__main__":
    add_task("Buy groceries")
    add_task("Complete blockchain project")
    get_all_tasks()
    complete_task(0)
    get_task(0)
