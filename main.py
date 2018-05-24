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


def download_images(keyword, images_to_download=None):
    """Uses <keyword> parameter as search keyword in Google Images,
    then downloads all (up to 100) image results.
    """
    if not keyword:
        raise RuntimeError('You provided an empty search keyword!')
    if images_to_download is not None and images_to_download <= 0:
        raise RuntimeError('You opted to download less than 1 image(s)')

    q = '+'.join(keyword.split())
    url = 'https://www.google.co.in/search?q={}&source=lnms&tbm=isch&tbs=ift:jpg'.format(q)
    google_images_request = requests.get(url, headers=REQUEST_HEADER)
    if google_images_request.status_code == 200 and google_images_request.text:
        folder_name = create_folder(keyword)
        # Google stores image source link within a key, "ou"
        # Ignore first result: bad link
        image_sources = google_images_request.text.split('"ou":"')[1:]
        if not images_to_download:
            images_to_download = len(image_sources)

        for i, image_src in enumerate(image_sources):
            if (i + 1) > images_to_download:
                break

            image_url = image_src[:image_src.find('"')]
            file_name = '{}.jpg'.format(i)

            successful_download = False
            try:
                image_request = requests.get(image_url, headers=REQUEST_HEADER)
                successful_download = True
            except requests.exceptions.RequestException as e:  # Retry request
                pass

            if successful_download:
                with open(os.path.join(folder_name, file_name), 'wb') as img:
                    img.write(image_request.content)
                print('Downloaded {} / {} images'.format(i+1, images_to_download))
            else:
                print('Failed downloading image #{} (Connection Refused)'.format(i+1))


def main():
    if len(sys.argv) < 2:
        raise RuntimeError('Please provide a search keyword, i.e.: '
                           'python3 main.py "cake"')
    else:
        search_keyword = sys.argv[1]

    images_to_download = None
    try:
        images_to_download = int(sys.argv[2])
        download_images(search_keyword, images_to_download)
    except IndexError as ie:  # No number of images to download provided
        download_images(search_keyword)
    except ValueError as ve:  # Provided argument was not a number
        print('Please provide a valid number of images to download, i.e.: '
              'python3 main.py "cake" 5')


if __name__ == "__main__":
    main()