import json
import requests
import xml.etree.ElementTree as ET
import time
import xmltodict
import os
import openpyxl

def soapAPIScenario(SCENARIO, DATA_SIZE, query_string):
    rows = []
    API = 'SOAP'

    query_string = query_string.replace('X', 'Table_' + str(DATA_SIZE) + '__c')

    # Load credentials from credentials.json
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)

    # Define authentication endpoint
    auth_url = 'https://test.salesforce.com/services/oauth2/token'

    # Define authentication parameters
    params = {
        'grant_type': 'password',
        'client_id': credentials['client_id'],
        'client_secret': credentials['client_secret'],
        'username': credentials['username'],
        'password': credentials['password']
    }

    response = requests.post(auth_url, params=params)
    access_token = ''
    instance = ''
    # Check response status code
    if response.status_code == 200:
        # Extract access token from response
        access_token = response.json()['access_token']
        instance = response.json()['instance_url']
        # Use access token to make API requests
        headers = {'Authorization': 'Bearer ' + access_token}
        # ...
    else:
        print('Authentication failed with status code', response.status_code)
        exit()


    # Define the SOAP endpoint
    soap_endpoint = instance + "/services/Soap/u/55.0"

    # Set the SOAP headers
    headers = {
        'Content-Type': 'text/xml;charset=UTF-8',
        'SOAPAction': '""'
    }

    # Define the SOAP envelope template
    soap_template = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:partner.soap.sforce.com">
        <soapenv:Header>
        <urn:QueryOptions xmlns:h="urn:partner.soap.sforce.com">
                <urn:batchSize>200</urn:batchSize>
            </urn:QueryOptions>
            <urn:SessionHeader>
                <urn:sessionId>{}</urn:sessionId>
            </urn:SessionHeader>
        </soapenv:Header>
        <soapenv:Body>
            <urn:query>
                <urn:queryString>{}</urn:queryString>
            </urn:query>
        </soapenv:Body>
    </soapenv:Envelope>'''

    # Define the query string


    # Define the batch size and total number of records to retrieve
    batch_size = 200
    iteration = 0
    offset = 0

    while iteration < 20:
        iteration = iteration + 1

        # Construct the SOAP envelope
        soap_envelope = ET.fromstring(soap_template.format(access_token, query_string))
        data=ET.tostring(soap_envelope)

        start_time = time.perf_counter()

        response = requests.post(soap_endpoint, headers=headers, data=data)

        end_time = time.perf_counter()

        elapsed_time = end_time - start_time
        print(str(iteration) + ": " + f"Elapsed time: {elapsed_time:.6f} seconds")
        rows.append([SCENARIO, API, DATA_SIZE,  f"{elapsed_time:.6f}"])


        xml_dict = xmltodict.parse(response.content)

        json_str = json.dumps(xml_dict)
        json_str = json.loads(json_str)
        if 'queryResponse' in json_str['soapenv:Envelope']['soapenv:Body']:
            query_locator = json_str['soapenv:Envelope']['soapenv:Body']['queryResponse']['result']['queryLocator']

        elif 'queryMoreResponse' in json_str['soapenv:Envelope']['soapenv:Body'] :
            query_locator = json_str['soapenv:Envelope']['soapenv:Body']['queryMoreResponse']['result']['queryLocator']
            
        else:
            break

        query_string = query_locator

        if str(query_string) == "{'@xsi:nil': 'true'}":
            break

        soap_template = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:partner.soap.sforce.com">
        <soapenv:Header>
        <urn:QueryOptions xmlns:h="urn:partner.soap.sforce.com">
                <urn:batchSize>200</urn:batchSize>
            </urn:QueryOptions>
            <urn:SessionHeader>
                <urn:sessionId>{}</urn:sessionId>
            </urn:SessionHeader>
        </soapenv:Header>
        <soapenv:Body>
            <urn:queryMore>
                <urn:queryLocator>{}</urn:queryLocator>
            </urn:queryMore>
        </soapenv:Body>
    </soapenv:Envelope>'''

        # Check the status code of the response
        if response.status_code == 200:
            offset += batch_size
        else:
            # Print the error message
            print("Error: {}".format(response.content))

    file_path = os.path.abspath("Results/results.xlsx")
    workbook = openpyxl.load_workbook(file_path)
    print(file_path)

    # Select the active worksheet
    worksheet = workbook.active

    print(rows)
    for row in rows:
        worksheet.append(row)

    # Save the workbook
    workbook.save(file_path)