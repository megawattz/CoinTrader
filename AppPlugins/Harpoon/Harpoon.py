#!/bin/python3

import json
import requests

payload = {"query":'''
query (
  $network: EthereumNetwork!,
  $limit: Int!,
  $offset: Int!$from: ISO8601DateTime,
  $till: ISO8601DateTime) {
    ethereum(network: $network) {
      dexTrades(options: {
        desc: ["block.height","tradeIndex"], 
        limit: $limit, offset: $offset
    },
    date: {
      since: $from till: $till
    }) {
  block {
    timestamp {
      time (format: "%Y-%m-%d %H:%M:%S")
    } 
    height
  } 
  tradeIndex protocol exchange {
    fullName
  } 
  smartContract {
    address {
      address annotation
    }
  } 
  buyAmount buyCurrency { 
    address symbol
  } 
  sellAmount sellCurrency { 
    address symbol
  }
  transaction {
    hash 
  } 
} } }''',"variables":'{"limit":10,"offset":10,"network":"ethereum","from":"2021-03-11","till":null,"dateFormat":"%Y-%m-%d"}'}

result = requests.post('https://graphql.bitquery.io/',
 data=payload
 )

print(result.headers)

print(json.dumps(json.loads(result.text), indent=1))
