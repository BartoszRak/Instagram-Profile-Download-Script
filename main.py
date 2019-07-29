import pprint
import requests
import json
import os
import time
import urllib.request
from instagram.client import InstagramAPI

# init
pp = pprint.PrettyPrinter(indent=4)

# main
instagramBaseUrl = 'https://www.instagram.com/'
profileName = input('Instagram profile NAME: ')
profileUrl = f"{instagramBaseUrl}{profileName}/"

lookFor = 'profilePage_'
scrapProfileResponse = requests.get(profileUrl)
profileText = scrapProfileResponse.text
indexOfId = profileText.find(lookFor)
textStartedWithId = profileText[indexOfId + len(lookFor):]

id = textStartedWithId[:textStartedWithId.find('"')]

graphqlUrl = f"{instagramBaseUrl}graphql/query/"
graphqlVariables = {
  'id': id,
  'first': 100,
  'after': '',
}
graphqlVariablesJson = json.dumps(graphqlVariables)
graphqlQueryHash = 'f2405b236d85e8296cf30347c9f08c2a'

graphqlQueryParams = {
  'query_hash': graphqlQueryHash,
  'variables': graphqlVariablesJson,
}

picturesQueryResponse = requests.get(graphqlUrl, params=graphqlQueryParams)
picturesQueryResponseJson = picturesQueryResponse.json()

user = picturesQueryResponse.json()['data']['user']
posts = user['edge_owner_to_timeline_media']['edges']

path = os.getcwd()
resultPath = f"{path}\\results"
profileResultPath = f"{resultPath}\\{profileName}"
newScrappingPath = f"{profileResultPath}\\{time.strftime('%Y.%m.%d-%H%M%S')}"

if not os.path.exists(resultPath):
  os.mkdir(resultPath)

if not os.path.exists(profileResultPath):
  os.mkdir(profileResultPath)

if not os.path.exists(newScrappingPath):
  os.mkdir(newScrappingPath)

pp.pprint(f"### {len(posts)}")

for index, post in enumerate(posts):
  postNode = post['node']
  pp.pprint(f"{index}. {postNode['display_url']}")
  urllib.request.urlretrieve(postNode['display_url'], f"{newScrappingPath}\\{postNode['id']}.jpg")