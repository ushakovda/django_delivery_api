import requests
from celery import shared_task
from django.core.cache import cache

from .models import Parcel
from decimal import Decimal

@shared_task
def fetch_exchange_rate():
    """Получает текущий курс доллара к рублю с сайта ЦБ РФ, используя кэш."""
    exchange_rate = cache.get('usd_to_rub')
    if exchange_rate is None:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            exchange_rate = str(data['Valute']['USD']['Value'])
            print(type(exchange_rate))
            print(exchange_rate)
            cache.set('usd_to_rub', exchange_rate, timeout=300)
        except Exception as e:
            print(f"Ошибка получения курса: {e}")
            return None
    return exchange_rate

@shared_task
def update_delivery_cost():
    """Обновляет стоимость доставки для необработанных посылок."""
    exchange_rate = fetch_exchange_rate()

    if exchange_rate is None:
        print("Курс доллара не доступен.")
        return

    parcels = Parcel.objects.filter(delivery_cost_rub__isnull=True)

    for parcel in parcels:
        delivery_cost = (parcel.weight * Decimal(0.5) + parcel.content_value_usd * Decimal(0.01)) * Decimal(exchange_rate)
        parcel.delivery_cost_rub = round(delivery_cost, 2)
        parcel.save()

    print(f'Обновлены стоимости доставки для {len(parcels)} посылок.')
