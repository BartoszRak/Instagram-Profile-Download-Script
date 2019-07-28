import pprint
import requests
import json
from instagram.client import InstagramAPI

# init
pp = pprint.PrettyPrinter(indent=4)

# main
instagramBaseUrl = 'https://www.instagram.com/'
profileName = input('Instagram profile NAME: ')
validUrl = f"{instagramBaseUrl}{profileName}/"

lookFor = 'profilePage_'
response = requests.get(validUrl)
text = response.text
indexOfId = text.find(lookFor)
textStartedWithId = text[indexOfId + len(lookFor):]

id = textStartedWithId[:textStartedWithId.find('"')]
pp.pprint(id)