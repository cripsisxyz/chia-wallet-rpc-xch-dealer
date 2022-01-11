# Chia XCH Wallet Dealer

![hello](doc/chia-wallet-dealer.png)

## Description
Welcome to Chia RPC XCH Wallet Dealer. The purpose of this project is fractionate and send XCH of an existing and synced chia wallet (using the Chia RPC Protocol) to multiple wallets destinations, using partitions rules on a config file.
Developed and tested only with the official [chia-blockchain](https://github.com/Chia-Network/chia-blockchain) project.

If you found the project useful, please consider a donation to my chia wallet :) 

![walleticon](doc/xch-icon.png) `xch1vt3g694eclvcjmrj8mq83vtgrva9sw0qdz34muxrqjh5y5fzq6vq89n605`

## Requirements
Attending the official [chia RPC doc](https://docs.chia.net/docs/12rpcs/rpcs/) you need a wallet listening via RPC Protocol, built with a default installation.

You may also need Python interpreter (3.x) installed on your system and it is recommended to use pipenv for installing all libraries dependencies. You can install it with 

```bash
pip3 install pipenv
```

## Usage 
### The environment
* Install the environment with 

```bash
pipenv install
```

* Enter in the environment with 

```bash
pipenv shell
```

You can also execute xchdealer without entering in the environment, using `pipenv run python xchdealer.py [params]`, example:

```
pipenv run python xchdealer.py --help

usage: xchdealer.py [-h] -f CONFIG_FILE [-m {simulate,execute}]
...

```
### Edit the config
* Edit config_example.yaml to your needs and rename it if you want

## Config file
Example of config file:
```yaml
---
rpc_connector: 
  host: "localhost" #Host of the wallet
  port: 9256 #Port of the rpc wallet
  private_wallet_cert_path: "~/.chia/mainnet/config/ssl/wallet/private_wallet.crt" #Private certificate to connect with RPC
  private_wallet_key_path: "~/.chia/mainnet/config/ssl/wallet/private_wallet.key" #Key of the certificate to connect with RP
dealer:
  source_wallet:
    id: 1 #ID of source wallet, can be identified launching in simulate mode
    distribute_percentage_of_total: 100.0 #Percentage of all amount will be distributed, the rest keep on the wallet
    fee: 0 #Transaction fee, default 0
  destination_wallets:
    - name: "iv-vz" #For each destination specify a name
      address: "xch1vt3g694eclvcjmrj8mq83vtgrva9sw0qdz34muxrqjh5y5fzq6vq89n605" #Address of the destination wallet
      distribution_percentage: 90.0 #Percentage of total amount assigned to this wallet
    - name: "alber" 
      address: "xch1vt3g694eclvcjmrj8mq83vtgrva9sw0qdz34muxrqjh5y5fzq6vq89n605"
      distribution_percentage: 10.0

#The sum of all distribution_percentage of destination_wallets must be equal to 100.0
```

## Arguments

### Simulate mode

* You can execute xchdealer in simulate mode to show only the dealing results, check the config or identify the id of source wallet. Run:

```bash
python xchdealer.py -f config_example.yaml -m simulate
```

### Execute mode

* If you are sure of the result, you can execute the real transactions with:

```bash
python xchdealer.py -f config_example.yaml -m execute
```

## Example execution output

### Simulate mode

```
$ pipenv run python xchdealer.py -f config_example.yaml -m simulate

[INFO]|2022-01-23 10:42:49,926|xchdealer.py|<module>|Welcome to Chia XCH RPC Dealer
[INFO]|2022-01-23 10:42:49,927|xchdealer.py|load_config_file|Successfully loaded config file config_example.yaml
[INFO]|2022-01-23 10:42:49,928|xchrpc.py|__init__|RPC connector set to localhost:9256 using certs ('/home/zxs/.chia/mainnet/config/ssl/wallet/private_wallet.crt', '/home/zxs/.chia/mainnet/config/ssl/wallet/private_wallet.key')
[INFO]|2022-01-23 10:42:49,928|xchdealer.py|<module>|XCH Dealer routine set to simulate mode
[INFO]|2022-01-23 10:42:49,928|xchrpc.py|check_available_wallets|Checking available RPC chia wallets
[INFO]|2022-01-23 10:42:49,936|xchrpc.py|check_available_wallets|Connection with chia RPC protocol sucessfull
[INFO]|2022-01-23 10:42:49,936|xchrpc.py|check_available_wallets|Available wallets: [{'data': '', 'id': 1, 'name': 'Chia Wallet', 'type': 0}]
[INFO]|2022-01-23 10:42:49,936|xchrpc.py|check_wallets_synced|Checking chia wallets synced
[INFO]|2022-01-23 10:42:49,942|xchrpc.py|check_wallets_synced|Wallets are NOT syncing with network
[INFO]|2022-01-23 10:42:49,942|xchrpc.py|check_wallets_synced|Wallets are correctly synced with network
[INFO]|2022-01-23 10:42:49,942|xchrpc.py|check_wallet_balance|Checking XCH balance on wallet id 1
[INFO]|2022-01-23 10:42:49,952|xchrpc.py|check_wallet_balance|Available balance for sending (max_send_amount): 217771 MOJOs == 0.000000217771 XCH
[INFO]|2022-01-23 10:42:49,952|xchdealer.py|check_percentages|All percentages in config are correctly set and pass checksum test
[INFO]|2022-01-23 10:42:49,952|xchdealer.py|calculate_deals|Calculating proportions of deal
[INFO]|2022-01-23 10:42:49,952|xchdealer.py|calculate_deals|1.0% of the total amount will be dealed: 2177 MOJOs
[INFO]|2022-01-23 10:42:49,952|xchdealer.py|calculate_deals|iv-vz will receive 2177 MOJOs == 0.000000002177 XCH
[INFO]|2022-01-23 10:42:49,952|xchdealer.py|<module>|Simulate mode finished, if you want to apply and send XCH launch xchdealer in 'execute' mode
```

### Execute mode
```
$ pipenv run python xchdealer.py -f config_example.yaml -m execute

[INFO]|2022-01-23 10:48:09,499|xchdealer.py|<module>|Welcome to Chia XCH RPC Dealer
[INFO]|2022-01-23 10:48:09,501|xchdealer.py|load_config_file|Successfully loaded config file config_example.yaml
[INFO]|2022-01-23 10:48:09,501|xchrpc.py|__init__|RPC connector set to localhost:9256 using certs ('/home/zxs/.chia/mainnet/config/ssl/wallet/private_wallet.crt', '/home/zxs/.chia/mainnet/config/ssl/wallet/private_wallet.key')
[INFO]|2022-01-23 10:48:09,501|xchdealer.py|<module>|XCH Dealer routine set to execute mode
[INFO]|2022-01-23 10:48:09,501|xchrpc.py|check_available_wallets|Checking available RPC chia wallets
[INFO]|2022-01-23 10:48:09,510|xchrpc.py|check_available_wallets|Connection with chia RPC protocol sucessfull
[INFO]|2022-01-23 10:48:09,510|xchrpc.py|check_available_wallets|Available wallets: [{'data': '', 'id': 1, 'name': 'Chia Wallet', 'type': 0}]
[INFO]|2022-01-23 10:48:09,510|xchdealer.py|default_routine|Configured source wallet id: 1 is available, using it to operate
[INFO]|2022-01-23 10:48:09,510|xchrpc.py|check_wallet_balance|Checking XCH balance on wallet id 1
[INFO]|2022-01-23 10:48:09,518|xchrpc.py|check_wallet_balance|Available balance for sending (max_send_amount): 217771 MOJOs == 0.000000217771 XCH
[INFO]|2022-01-23 10:48:09,518|xchdealer.py|check_percentages|All percentages in config are correctly set and pass checksum test
[INFO]|2022-01-23 10:48:09,518|xchdealer.py|calculate_deals|Calculating proportions of deal
[INFO]|2022-01-23 10:48:09,518|xchdealer.py|calculate_deals|1.0% of the total amount will be dealed: 2177 MOJOs
[INFO]|2022-01-23 10:48:09,518|xchdealer.py|calculate_deals|iv-vz will receive 2177 MOJOs == 0.000000002177 XCH
[INFO]|2022-01-23 10:48:09,518|xchdealer.py|default_routine|Preparing transaction to iv-vz with 0.000000002177 XCH
[INFO]|2022-01-23 10:48:09,518|xchrpc.py|send_wallet_transaction|Sending 2177 MOJO to address xch1vt3g694eclvcjmrj8mq83vtgrva9sw0qdz34muxrqjh5y5fzq6vq89n605
[INFO]|2022-01-23 10:48:09,634|xchrpc.py|send_wallet_transaction|Transaction successfully sent/registered!
[INFO]|2022-01-23 10:48:09,634|xchrpc.py|send_wallet_transaction|Transaction ID: 0xf874f58c59f350e12c171e7972b0bc518fc53d4f7d4577474c3eb593471c0d73
```