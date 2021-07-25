import json
import requests
import os

UNSPLASH_BASE_URL = "api.unsplash.com"
API_ACCESS_KEY = os.environ.get('UNSPLASH_API_ACCESS_KEY')
SAVE_IMAGE_LOCATION = './images/'
RESULTS_PER_PAGE = 30
IMAGES_TO_DOWNLOAD = 300


def do_search_images(search_term, page, per_page):
    query_params = {'query': search_term, 'page': page, 'per_page': per_page}
    headers = {'Accept-Version': 'v1', 'Authorization': 'Client-ID ' + API_ACCESS_KEY}
    response = requests.get("https://" + UNSPLASH_BASE_URL + "/search/photos", params=query_params, headers=headers)
    return response


def extract_urls(json_results):
    return [result['urls']['regular'] for result in json_results]


def save_images(urls):
    count = 0
    for url in urls:
        count = count + 1
        image = requests.get(url)
        print("Saving image " + str(count))
        with open(SAVE_IMAGE_LOCATION + "image-" + str(count) + ".jpg", 'wb') as f:
            f.write(image.content)


def search_images(search_term):
    urls = []
    pages_to_get = int(IMAGES_TO_DOWNLOAD / RESULTS_PER_PAGE)
    for page in range(1, pages_to_get + 1):
        print("Retrieving page " + str(page))
        search_response = do_search_images(search_term, page, RESULTS_PER_PAGE)
        json_response = json.loads(search_response.text)
        total_pages = json_response['total_pages']
        urls.extend(extract_urls(json_response['results']))
        if page + 2 >= total_pages:
            print("WARN: not enough pages! please change number of images to download for search term: " + search_term)
            break
    return urls


if __name__ == '__main__':
    images_urls = search_images('people covid face mask')
    save_images(images_urls)
