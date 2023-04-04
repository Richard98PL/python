import json
import requests
import time
import os
import openpyxl

def graphQLScenario(SCENARIO, DATA_SIZE, graphql_query):
  rows = []
  API = 'GraphQL'


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

  # Set the Salesforce instance URL
  instance_url = instance + "/services/data/v57.0/graphql"

  # Set the GraphQL query
  TABLE_NAME = 'Table_' + str(DATA_SIZE) + '__c'
  graphql_query = graphql_query.replace("table", TABLE_NAME)

  # Set the authentication headers
  headers = {
      "Authorization": "Bearer {}".format(access_token),
      "Content-Type": "application/json"
  }



  cursor = None
  hasNextPage = True
  iteration = 0
  while hasNextPage and iteration < 20:
      # Make the API request
      iteration = iteration + 1
      variables = {'cursor': cursor} if cursor else {}
      json_variable = { 'query': graphql_query, 'variables': variables}
      
      start_time = time.perf_counter()

      response = requests.post(instance_url, headers=headers,json=json_variable)

      end_time = time.perf_counter()

      elapsed_time = end_time - start_time
      print(str(iteration) + ": " + f"Elapsed time: {elapsed_time:.6f} seconds")

      rows.append([SCENARIO, API, DATA_SIZE, f"{elapsed_time:.6f}"])

      if response.status_code == 200:
              
          data = response.json()['data']['uiapi']['query'][TABLE_NAME]

          totalCount = data['totalCount']
          pageInfo = data['pageInfo']
          cursor = data['pageInfo']['endCursor']
          hasNextPage = pageInfo['hasNextPage']
          

      else:
          break

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