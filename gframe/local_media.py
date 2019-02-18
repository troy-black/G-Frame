import os
import random


class Media:
	def list_media(self, path, media_list):
		for entry in os.listdir(path):
			filename = os.path.join(path, entry)
			if os.path.isdir(filename):
				return self.list_media(filename, media_list)
			media_list[filename] = os.path.getmtime(filename)
		return list(media_list.keys())

	def random_media(self, path):
		return random.choice(self.list_media(path, {}))
