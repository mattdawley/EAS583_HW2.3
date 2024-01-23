from web3 import Web3, contract
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
import requests
import json
import time

bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
#contract_address = Web3.to_checksum_address(bayc_address)
contract_address = Web3.toChecksumAddress(bayc_address)

#You will need the ABI to connect to the contract
#The file 'abi.json' has the ABI for the bored ape contract
#In general, you can get contract ABIs from etherscan
#https://api.etherscan.io/api?module=contract&action=getabi&address=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D

with open('/home/codio/workspace/abi.json', 'r') as f:
#with open('abi.json','r') as f:
	abi = json.load(f)

############################
#Connect to an Ethereum node
api_url = "https://mainnet.infura.io/v3/7d971d5755d142b49329f02a8bfd5d72"
provider = HTTPProvider(api_url)
web3 = Web3(provider)

def get_ape_info(apeID):
	assert isinstance(apeID,int), f"{apeID} is not an int"
	assert 1 <= apeID, f"{apeID} must be at least 1"

	# create contract variable
	contract = web3.eth.contract(address=bayc_address, abi=abi)

	# get uri and owner of given ape id
	result = contract.functions.tokenURI(apeID).call()
	owner = contract.functions.ownerOf(apeID).call()

	# get data for given ape
	uri = result.replace("ipfs://","")
	base_url = "https://gateway.pinata.cloud/ipfs/"
	pinata_gateway_url = base_url+uri
	headers = {"content_type": "json"}
	response = requests.get(pinata_gateway_url, headers)
	j_data = response.json()

	#Determine eye color
	eye_color = None
	for attr in j_data["attributes"]:
		if attr["trait_type"] == "Eyes":
			eye_color = attr["value"]

	data = {'owner': owner, 'image': j_data["image"], 'eyes': eye_color }

	assert isinstance(data,dict), f'get_ape_info{apeID} should return a dict' 
	assert all( [a in data.keys() for a in ['owner','image','eyes']] ), f"return value should include the keys 'owner','image' and 'eyes'"
	return data

print(get_ape_info(7893))
"""Test
print("Ape # 1", get_ape_info(1))
print("-----")
for i in range(100, 110):
	print("Ape #",i,get_ape_info(i))
"""