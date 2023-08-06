import logging
import time

import psycopg2
import requests
from fake_useragent import UserAgent
from psycopg2 import Error
from rocketry import Rocketry

from app.core.config import settings

rocketry_app = Rocketry(config={"task_execution": "thread"})
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


@rocketry_app.task('every 5 minute')
def parse_prices():
    logger.info(f'------Initialize module------')
    logger.info(f'Connect to DB')
    connection = psycopg2.connect(user=settings.DB_USER,
                                  password=settings.DB_PASSWORD,
                                  host=settings.DB_HOST,
                                  port=settings.DB_PORT,
                                  database=settings.DB_NAME)
    curr = connection.cursor()

    page, total_pages = 1, 100
    ua = UserAgent()
    headers = {
        'authority': 'web-gateway.middle-api.magnit.ru',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'origin': 'https://magnit.ru',
        'referer': 'https://magnit.ru/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': ua.random,
        'x-app-version': '0.1.0',
        'x-client-name': 'magnit',
        'x-device-id': 'x2h29qw60g',
        'x-device-platform': 'Web',
        'x-device-tag': 'disabled',
        'x-platform-version': 'window.navigator.userAgent',
    }
    logger.info(f'Start parsing')
    while page < total_pages:
        payload = {
            'categoryIDs': [],
            'includeForAdults': True,
            'onlyDiscount': False,
            'order': 'desc',
            'pagination': {
                'number': page,
                'size': 50
            },
            'shopType': '1',
            'sortBy': 'price',
            'storeCodes': [
                '668472'
            ]
        }
        r = requests.post(settings.ITEMS_URL, headers=headers, json=payload)
        total_pages = r.json()['pagination']['totalPages']
        items = r.json()['goods']
        for j in items:
            id_ = int(j['id'])
            image_url = j['image']['prefixUrl'] + j['image']['defaultSize'] + j['image']['postfixUrl']
            name = j['name']
            price = float(str(j['offers'][0]['price']).replace(',', '.'))
            curr.execute(settings.SELECT_SQL, (id_,))
            res = curr.fetchall()
            if res:
                try:
                    curr.execute(settings.UPDATE_SQL, (image_url, name, price, id_,))
                    connection.commit()
                except (Exception, Error) as err:
                    logger.error(f'Postgres error: {err}', exc_info=True)
            else:
                try:
                    curr.execute(settings.INSERT_SQL, (id_, image_url, name, price,))
                    connection.commit()
                except (Exception, Error) as err:
                    logger.error(f'Postgres error: {err}', exc_info=True)
        time.sleep(0.5)
        page += 1

    if connection:
        curr.close()
        connection.close()
        logger.info('Closed DB connections')
    logger.info(f'Parsing finished')


if __name__ == "__main__":
    rocketry_app.run()
