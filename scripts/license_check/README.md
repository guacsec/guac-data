# license_check

A script to search your [GUAC](https://guac.sh) data for projects that have a mismatch between declared and detected licenses.

## Requirements

* Python modules
    * csv
    * gql
    * sys

## Usage

After installing any missing requirements, run `python3 ./license_check.py`

The script assumes your query is in `./query.gql` and that your GraphQL query endpoint is `http://localhost:8080/query`.

The table below describes setting you may want to change.
All the settings described appear near the top of the script.

| Setting | Description
| ------- | -----------
| GRAPHQL_SERVER | The full URL to your GUAC GraphQL server's query endpoint

The script will print packages or sources with mismatched licenses along with the declared license and the discovered license.

To write a CSV file instead, provide the file name as an argument.
For example: `python3 ./license_check.py license_mismatch.csv`
This results in a CSV file with three columns: package/source, declared license, discovered license.
