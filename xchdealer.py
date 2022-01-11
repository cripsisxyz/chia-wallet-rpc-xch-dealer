#!/bin/python
import argparse, requests, logging, sys, yaml
from lib.rpc.xchrpc import RemoteProcedureCall
from lib.dealermath.dealermath import DealerMath

def set_app_logger():
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s]|%(asctime)s|%(filename)s|%(funcName)s|%(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

def get_app_argparse():
    parser = argparse.ArgumentParser(description='Fractionate and send XCH of a chia wallet (using the Chia RPC Protocol) to multiple wallets destinations using partitions rules on a config file.')

    parser.add_argument('-f', '--config-file', type=str, help='YAML config file', required=True)
    parser.add_argument('-m', '--mode',
                        type=str,
                        choices=['simulate', 'execute'],
                        default='simulate', required=False,
                        help='Simulate only or really execute the deal')
    
    global args
    args = parser.parse_args()

def load_config_file():
    global config
    try:
        with open(args.config_file, 'r') as file:
            config = yaml.full_load(file)
    except Exception as e:
        logging.error(f"Cannot open config file {args.config_file}: {str(e)}")
        exit(1)
    else:
        logging.info(f"Successfully loaded config file {args.config_file}")

def calculate_deals(total_mojos, total_xch_str):
    logging.info(f"Calculating proportions of deal")
    dealing_total_mojo = DealerMath.calculate_proportion(total_mojos, float(config['dealer']['source_wallet']['distribute_percentage_of_total']))

    logging.info(f"{str(config['dealer']['source_wallet']['distribute_percentage_of_total'])}% of the total amount will be dealed: {str(dealing_total_mojo)} MOJOs")

    deals = {}

    for count, dest in enumerate(config['dealer']['destination_wallets']):
        will_receive_mojos = DealerMath.calculate_proportion(dealing_total_mojo, float(config['dealer']['destination_wallets'][count]['distribution_percentage']))
        deals[dest['name']] = {'address': dest['address'], 'mojo': will_receive_mojos, 'xch': DealerMath.mojo_to_xch_str(will_receive_mojos)}
        logging.info(f"{dest['name']} will receive {will_receive_mojos} MOJOs == {DealerMath.mojo_to_xch_str(will_receive_mojos)} XCH")

    return(deals)

def check_percentages():
    try:
        DealerMath.check_sum([d['distribution_percentage'] for d in config['dealer']['destination_wallets']], 100.0)
    except Exception as e:
        logging.error(f"Incorrect configurated distribution percentages: {str(e)}")
        exit(1)
    else:
        logging.info(f"All percentages in config are correctly set and pass checksum test")

def default_routine():
    available_wallets = rpc.check_available_wallets()
    if available_wallets == False:
        exit(1)

    if any(d['id'] == config["dealer"]["source_wallet"]["id"] for d in available_wallets):
        logging.info(f"Configured source wallet id: {str(config['dealer']['source_wallet']['id'])} is available, using it to operate")
    else:
        logging.error(f"Configured source wallet id: {str(config['dealer']['source_wallet']['id'])} not in available wallets")
        exit(1)

    max_send_amount_mojo, max_send_amount_xch_str = rpc.check_wallet_balance(wallet_id=int(config['dealer']['source_wallet']['id']))
    check_percentages()
    deals = calculate_deals(max_send_amount_mojo, max_send_amount_xch_str)

    for name, data in deals.items():
        logging.info(f"Preparing transaction to {name} with {data['xch']} XCH")
        rpc.send_wallet_transaction(source_wallet_id=config['dealer']['source_wallet']['id'], amount=data['mojo'], destination_wallet_address=data['address'])
        
def check_only_routine():
    rpc.check_available_wallets()
    rpc.check_wallets_synced()
    max_send_amount_mojo, max_send_amount_xch_str = rpc.check_wallet_balance(wallet_id=int(config['dealer']['source_wallet']['id']))
    check_percentages()
    deals = calculate_deals(max_send_amount_mojo, max_send_amount_xch_str)

if __name__ == "__main__":
    get_app_argparse()
    set_app_logger()
    logging.info(f"Welcome to Chia XCH RPC Dealer")
    load_config_file()
    
    rpc = RemoteProcedureCall(
        host=config["rpc_connector"]["host"], 
        port=int(config["rpc_connector"]["port"]), 
        private_wallet_cert_path=config["rpc_connector"]["private_wallet_cert_path"], 
        private_wallet_key_path=config["rpc_connector"]["private_wallet_key_path"])

    logging.info(f"XCH Dealer routine set to {args.mode} mode")

    if args.mode == "simulate":
        check_only_routine()
        logging.info(f"Simulate mode finished, if you want to apply and send XCH launch xchdealer in 'execute' mode")
    elif args.mode == "execute":
        default_routine()
    else:
        logging.error(f"Only simulate or execute modes can be set")
        exit(1)
    exit(0)
    

