import os
import sys

import requests


REQUEST_HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                                'AppleWebKit/537.36(KHTML, like Gecko) '
                                'Chrome/43.0.2357.134 Safari/537.36'}

query = None
try:
    query = sys.argv[1]
except IndexError as e:
    print('Please provide a search keyword, i.e.: python3 main.py "cake"')

if query:
    query = '+'.join(query.split())
    url = 'https://www.google.co.in/search?q={}&source=lnms&tbm=isch'.format(query)
    request = requests.get(url, headers=REQUEST_HEADER)
    if request.status_code == 200 and request.text:
        # Create a directory named after search keyword if it doesn't exist
        try:
            folder_name = ''.join(ch for ch in '-'.join(query.split())
                                  if ch.isalpha() or ch.isdigit() or ch == '-')
            os.makedirs(folder_name)
        except OSError as e:
            pass

        # Download images
        # Google stores image source link within a key, "ou"
        image_sources = request.text.split('"ou":"')[1:]
        for i, image_src in enumerate(image_sources):
            image_url = image_src[:image_src.find('"')]
            file_name = '{}{}'.format(i, image_url[image_url.rfind('.'):])
            image_request = requests.get(image_url, headers=REQUEST_HEADER)
            with open(os.path.join(folder_name, file_name), 'wb') as img:
                img.write(image_request.content)
            print('Downloaded {} / {} image results'.format(i+1, len(image_sources)))
