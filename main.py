import os
import sys

import requests


REQUEST_HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                                'AppleWebKit/537.36(KHTML, like Gecko) '
                                'Chrome/43.0.2357.134 Safari/537.36'}


def create_folder(keyword):
    """Creates a folder named after the search keyword if it doesn't exist.
    Returns the name of the created/existing folder.
    """
    folder_name = ''.join(ch for ch in '-'.join(keyword.split())
                          if ch.isalpha() or ch.isdigit() or ch == '-')
    try:
        os.makedirs(folder_name)
    except OSError as e:  # folder/directory already exists
        pass

    return folder_name


def download_images(query):
    """Uses <query> parameter as search keyword in Google Images,
    then downloads all (up to 100) image results.
    """
    if not query:
        raise RuntimeError('You provided an empty search keyword!')

    q = '+'.join(query.split())
    url = 'https://www.google.co.in/search?q={}&source=lnms&tbm=isch'.format(q)
    google_images_request = requests.get(url, headers=REQUEST_HEADER)
    if google_images_request.status_code == 200 and google_images_request.text:
        folder_name = create_folder(query)
        # Google stores image source link within a key, "ou"
        # Ignore first result: bad link
        image_sources = google_images_request.text.split('"ou":"')[1:]
        for i, image_src in enumerate(image_sources):
            image_url = image_src[:image_src.find('"')]
            file_name = '{}{}'.format(i, image_url[image_url.rfind('.'):])
            image_request = requests.get(image_url, headers=REQUEST_HEADER)
            with open(os.path.join(folder_name, file_name), 'wb') as img:
                img.write(image_request.content)
            print('Downloaded {} / {} image results'.format(i+1, len(image_sources)))


def main():
    search_keyword = None
    try:
        search_keyword = sys.argv[1]
        download_images(search_keyword.strip())
    except IndexError as e:
        print('Please provide a search keyword, i.e.: python3 main.py "cake"')


if __name__ == "__main__":
    main()