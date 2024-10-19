import random
import time
import eth_account.signers.local
import web3
from web3 import Web3, Account
from config import RPC_URL, CONTRACT_ADDRESS, CONTRACT_METHOD, CHAIN_ID


def get_logo():
    print("""
██╗░░░░░░█████╗░██╗░░░██╗███████╗██████╗░  ░█████╗░██╗██████╗░██████╗░██████╗░░█████╗░██████╗░
██║░░░░░██╔══██╗╚██╗░██╔╝██╔════╝██╔══██╗  ██╔══██╗██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗
██║░░░░░███████║░╚████╔╝░█████╗░░██████╔╝  ███████║██║██████╔╝██║░░██║██████╔╝██║░░██║██████╔╝
██║░░░░░██╔══██║░░╚██╔╝░░██╔══╝░░██╔══██╗  ██╔══██║██║██╔══██╗██║░░██║██╔══██╗██║░░██║██╔═══╝░
███████╗██║░░██║░░░██║░░░███████╗██║░░██║  ██║░░██║██║██║░░██║██████╔╝██║░░██║╚█████╔╝██║░░░░░
╚══════╝╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝  ╚═╝░░╚═╝╚═╝╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░░░░
Telegram community: https://t.me/layerairdrop
""")


def menu() -> int:
    x = None
    while not x:
        print("""
1) Enter your seed phrase
2) Generate and use a new wallet
3) Enter your private key
        """)
        x = input("-> ")
    return int(x)


def get_account_from_seed(w3: web3.Web3) -> eth_account.signers.local.LocalAccount:
    w3.eth.account.enable_unaudited_hdwallet_features()
    print("Enter your seed phrase:")
    phrase = input("-> ")
    try:
        account = w3.eth.account.from_mnemonic(phrase)
        print(f"Your wallet address: {account.address}")
        return account
    except Exception as e:
        print(e)
        main()


def generate_account(w3: web3.Web3) -> eth_account.signers.local.LocalAccount:
    w3.eth.account.enable_unaudited_hdwallet_features()
    print("Generating a new wallet...")
    account, mnemonic = w3.eth.account.create_with_mnemonic()
    print(f"Your wallet address: {account.address}")
    print(f"Your wallet seed phrase: {mnemonic}")
    print(f"Your wallet private key: {account.key.hex()}")
    return account


def get_account_from_private_key(w3: web3.Web3) -> eth_account.signers.local.LocalAccount:
    print("Enter your private key:")
    private_key = input("-> ")
    try:
        account = w3.eth.account.from_key(private_key)
        print(f"Your wallet address: {account.address}")
        return account
    except Exception as e:
        print(f"Invalid private key: {e}")
        main()


def check_eth_balance(w3: web3.Web3, account: eth_account.signers.local.LocalAccount):
    balance = w3.from_wei(w3.eth.get_balance(account.address), "ether")
    print(f"Your wallet balance: {balance} ETH")
    if balance < 0.00001:
        print("Request some funds for your wallet using this link:")
        print("https://rivalz2.hub.caldera.xyz/")
        input("Then press Enter")
    else:
        input("Press Enter to start auto-claim")


def claim_nft(w3: web3.Web3, account: eth_account.signers.local.LocalAccount):
    nonce = w3.eth.get_transaction_count(account.address)
    gas_price = w3.eth.gas_price
    transaction = {
        'to': CONTRACT_ADDRESS,
        'value': 0,
        'data': CONTRACT_METHOD,
        'chainId': CHAIN_ID,
        'nonce': nonce,
        'gas': 180000,  # Adjusted gas limit based on trace
        'gasPrice': gas_price
    }
    try:
        # Estimate gas limit (to verify against the 300k gas setting)
        estimated_gas = w3.eth.estimate_gas(transaction)
        print(f"Estimated gas: {estimated_gas}")
        transaction['gas'] = estimated_gas  # Apply the estimated gas limit

        # Sign and send the transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, account.key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"NFT claim hash: {tx_hash.hex()}")

        # Wait for transaction receipt to check success
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print("Transaction succeeded")
        else:
            print("Transaction failed")
    except Exception as e:
        print(f"Transaction error: {e}")


def main() -> None:
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if w3.is_connected():
        choice = menu()
        if choice == 1:
            account = get_account_from_seed(w3)
        elif choice == 2:
            account = generate_account(w3)
        elif choice == 3:
            account = get_account_from_private_key(w3)
        check_eth_balance(w3, account)

        while True:
            print("Starting claim process")
            for i in range(20):
                claim_nft(w3, account)
                print(f"{i + 1} claim request sent successfully")
                time.sleep(random.randint(5, 15))  # Random delay between claims
            print("Waiting 12 hours cooldown")
            time.sleep(43260)  # 12 hours + 1 minute cooldown
    else:
        print("Web3 connection failed!")
        print("Check your internet connection")


if __name__ == "__main__":
    get_logo()
    main()
