# Relayer Registry

This repo contains a `information.json` and `chain1-chain2.json` for a number of cosmos-sdk based chains. 

Schema files containing the recommended metadata structure can be found in the `*.schema.json` files located in the root directory. Schemas are still undergoing revision as user needs are surfaced. Optional fields may be added beyond what is contained in the schema files.

Once schemas have matured and client needs are better understood Relayer Registry data is intended to migrate to an on-chain representation hosted on the IRIS Hub, i.e. the IOBScan IBC Relayer Name Service. If you are interested in this effort please join the discussion [here](https://discord.com/invite/bmhu9F9xbX)!

## Website
- https://ibc.iobscan.io

## Contributing

We accept pull requests to add data to an existing information.json or chain1-chain2.json or to add a new relayer.

# information.json

The 'information.json' JSON Schema can be found [here](/information.schema.json).

An example 'information.json' contains the following structure:

```json
{
  "team name": "IRISnet Foundation",
  "contact": {
    "website" : "https://irisnet.org/",
    "github": "https://github.com/irisnet",
    "telegram": "https://t.me/irisnetwork",
    "twitter": "https://twitter.com/irisnetwork",
    "medium": "https://medium.com/irisnet-blog",
    "discord": "https://discord.com/invite/bmhu9F9xbX"
  },
  "introduction": {
    "IRISnet (a.k.a IRIS Hub) is designed to be the foundation for the next generation distributed applications. Built with Cosmos-SDK, IRIS Hub enables cross-chain interoperability through a unified service model, while providing a variety of modules to support DeFi applications.",
    "IRISnet dev teams include Bianjie (https://www.bianjie.ai/), a national award-winning blockchain technology team based in Shanghai, and Tendermint (https://tendermint.com/), the world-famous team that created the Tendermint consensus engine and the Cosmos project."
  }
}
```

# chain1-chain2.json

The 'chain1-chain2.json' JSON Schema can be found [here](/chain1-chain2.schema.json).

Note: when creating these files, please ensure the the chains in both the file name and the references of `chain1` and `chain2` in the json file are in alphabetical order. Ex: `Achain-Zchain.json`. The chain names used must match name of the chain's directory here in the chain-registry.

An example 'chain1-chain2.json' contains the following structure:

```
{
  "chain-1": {
    "address" : "iaa148zzqgulnly3wgx35s5f0z4l4vwf30tj03wgaq",
    "chain-id": "irishub-1",
    "channel-id": "channel-0",
    "version": "ics20-1"
  },
  "chain-2": {
    "address" : "cosmos15md2qvgma8lnvqv67w0umu2paqkqkhege2evgl",
    "chain-id": "cosmoshub-4",
    "channel-id": "channel-91",
    "version": "ics20-1"
  }
}
```
