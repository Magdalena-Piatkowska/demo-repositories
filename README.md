# demo-azurite

A sample project put together to explain the Ports and Adapters pattern

### Requirements

##### Storage:

- Azurite service running with Blob port exposed https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azurite?tabs=docker-hub%2Cblob-storage
- Microsoft Azure Storage Explorer https://azure.microsoft.com/en-gb/products/storage/storage-explorer
- Blob Container with the name `demo-repositories`

##### SQL DB:

- Postgresql Server running with default configuration
- Postgresql DB with the name `demo-repositories`

### Setup

- Create a virtual environment
- From root directory of the project, run: `pip install requirements.txt`

### How to run the API

- From root directory of the project, run: `uvicorn app.adapter.fastapi.main:app --reload`
