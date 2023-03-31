# Azure Forwarder

Azure Function App that forwards data from Azure to Elsticsearch.

```text
┌───────────────┐               ┌───────────────┐           ┌─────────────────────────────────┐
│    testing    │               │   forwarder   │           │ logs-azure.activitylogs-default │
│ <<event hub>> │───triggers───▶│ <<function>>  │───ship───▶│         <<data stream>>         │
└───────────────┘               └───────────────┘           └─────────────────────────────────┘
```

The current version supports Azure Event Hub only.

## Installation

Clone the repository:

```shell
git clone git@github.com:zmoog/forwarder.git
```

Create and activate a virtual env:

```shell
python -m venv venv

source venv/bin/activate
```

Install the required dependencies:

```shell
pip install -r requirements.txt 
```

## Usage

To run the forwarder locally, run:

```shell
$ func start
Found Python version 3.8.10 (python3).

Azure Functions Core Tools
Core Tools Version:       4.0.4895 Commit hash: N/A  (64-bit)
Function Runtime Version: 4.13.0.19486


Functions:

        process_eventhub: eventHubTrigger

For detailed output, run func with --verbose flag.
[2023-03-30T12:10:03.445Z] Worker process started and initialized.
[2023-03-30T12:10:07.904Z] Host lock lease acquired by instance ID '000000000000000000000000000C2005'.
```

## Requirements

```shell
brew install azure/functions/azure-functions-core-tools@4
```

## Development

Install the dev dependencies for testing and lintin:

```shell
pip install -r requirements-dev.txt
```

During development, you may need one or more of the following:

```shell
# run tests
make test

# check formatting, linting, and type checking
make lint

# fix linting
make fix-lint

# check that everying is okay before commit
make ready
```
