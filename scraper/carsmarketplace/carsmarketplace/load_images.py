import json
import requests
import os
import time

# # Opening JSON file
# f = open('outputs.json')
  
# f = json.loads(f.read())

# for img in f["urls"]:
# 	print(img[0], img[1])
# 	if not os.path.exists("./outputs/"  + img[1]):
# 		print("downloading...")
# 		time.sleep(2)
# 		r = requests.get(img[0], allow_redirects=False)
# 		open("./outputs/"  + img[1], 'wb').write(r.content)
# 		print("downloaded!")
# 		print()





def delete_none_annoted_images():

	files = os.listdir('outputs/')

	print(files)

	for file in files:
		print(file)
		if '.jpg' in str(file): 	
			file_name = file.replace('.jpg', '')
		elif '.png'in str(file): 	
			file_name = file.replace('.png', '')
		elif '.jpeg'in str(file):
			file_name = file.replace('.jpeg', '')

			if str(file_name + '.txt') in files:
				print("OK")
			else:
				os.remove("outputs/" + file)



delete_none_annoted_images()