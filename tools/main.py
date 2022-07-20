# This script parse Hermes configuration to extract registry informations
import json
from ctypes import Union
from types import SimpleNamespace

import certifi
import cosmpy.protos.ibc.core.channel.v1.query_pb2_grpc
import cosmpy.protos.ibc.core.connection.v1.query_pb2_grpc
import cosmpy.protos.ibc.core.client.v1.query_pb2_grpc
import grpc
import requests

import toml
import urllib3.util

# chain definition schema
# {
#   "chain-1": {
#     "address" : {"type": "string"},
#     "chain-id": {"type": "string"},
#     "channel-id": {"type": "string"},
#     "version": {"type": "string"}
#   },
#   "chain-2": {
#     "address" : {"type": "string"},
#     "chain-id": {"type": "string"},
#     "channel-id": {"type": "string"},
#     "version": {"type": "string"}
#   }
# }
from cosmpy.protos.ibc.core.channel.v1.channel_pb2 import Channel
from cosmpy.protos.ibc.core.channel.v1.query_pb2 import QueryChannelRequest
from cosmpy.protos.ibc.core.connection.v1.connection_pb2 import ConnectionEnd
from cosmpy.protos.ibc.core.connection.v1.query_pb2 import QueryConnectionRequest
from cosmpy.protos.ibc.core.client.v1.query_pb2 import QueryClientStateRequest
from google.protobuf.json_format import MessageToJson

class ChainChain:
    def __init__(self, chain1_name, chain2_name):
        self.chain1_name = chain1_name
        self.chain2_name = chain2_name
        
    def populate_chain_1(self, chain_id, channel, wallet, version='ics20-1'):
        self.chain1 = {
                          "address" : wallet,
                          "chain-id": chain_id,
                          "channel-id": channel,
                          "version": "ics20-1"
                      }
    
    def populate_chain_2(self, chain_id, channel, wallet, version='ics20-1'):
        self.chain2 = {
                          "address": wallet,
                          "chain-id": chain_id,
                          "channel-id": channel,
                          "version": "ics20-1"
                      }
    def to_string(self):
        json.dumps({
            "chain-1": self.chain1,
            "chain-2": self.chain2
        })

class GrpcIBC:
    def __init__(self, url:str):
        self.grpc_url = urllib3.util.parse_url(url)
        self.grpc_client = None
        if 'https' in urllib3.util.get_host(str(grpc_url))[0]:
            with open(certifi.where(), "rb") as f:
                trusted_certs = f.read()
            credentials = grpc.ssl_channel_credentials(
                root_certificates=trusted_certs
            )
            self.grpc_client = grpc.secure_channel(str(grpc_url), credentials)
        else:
            self.grpc_client = grpc.insecure_channel(str(grpc_url))

        self.ibc_channel_query = cosmpy.protos.ibc.core.channel.v1.query_pb2_grpc.QueryStub(self.grpc_client)
        self.ibc_connection_query = cosmpy.protos.ibc.core.connection.v1.query_pb2_grpc.QueryStub(self.grpc_client)
        self.ibc_client_query = cosmpy.protos.ibc.core.client.v1.query_pb2_grpc.QueryStub(self.grpc_client)
        
    def query_channel(self, port, channel)->Channel:
        resp = self.ibc_channel_query.Channel(QueryChannelRequest(port_id=port, channel_id=channel))
        return resp.channel

    def query_connection(self, connection)->ConnectionEnd:
        resp = self.ibc_connection_query.Connection(QueryConnectionRequest(connection_id=connection))
        return resp
    
    def query_client(self, client) -> dict:
        from cosmpy.protos.ibc.lightclients.tendermint.v1.tendermint_pb2 import ClientState
        
        resp = self.ibc_client_query.ClientState(QueryClientStateRequest(client_id=client))
        # client_state is not parsed in the answer
        try:
            string_json = MessageToJson(resp.client_state)
        except TypeError as err:
            print(err)
        # Parse JSON into an object with attributes corresponding to dict keys.
        mess = json.loads(string_json, object_hook=lambda d: SimpleNamespace(**d))
        return mess

class Registry:
    chain_registry = []
    
    def __init__(self):
        self.chain_registry = self.get_chains()
    
    def get_chains(self) -> dict:
        chains = requests.get("https://chains.cosmos.directory/").json()['chains']
        return chains
    
    def get_chain(self, chain) -> dict:
        if isinstance(chain, dict):
            chain_name = next(item for item in self.chain_registry if item["chain_id"] == chain['id'])['name']
        else:
            chain_name = next(item for item in self.chain_registry if item["chain_id"] == chain)['name']
        chain_def_full = requests.get("https://chains.cosmos.directory/{}".format(chain_name)).json()['chain']
        return chain_def_full

def get_wallet_from_keyring(chain_id, key_name):
    return json.loads(f".hermes/keys/{chain_id}/keyring-test/{key_name}.json")['account']

def get_counterparty_chain(ibc, port, channel):
    try:
        channel_resp = ibc.query_channel(port, channel)
    except grpc.RpcError as err:
        print("chain config {} not parsed, due to bad GRPC endpoint.".format(chain['id']))
        raise err
    counterparty_port = channel_resp.counterparty.port_id
    counterparty_channel = channel_resp.counterparty.channel_id
    connection = channel_resp.connection_hops[-1:][0]
    
    resp = ibc.query_connection(connection)
    client_id = resp.connection.client_id

    client = ibc.query_client(client_id)
    counterparty_chain_id = client.chainId
    return counterparty_chain_id, counterparty_port, counterparty_channel

if __name__ == '__main__':
    registry = Registry()
    
    config = toml.load(open("/home/dpierret/cros-nest/hermes_relayer1.toml", 'r'))
    for chain in config['chains']:
        if 'packet_filter' not in chain:
            print("chain config {} not parsed, please use packet_filter.".format(chain['id']))
        if chain['packet_filter']['policy'] != 'allow':
            print("chain config {} not parsed, please use \'allow\' packet_filter\'s policy.".format(chain['id']))
        
        chain_extended_definition = registry.get_chain(chain)
        chain_name = chain_extended_definition['name']
        chain_id = chain['id']
        port = ""
        channel = ""

        counterparty_chain_id = ""
        counterparty_port = ""
        counterparty_channel = ""
        
        grpc_url = urllib3.util.parse_url(chain_extended_definition['apis']['grpc'][0]['address'])
        # grpc_url = urllib3.util.parse_url(chain['grpc_addr'])
        ibc = GrpcIBC(chain_extended_definition['apis']['grpc'][0]['address'])
        
        channel_list = chain['packet_filter']['list']
        for port, channel in channel_list:
            try:
                counterparty_chain_id, counterparty_port, counterparty_channel = get_counterparty_chain(ibc, port, channel)
                counterparty_chain_definition = registry.get_chain(counterparty_chain_id)
                wallet = get_wallet_from_keyring(chain_id, chain['key_name'])
                wallet_counterparty = get_wallet_from_keyring(counterparty_chain_id,
                                                              next(item for item in channel_list if item["id"] == counterparty_chain_id)['key_name'])
                cc = ChainChain(chain_name, counterparty_chain_definition['name'])
                cc.populate_chain_1(chain_id, channel, wallet)
                cc.populate_chain_2(counterparty_chain_id, counterparty_channel, wallet_counterparty)
                print(cc.to_string())
                print("ok?")
            except Exception as err:
                pass
