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
usage: hermes_parser.py [-h] [--config CONFIG] --team_name TEAM_NAME [--path PATH] [--team_logo TEAM_LOGO] [--team_website TEAM_WEBSITE] [--team_github TEAM_GITHUB] [--team_twitter TEAM_TWITTER] [--team_discord TEAM_DISCORD]
                        [--team_medium TEAM_MEDIUM] [--team_description TEAM_DESCRIPTION]

Read Hermes configuration and generate relayer registry entries

  --team_name TEAM_NAME
                        team name
  
optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       path the the hermes configuration file
  --path PATH           path to store output files
  --team_logo TEAM_LOGO
                        team logo
  --team_website TEAM_WEBSITE
                        team website
  --team_github TEAM_GITHUB
                        team github
  --team_twitter TEAM_TWITTER
                        team twitter
  --team_discord TEAM_DISCORD
                        team discord
  --team_medium TEAM_MEDIUM
                        team medium
  --team_description TEAM_DESCRIPTION
                        team description

```

If called with `--team_xxx` argument, the field will be updated in the description.
Each call of the script will append the config to the existing one without existance check.