#!/bin/python3

import requests
import json
import etherscan

detail = requests.get("https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash=%s&apikey=%s" % (transaction['hash'], API_KEY))

'''
API_KEY = '7AHYYFHS91RFIRZFYWJB83Z1XU8XPGCN37'

es = etherscan.Client(api_key = API_KEY)

Uniswap2_Contract = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'

transactions = es.get_transactions_by_address(Uniswap2_Contract)
for transaction in transactions:
    print(json.dumps(transaction, indent=1))
    if transaction['value'] > 0:
        detail = requests.get("https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash=%s&apikey=%s" % (transaction['hash'], API_KEY))
        data = json.loads(detail.text)
        print(json.dumps(data, indent=1))
        sys.exit(0)
'''
#
# tx_json_data = json.loads(get_tx_by_hash.text)
# print(tx_json_data)

#res = requests.get("https://api.etherscan.io/api?module=account&action=tokentx&contractaddress=%s&page=1&offset=100&sort=asc&apikey=%s" % (Uniswap2_Contract, API_KEY))
#json_data = json.loads(res.text)
#print(json_data)
#result = json_data["result"]
#json_formatted_str = json.dumps(result, indent=2)
#
# # print(json_formatted_str)
#
