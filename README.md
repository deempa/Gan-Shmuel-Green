# Gan Shmuel IT Project

## Weight Microservice

- Responsible for weighing trucks and allowing payment to providers.
- Tracks all weights and allows payment to be for net weight.
- API routes:
  - `POST /weight`: Records data and server date-time and returns a JSON object with a unique weight. Supports various parameters.
  - `POST /batch-weight`: Uploads list of tara weights from a file in "/in" folder.
  - `GET /unknown`: Returns a list of all recorded containers that have unknown weight.
  - `GET /weight?from=t1&to=t2&filter=f`: Returns an array of JSON objects, one per weighing (batch NOT included).
  - `GET /item/<id>?from=t1&to=t2`: Returns a JSON object for an item (truck or container).
  - `GET /session/<id>`: Returns a JSON object for a weighing session.
  - `GET /health`: Returns status of the service.

## Billing Microservice

- Calculates pay for fruit providers.
- API routes:
  - `POST /provider`: Creates a new provider record.
  - `PUT /provider/{id}`: Updates provider name.
  - `POST /rates`: Uploads new rates from an Excel file.
  - `GET /rates`: Downloads a copy of the uploaded Excel file.
  - `POST /truck`: Registers a truck in the system.
  - `PUT /truck/{id}`: Updates provider id.
  - `GET /truck/<id>?from=t1&to=t2`: Returns a JSON object for a truck.
  - `GET /bill/<id>?from=t1&to=t2`: Returns a JSON object for a provider bill.
  - `GET /health`: Returns status of the service.

## DevOps CI Service

- Awaits a trigger and activates the CI workflow.
- API routes:
  - `GET /health`: Returns status of the service.
  - `POST /trigger`: Triggers the CI workflow. The request body contains useful JSON data from GitHub.
