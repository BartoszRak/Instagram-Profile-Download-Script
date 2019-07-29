import pprint
import requests
import json
import os
import time
import urllib.request
from instagram.client import InstagramAPI

# utils

def getIdFromProfileHtml(response):
  lookFor = 'profilePage_'
  profileText = response.text
  indexOfId = profileText.find(lookFor)
  textStartedWithId = profileText[indexOfId + len(lookFor):]
  return textStartedWithId[:textStartedWithId.find('"')]

def checkResultDirectories():
  path = os.getcwd()
  resultPath = f"{path}\\results"
  profileResultPath = f"{resultPath}\\{profileName}"
  newScrappingPath = f"{profileResultPath}\\{getTime}"

  if not os.path.exists(resultPath):
    os.mkdir(resultPath)

  if not os.path.exists(profileResultPath):
    os.mkdir(profileResultPath)

  if not os.path.exists(newScrappingPath):
    os.mkdir(newScrappingPath)

  return newScrappingPath

def getGraphqlQueryParams(cursor = ''):
  graphqlVariables = {
    'id': id,
    'first': 20,
    'after': cursor,
  }
  graphqlVariablesJson = json.dumps(graphqlVariables)
  graphqlQueryHash = 'f2405b236d85e8296cf30347c9f08c2a'

  return {
    'query_hash': graphqlQueryHash,
    'variables': graphqlVariablesJson,
  }

def scrapProfile(endCursor = ''):
  graphqlUrl = f"{instagramBaseUrl}graphql/query/"
  graphqlQueryParams = getGraphqlQueryParams(endCursor)
  picturesQueryResponse = requests.get(graphqlUrl, params=graphqlQueryParams)
  picturesQueryResponseJson = picturesQueryResponse.json()
  user = picturesQueryResponse.json()['data']['user']
  pageInfo = user['edge_owner_to_timeline_media']['page_info']
  posts = user['edge_owner_to_timeline_media']['edges']

  newScrappingPath = checkResultDirectories()

  for index, post in enumerate(posts):
    postNode = post['node']
    urllib.request.urlretrieve(postNode['display_url'], f"{newScrappingPath}\\{postNode['id']}.jpg")

  pp.pprint(f"# {len(posts)} pictures have been saved.")
  
  if pageInfo['has_next_page']:
    scrapProfile(pageInfo['end_cursor'])

# init
pp = pprint.PrettyPrinter(indent=4)

# main
instagramBaseUrl = 'https://www.instagram.com/'
profileName = input('Instagram profile NAME: ')
profileUrl = f"{instagramBaseUrl}{profileName}/"
profileHtmlResponse = requests.get(profileUrl)

id = getIdFromProfileHtml(profileHtmlResponse)
getTime = time.strftime('%Y.%m.%d-%H%M%S')

try:
  scrapProfile()
except:
  pp.pprint('[ERROR] Scrapping failed.')

pp.pprint('[SUCCESS] Scrapping finished.')