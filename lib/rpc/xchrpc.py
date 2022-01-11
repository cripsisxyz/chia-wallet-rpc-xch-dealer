import logging, requests, json
from os.path import expanduser
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from lib.dealermath.dealermath import DealerMath

class RemoteProcedureCall():

    def __init__(self, host="localhost", port=9256, private_wallet_cert_path="~/.chia/mainnet/config/ssl/wallet/private_wallet.crt", private_wallet_key_path="~/.chia/mainnet/config/ssl/wallet/private_wallet.key"):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        self.default_rpc_headers = {'Content-Type': 'application/json'}
        self.default_wallet_certs = (expanduser(private_wallet_cert_path), expanduser(private_wallet_key_path))
        self.host = host
        self.port = port

        logging.info(f"RPC connector set to {self.host}:{str(self.port)} using certs {str(self.default_wallet_certs)}")


    def check_available_wallets(self):
        logging.info('Checking available RPC chia wallets')

        request_data = {"wallet_id": "*"}
        try:
            response = requests.post(f"https://{self.host}:{str(self.port)}/get_wallets", headers=self.default_rpc_headers, json=request_data, cert=self.default_wallet_certs, verify=False)
            response.raise_for_status()
        except Exception as e:
            logging.error(f"Cannot get available RPC chia wallets {str(e)}")
            return(False)
        else:
            available_wallets = json.loads(response.text)['wallets']
            logging.info(f"Connection with chia RPC protocol sucessfull")
            logging.info(f"Available wallets: {available_wallets}")
            return(available_wallets)

    def check_wallets_synced(self):
        logging.info(f"Checking chia wallets synced")

        request_data = {}
        try:
            response = requests.post(f"https://{self.host}:{str(self.port)}/get_sync_status", headers=self.default_rpc_headers, json=request_data, cert=self.default_wallet_certs, verify=False)
            response.raise_for_status()
        except Exception as e:
            logging.error(f"Cannot get RPC chia wallets sync status {str(e)}")
            return(False)
        else:
            loaded_json = json.loads(response.text)
            if loaded_json["syncing"]:
                logging.info(f"Wallets are syncing with network")
            else:
                logging.info(f"Wallets are NOT syncing with network")

            if loaded_json["synced"]:
                logging.info(f"Wallets are correctly synced with network")
            else:
                logging.warning(f"Wallets are NOT synced with network")
                return(False)

    def check_wallet_balance(self, wallet_id=int):
        logging.info(f"Checking XCH balance on wallet id {str(wallet_id)}")

        request_data = {"wallet_id": wallet_id}
        try:
            response = requests.post(f"https://{self.host}:{str(self.port)}/get_wallet_balance", headers=self.default_rpc_headers, json=request_data, cert=self.default_wallet_certs, verify=False)
            response.raise_for_status()
        except Exception as e:
            logging.error(f"Cannot get available RPC chia wallets {str(e)}")
            return(False)
        else:
            max_send_amount_mojo = int(json.loads(response.text)["wallet_balance"]["max_send_amount"])
            max_send_amount_xch_str = DealerMath.mojo_to_xch_str(max_send_amount_mojo)
            logging.info(f"Available balance for sending (max_send_amount): {str(max_send_amount_mojo)} MOJOs == {str(max_send_amount_xch_str)} XCH")

            return(max_send_amount_mojo, max_send_amount_xch_str)

    def send_wallet_transaction(self, source_wallet_id=int, amount=int, destination_wallet_address=str, fee=0):
        logging.info(f"Sending {str(amount)} MOJO to address {destination_wallet_address}")

        request_data = {
            "wallet_id": source_wallet_id,
            "amount": amount,
            "address": destination_wallet_address,
            "fee": fee
            }
        try:
            response = requests.post(f"https://{self.host}:{str(self.port)}/send_transaction", headers=self.default_rpc_headers, json=request_data, cert=self.default_wallet_certs, verify=False)
            response.raise_for_status()
        except Exception as e:
            logging.error(str(e))
            return(False)
        else:
            loaded_json = json.loads(response.text)
            if loaded_json["success"]:
                logging.info(f"Transaction successfully sent/registered!")
                logging.info(f"Transaction ID: {loaded_json['transaction_id']}")
                return(True)
            else:
                logging.error(f"Cannot send transaction! {str(response.text)}")
            return(False)
            
