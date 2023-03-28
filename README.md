# Azure Forwarder

Azure Function App that forwards data from Azure to Elsticsearch.

```text
┌───────────────┐               ┌───────────────┐           ┌─────────────────────────────────┐
│    testing    │               │   forwader    │           │ logs-azure.activitylogs-default │
│ <<event hub>> │───triggers───▶│ <<function>>  │───ship───▶│         <<data stream>>         │
└───────────────┘               └───────────────┘           └─────────────────────────────────┘
```

## Requirements

```shell
brew install azure/functions/azure-functions-core-tools@4
```
