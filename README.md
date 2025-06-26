# product-analysts
Этот проект автоматически парсит карточки товаров с сайта Wildberries по ссылке на категорию и сохраняет данные в базу, 
а также отображает их на веб-странице с фильтрами и графиками.

Возможности:
- Загрузка товаров из категорий Wildberries через catalog.wb.ru;
- Сохранение в модель Product с полями: name, price, discounted_price, rating, review_count, link;
- Фильтрация товаров по цене, рейтингу, количеству отзывов;
- Динамические графики по цене и скидкам (Chart.js);
- Кликабельные ссылки на товары WB в таблице.

Запуск парсинга:
python manage.py parser --url "https://www.wildberries.by/catalog/elektronika/kabeli-i-zaryadnye-ustroystva" --pages 3 --limit 100



