#!/usr/bin/env python3
# Copyright 2019 Brendan Ferracciolo
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

"""Group Meme Bot v2.0
https://github.com/EpicWolverine/GroupMemeBot

--- License ---
Group Meme Bot is licensed under the GNU General Public License V3. A full copy of the license can be found in the LICENSE file in this repository or at http://www.gnu.org/licenses/.
Licence tl;dr: http://www.tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)
"""

import json
import requests
import sys
import time

class GroupMemeBot:
	def __init__(self):
		self.version_number = "2.0"
		self.my_api_key = open(f"{sys.path[0]}/apikey.txt").read()
		self.top_reddit_posts_url = "https://www.reddit.com/r/{}/top.json?sort=top&t=week"
		self.subreddits = open(f"{sys.path[0]}/subreddits.txt").read().split("\n")
		self.group_id = sys.argv[1]
		self.debug = False

	def main(self):
		if self.debug: print(f"Group Meme Bot v{self.version_number}")

		self.format_url()
		reddit_json = requests.get(self.top_reddit_posts_url, headers={'User-Agent': 'Mozilla/5.0'}).json()
		top_meme_post = reddit_json['data']['children'][0]['data']
		top_meme_url = str(top_meme_post['url'])
		if self.debug: print(f"Original URL: {top_meme_url}")

		top_meme_request = requests.get(top_meme_url)

		groupme_image_json = requests.post("https://image.groupme.com/pictures", headers={"X-Access-Token": self.my_api_key}, data=top_meme_request.content).json()
		groupme_image_url = str(groupme_image_json['payload']['url'])
		if self.debug: print(f"GroupMe URL: {groupme_image_url}")

		groupme_group_update = requests.post(f"https://api.groupme.com/v3/groups/{self.group_id}/update", headers={"X-Access-Token": self.my_api_key},
											 json={"image_url": groupme_image_url})
		if self.debug: print(f"Group avatar update status code: {groupme_group_update.status_code}")
		if groupme_group_update.status_code != requests.codes.ok:
			if self.debug: print(groupme_group_update.json())
		
		message = (
			f"[Group Meme Bot] Group avatar changed to:\n"
			f"{top_meme_post['title']}\n"
			f"by {top_meme_post['author']} on /r/{top_meme_post['subreddit']}\n"
			f"https://reddit.com{top_meme_post['permalink']}"
		)
		if self.debug: print(message)
		groupme_send_post = requests.post(f"https://api.groupme.com/v3/groups/{self.group_id}/messages", headers={"X-Access-Token": self.my_api_key},
										  json={"message": {"text": message, "attachments": [{"type": "image", "url": groupme_image_url}], "source_guid": str(time.time_ns())}})
		if self.debug: print(f"Group message post status code: {groupme_send_post.status_code}")
		if groupme_send_post.status_code != requests.codes.ok:
			if self.debug: print(groupme_send_post.json())

	def format_url(self):
		self.subreddits = [sub for sub in self.subreddits if sub[0] != '#']
		multireddit_string = self.subreddits[0]
		for subreddit in self.subreddits[1:]:
				multireddit_string += "+" + subreddit
		self.top_reddit_posts_url = self.top_reddit_posts_url.format(multireddit_string)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
	bot = GroupMemeBot()
	bot.main()
