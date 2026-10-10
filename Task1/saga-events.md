# Saga-хореография оформления заказа NovaMarket

Управление распределённой транзакцией реализовано хореографией: каждый сервис,
получив событие, меняет своё состояние и публикует следующее событие. Оркестратора,
который знает весь сценарий, нет — это позволяет подключать новые потребители
событий без изменения существующих сервисов.

Типы событий:

- `domain` — событие, отражающее произошедший в домене факт;
- `failure` — событие об ошибке на шаге Saga;
- `compensation` — событие отката уже выполненного шага.

## Реестр событий

| Этап | Тип события | Название |
| :-: | :- | :- |
| Покупатель подтвердил состав заказа, адрес, способ доставки и способ оплаты | domain | OrderCreated |
| Товары зарезервированы на складе продавца | domain | InventoryReserved |
| Нужного количества товара нет на складе либо склад недоступен | failure | InventoryReservationFailed |
| Средства списаны, платёж подтверждён платёжным шлюзом | domain | PaymentSucceeded |
| Платёж отклонён: недостаток средств, отказ банка, таймаут шлюза | failure | PaymentFailed |
| Заказ оплачен, заявка на доставку передана в логистику | domain | DeliveryRequested |
| Логистический провайдер создал заявку и вернул трек-номер | domain | DeliveryRegistered |
| Логистический провайдер не принял заявку: таймаут или сервис недоступен | failure | DeliveryFailed |
| Покупатель получил заказ, резерв списан в продажу | domain | DeliveryCompleted |
| Продавец получил уведомление о новом заказе | domain | NotificationSent |
| Изменился статус заказа (для клиента и проекций чтения) | domain | OrderStatusChanged |
| Требуется снять резерв с товара | compensation | ReleaseReservationRequested |
| Резерв снят, товар снова доступен в каталоге | compensation | ReservationReleased |
| Требуется вернуть деньги покупателю | compensation | RefundRequested |
| Деньги возвращены покупателю | compensation | RefundSucceeded |

## Цепочка событий по сценариям

Успешный сценарий:

```
OrderCreated -> InventoryReserved -> PaymentSucceeded -> DeliveryRequested
             -> DeliveryRegistered -> DeliveryCompleted
```

Отказ на складе:

```
OrderCreated -> InventoryReservationFailed -> OrderStatusChanged(CANCELLED)
```

Отказ оплаты:

```
OrderCreated -> InventoryReserved -> PaymentFailed
             -> ReleaseReservationRequested -> ReservationReleased
             -> OrderStatusChanged(CANCELLED)
```

Отказ доставки после оплаты:

```
OrderCreated -> InventoryReserved -> PaymentSucceeded -> DeliveryRequested
             -> DeliveryFailed -> RefundRequested -> RefundSucceeded
             -> ReleaseReservationRequested -> ReservationReleased
             -> OrderStatusChanged(CANCELLED)
```
