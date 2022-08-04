# Hermes configuration parser

This tools allow any Informal's Hermes relayer user to parse the configuration file and generate the IOB registry json files.

The script use GRPC requests to query chains and channels connection.
It use the GRPC endpoints specified in the Hermes configuration file.

An internet access is needed to query cosmos.directory API needed to recover chains information.

## installation

```bash
# create virtual environment
$ sudo apt install python3-virtualenv
$ python3 -m virtualenv ./venv
$ source ./venv/bin/activate
# install dependencies
$ pip3 install -r ./requirements.txt 
# run the script
$ PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python python3 ./hermes_parser.py
```

Usage of the environment vairable `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python` is prefered to not have full protobuff rebuild to do.

### options
```bash
usage: hermes_parser.py [-h] [--config CONFIG] [--relayer_id RELAYER_ID] [--path PATH]

Read Hermes configuration and generate relayer registry entries

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       path the the hermes configuration file
  --relayer_id RELAYER_ID
                        in case of multiple relayer, help identify
  --path PATH           path to store output files

```

