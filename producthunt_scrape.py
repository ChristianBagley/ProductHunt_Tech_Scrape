import logging
import pandas as pd
import requests
import secrets

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%H:%M:%S', )

logger = logging.getLogger(__name__)

token = secrets.api_key


def parse(page):
    for item in page:
        result = dict()
        for k in ('tagline', 'name', 'redirect_url', 'day', 'votes_count'):
            result[k] = item[k]
        yield result


with requests.Session() as s:
    s.headers['Authorization'] = token
    s.headers['Content-Type'] = 'application/json'
    s.headers['Accept'] = 'application/json'
    s.headers['Host'] = 'api.producthunt.com'

    data = []

    url = 'https://api.producthunt.com/v1/categories/tech/posts'
    logger.info("Fetching today's posts from Tech topic.")
    page = s.get(url).json().get('posts')
    images = s.get(url).json().get('thumbnail')
    top = s.get(url).json().get("topics")
    for item in parse(page):
        data.append(item)
    data = pd.DataFrame(data)
    data.to_csv('product_hunt.csv', index=False)
