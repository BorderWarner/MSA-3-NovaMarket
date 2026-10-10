# Task3. Масштабирование — отчёт

**Кластер:** minikube, образ `ghcr.io/yandex-practicum/scaletestapp:latest`.

---

## HPA по памяти

Deployment: 1 реплика, `limits/requests: 30Mi`. HPA: memory 80%, max 10.

Нагрузка через Locust (веб 8089), плавный набор пользователей. Лог HPA: `hpa-memory-watch.log`.

Память на поде росла: 4% → 91% за ~15 мин. На 91% (цель 80%, допуск 10% → срабатывает >88%) HPA добавил 2-ю реплику (`New size: 2`). Память упала до ~51%, потом пошла вверх.

События: `hpa-memory-events.log`.

---

## HPA по RPS

Prometheus + prometheus-adapter. Адаптер: `sum(rate(http_requests_total[1m])) by (pod)`. HPA: `type: Pods`, `requests_per_second`, `averageValue: "20"`, max 10.

Нагрузка: 400 пользователей, 240 сек. Лог locust: `locust-rps.log` — 31.8k запросов, 132 RPS, 0 ошибок.

Масштабирование (`hpa-rps-watch.log`):
- 1 → 3 → 5 → 7 реплик за ~90 сек
- На 7 репликах средний RPS/под ~19 (цель 20), стабильно

События: `hpa-rps-events.log` (`New size: 3, 5, 7`). Проверка метрик на подах: `rps-per-pod.log`.

---

## Скриншоты (Task3/screenshots/)
- `02-dashboard-memory.png` — реплики 2 (память)
- `03-prometheus-targets.png` — Targets UP
- `04-prometheus-graph.png` — суммарный RPS
- `05-prometheus-graph-pods.png` — RPS по поду
- `06-dashboard-rps.png` — реплики 7 (RPS)
