# SPDX-License-Identifier: copyleft-next-0.3.1

import csv
import sys
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

###
#
# Things you might need to change
#
###

# Your GUAC GraphQL server
GRAPHQL_SERVER = "http://localhost:8080/query"

###
#
# Things you probably won't need to change
#
###

def queryGuac():
    '''
    Search the data in GUAC and return anything with CertifyLegal

    Inputs: none
    Outputs: licenseinfo (dict of lists)
    '''
    licenseData = {}
    print("Searching your GUAC data")
    transport = RequestsHTTPTransport(url=GRAPHQL_SERVER)
    gql_client = Client(transport=transport, fetch_schema_from_transport=True)

    with open('query.gql') as query_file:
        gql_query = gql(query_file.read())
        query_file.close()

    guac_data = gql_client.execute(gql_query)

    for legal in guac_data['CertifyLegal']:
        namespace = legal['subject']['namespaces'][0]['namespace']
        if not namespace:
            package = legal['subject']['namespaces'][0]['names'][0]['name']
        else:
            package =  namespace + "/" + legal['subject']['namespaces'][0]['names'][0]['name']

        declaredLicense = legal['declaredLicense']
        discoveredLicense = legal['discoveredLicense']
        if declaredLicense and discoveredLicense:
            licenseData[package] = [ declaredLicense, discoveredLicense]

    return licenseData

def checkLicenses(licenseData):
    '''
    Comments go here
    '''

    if sys.argv[1:]:
        # Oh, you want me to write to a file? Okay!
        outfile = open(sys.argv[1], 'w', newline='')
        csvfile = csv.writer(outfile)
        csvfile.writerow(['Package', 'Declared', 'Discovered'])

    for entry in licenseData:
        declaredLicense = licenseData[entry][0]
        discoveredLicense = licenseData[entry][1]
        if declaredLicense != discoveredLicense:
            if sys.argv[1:]:
                # Write to the file
                csvfile.writerow([entry,declaredLicense, discoveredLicense])
            else:
                # Okay, just print to STDOUT
                print(entry)
                print("\tDeclares: " + licenseData[entry][0])
                print("\tDiscovered: "+ licenseData[entry][1])

licenseData = queryGuac()
checkLicenses(licenseData)