from django.core.management.base import BaseCommand
from analytics.models import Product
import requests


class Command(BaseCommand):
    help = 'Загружает товары Wildberries по ссылке на категорию (--url)'

    def add_arguments(self, parser):
        parser.add_argument('--url', type=str, help='Ссылка на категорию WB (без фильтров)')
        parser.add_argument('--pages', type=int, default=1, help='Количество страниц (по умолчанию 1)')
        parser.add_argument('--limit', type=int, default=100, help='Максимум товаров')

    def handle(self, *args, **opts):
        url = opts.get('url')
        pages = opts.get('pages')
        limit = opts.get('limit')

        if not url:
            self.stdout.write("❗ Укажи ссылку на категорию через --url")
            return

        headers = {'User-Agent': 'Mozilla/5.0'}
        menu_url = 'https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v3.json'
        menu = requests.get(menu_url, headers=headers).json()

        catalog_list = []

        def extract(node):
            if isinstance(node, list):
                for item in node:
                    extract(item)
            elif isinstance(node, dict):
                if 'url' in node:
                    catalog_list.append({
                        'name': node['name'],
                        'url': node['url'],
                        'shard': node.get('shard'),
                        'query': node.get('query')
                    })
                if 'childs' in node:
                    extract(node['childs'])

        extract(menu)

        category = next((c for c in catalog_list if url.endswith(c['url'])), None)
        if not category or not category.get('shard'):
            self.stdout.write("Не удалось определить категорию по ссылке")
            return

        self.stdout.write(f"Найдена категория: {category['name']} (shard={category['shard']})")

        page = 1
        total_added = 0

        while page <= pages and total_added < limit:
            params = {
                "appType": 1,
                "curr": "rub",
                "dest": -1257786,
                "page": page,
                "sort": "popular",
                "spp": 0
            }
            if category.get("query"):
                for item in category["query"].split("&"):
                    if "=" in item:
                        k, v = item.split("=")
                        params[k] = v

            catalog_api = f"https://catalog.wb.ru/catalog/{category['shard']}/catalog"
            resp = requests.get(catalog_api, params=params, headers=headers)

            if resp.status_code != 200:
                self.stdout.write(f"Ошибка страницы {page}: {resp.status_code}")
                break

            products = resp.json().get("data", {}).get("products", [])
            if not products:
                self.stdout.write(f"Страница {page}: нет товаров.")
                break

            for p in products:
                try:
                    nm_id = p.get("id")
                    name = p.get("name")
                    price = int(p.get("priceU", 0)) / 100
                    discount = int(p.get("salePriceU", 0)) / 100
                    rating = p.get("reviewRating", 0)
                    reviews = p.get("feedbacks", 0)
                    link = f"https://www.wildberries.ru/catalog/{nm_id}/detail.aspx"

                    Product.objects.create(
                        name=name,
                        price=price,
                        discounted_price=discount,
                        rating=rating,
                        review_count=reviews,
                        link=link
                    )

                    self.stdout.write(self.style.SUCCESS(
                        f"✓ {name} | {price:.2f} → {discount:.2f} | ★ {rating} | отзывов: {reviews}\n  🔗 {link}"
                    ))
                    total_added += 1
                    if total_added >= limit:
                        break

                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Ошибка сохранения \"{p.get('name')}\": {e}"))

            page += 1

        self.stdout.write(self.style.SUCCESS(f"\nЗагрузка завершена: сохранено {total_added} товаров"))