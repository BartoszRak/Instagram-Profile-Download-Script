import pprint
import requests
import json
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
  'first': 12,
  'after': '',
}
graphqlVariablesJson = json.dumps(graphqlVariables)
graphqlQueryHash = 'f2405b236d85e8296cf30347c9f08c2a'

graphqlQueryParams = {
  'query_hash': graphqlQueryHash,
  'variables': graphqlVariablesJson,
}

picturesQueryResponse = requests.get(graphqlUrl, params=graphqlQueryParams)

pp.pprint(picturesQueryResponse.json())