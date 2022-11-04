# Relayer Registry

This repo contains an `relayer_info.json` for a number of cosmos-sdk based chains. 

Schema files containing the recommended metadata structure can be found in the `*.schema.json` files located in the root directory. Schemas are still undergoing revision as user needs are surfaced. Optional fields may be added beyond what is contained in the schema files.

Once schemas have matured and client needs are better understood Relayer Registry data is intended to migrate to an on-chain representation hosted on the IRIS Hub, i.e. the IOBScan IBC Relayer Name Service. If you are interested in this effort please join the discussion [here](https://discord.com/invite/bmhu9F9xbX)!

## Website
- https://ibc.iobscan.io

## Contributing

We accept pull requests to add data to an existing relayer_info.json to add a new relayer.

# relayer_info.json

The `relayer_info.json` JSON Schema can be found [here](/relayers/relayer.schema.json).

An example `relayer_info.json` contains the following structure:

```json
{
    "team_name": "IRISnet Foundation",
    "team_logo":"",
    "contact": {
      "website" : "https://irisnet.org/",
      "github": "https://github.com/irisnet",
      "telegram": "https://t.me/irisnetwork",
      "twitter": "https://twitter.com/irisnetwork",
      "medium": "https://medium.com/irisnet-blog",
      "discord": "https://discord.com/invite/bmhu9F9xbX"
    },
    "introduction": [
      "IRISnet (a.k.a IRIS Hub) is designed to be the foundation for the next generation distributed applications. Built with Cosmos-SDK, IRIS Hub enables cross-chain interoperability through a unified service model, while providing a variety of modules to support DeFi applications.",
      "IRISnet dev teams include Bianjie (https://www.bianjie.ai/), a national award-winning blockchain technology team based in Shanghai, and Tendermint (https://tendermint.com/), the world-famous team that created the Tendermint consensus engine and the Cosmos project."
    ],
    "addresses": [
        {
            "irishub-1": "iaa1cf8ufk9mqtj48zj9l4pupyfeqjwh7fjms67e50",
            "osmosis-1": "osmo1cf8ufk9mqtj48zj9l4pupyfeqjwh7fjmdrdcqv"
        },
        {
            "irishub-1": "iaa1cf8ufk9mqtj48zj9l4pupyfeqjwh7fjms67e50",
            "cosmoshub-4": "cosmos1cf8ufk9mqtj48zj9l4pupyfeqjwh7fjm9c7gk7"
        },
        {
            "irishub-1": "iaa1cf8ufk9mqtj48zj9l4pupyfeqjwh7fjms67e50",
            "gravity-bridge-3": "gravity1cf8ufk9mqtj48zj9l4pupyfeqjwh7fjmpgvsnk"
        }
    ]
  }
```

