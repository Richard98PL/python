import json
import requests
import time
import os
import openpyxl

rows = []
SCENARIO = 1
API = 'REST'

TABLE_NAME = 'Table_10000__c'
query = "SELECT Boolean__c, Currency__c, Date__c, Date_Time__c, Id, Index__c, Multi_Pick_List__c, Number__c, Picklist__c FROM " + TABLE_NAME + " ORDER By Name ASC"


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
    headers = {'Authorization': 'Bearer ' + access_token, 'Sforce-Query-Options' : 'batchSize=200'}
    # ...
else:
    print('Authentication failed with status code', response.status_code)
    exit()

# Define Salesforce query endpoint and initial query
query_url = instance + "/services/data/v55.0/queryAll"

# Set the maximum number of records to retrieve per batch
batch_size = 200

# Set the initial offset
offset = 0
iteration = 0
while iteration < 20:
    iteration = iteration + 1
    # Set the limit parameter for the query
    limit = batch_size if offset + batch_size <= 4000 else 4000 - offset

    # Set the query parameters
    params = {
        "q": query,
    }

    start_time = time.perf_counter()
    
    response = requests.get(query_url, params=params, headers=headers)

    end_time = time.perf_counter()

    query_url = instance + response.json()['nextRecordsUrl']

    elapsed_time = end_time - start_time
    print(str(iteration) + ": " + f"Elapsed time: {elapsed_time:.6f} seconds")
    rows.append([SCENARIO, API,  f"{elapsed_time:.6f}"])

    # Check the status code of the response
    if response.status_code == 200:
        offset += batch_size
    else:
        # Print the error message
        print("Error: {}".format(response.json()))
        exit()

file_path = os.path.abspath("./Results/results.xlsx")
workbook = openpyxl.load_workbook(file_path)
print(file_path)

# Select the active worksheet
worksheet = workbook.active

print(rows)
for row in rows:
    worksheet.append(row)

# Save the workbook
workbook.save(file_path)