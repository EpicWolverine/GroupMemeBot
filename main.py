#!/usr/bin/python -tt
# Copyright 2017 Brendan Ferracciolo
# 
# This file is part of Group Meme Bot.
#
# Group Meme Bot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Group Meme Bot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Group Meme Bot. If not, see <http://www.gnu.org/licenses/>.

"""Group Meme Bot v1.0
https://github.com/EpicWolverine/GroupMemeBot

--- License ---
Group Meme Bot is licensed under the GNU General Public License V3. A full copy of the license can be found in the LICENSE file in this repository or at http://www.gnu.org/licenses/.
Licence tl;dr: http://www.tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)
"""

import json
import requests
import sys       #for script arguments

versionnumber = "1.0"
myapikey = open(sys.path[0]+"/apikey.txt").read() # retrieve API key from apikey.txt
url = "https://www.reddit.com/r/dankmemes/top.json?sort=top&t=week"
groupid = sys.argv[1]


def main():
	print "Group Meme Bot v" + versionnumber

	redditJson = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).json()
	topMemeUrl = str(redditJson['data']['children'][0]['data']['url'])
	print "Original URL: " + topMemeUrl

	topMemeRequest = requests.get(topMemeUrl)

	groupMeImageJson = requests.post("https://image.groupme.com/pictures",  data=topMemeRequest.content, headers={"X-Access-Token": myapikey}).json()
	groupMeImageUrl = str(groupMeImageJson['payload']['url'])
	print "GroupMe URL: " + groupMeImageUrl

	groupMeGroupUpdate = requests.post("https://api.groupme.com/v3/groups/"+groupid+"/update?token="+myapikey, data=json.dumps({"image_url": groupMeImageUrl}))
	print "Group avater update status code: " + str(groupMeGroupUpdate.status_code)
	if groupMeGroupUpdate.status_code != requests.codes.ok:
		print groupMeGroupUpdate.json()

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
	main()
