# Python testing lab

Навчальний проєкт модульного тестування системи замовлень з **pytest**.

## Мета

Спроєктувати unit-тести для функцій і класів: нормальні, граничні та помилкові сценарії, винятки і зміна стану.

## Структура

```
python-testing-lab/
├── src/                 # production code (не змінювати)
│   ├── validation.py
│   ├── product.py
│   ├── cart.py
│   ├── discount.py
│   └── order.py
├── tests/               # unit-тести
│   ├── test_validation.py
│   ├── test_product.py
│   ├── test_cart.py
│   ├── test_discount.py
│   └── test_order.py
├── requirements.txt
└── README.md
```

## Встановлення і запуск

```bash
cd python-testing-lab
python -m pip install -r requirements.txt
python -m pytest -v
```

Вибірково:

```bash
python -m pytest tests/test_cart.py -v
python -m pytest tests/test_discount.py::test_customer_tier_at_level_boundaries -v
```

## Таблиця вибраних тест-кейсів

| ID | Функція / метод | Вхід | Очікуваний результат | Тип |
|----|-----------------|------|----------------------|-----|
| TC-01 | customer_tier | points=99 | basic | межа |
| TC-02 | customer_tier | points=100 | silver | межа |
| TC-03 | customer_tier | points=500 | gold | межа |
| TC-04 | calculate_discount | 101, 10% | 10 центів | округлення |
| TC-05 | shipping_fee | 5000, basic | 700 | межа |
| TC-06 | shipping_fee | 10000, basic | 0 | межа |
| TC-07 | shipping_fee | будь-яка сума, gold | 0 | правило |
| TC-08 | Product | price_cents=0 | ValueError | негативний |
| TC-09 | require_int | True | TypeError | тип |
| TC-10 | Cart.add | той самий Product двічі | qty сумується | стан |
| TC-11 | Cart.add | інший Product, той самий ID | ValueError, кошик незмінний | негативний |
| TC-12 | Cart.remove | невідомий ID | KeyError | негативний |
| TC-13 | Order.place | порожній кошик | ValueError | негативний |
| TC-14 | Order | draft→placed→cancelled | статуси змінюються | перехід |
| TC-15 | Order | place двічі | ValueError | негативний |

## Стислий підсумок правил

- **Рівні:** basic 0–99, silver 100–499, gold ≥500; знижка 0/5/10%.
- **Доставка:** gold або ≥10000 → 0; 5000–9999 → 700; інакше 1500.
- **Кошик:** той самий екземпляр Product — сума кількості; інший об’єкт з тим самим ID — ValueError.
- **Order:** draft → placed → cancelled; порожній не оформлюється; summary фіксується на момент place().

## Рішення щодо межі та винятку

- **Межа:** для silver перевірено 99 (basic) і 100 (silver), щоб підтвердити поріг включно з 100.
- **Виняток:** після `add_product` з insufficient stock перевіряється, що `get_items_count()` не змінився — відхилення не повинно мутувати кошик.

## Результат запуску

Після `python -m pytest -v` усі тести мають статус **PASSED**.
