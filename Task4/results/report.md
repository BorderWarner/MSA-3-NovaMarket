# Task4. Rate Limiter + Circuit Breaker — отчёт

NGINX в Docker (`nginx:alpine`), конфиги из `Task4/`.

---

## Rate Limiter

`nginx-rate-limiter.conf`: две зоны `limit_req_zone` — `web_api` 50 r/s, `mobile_api` 30 r/s. Разделение по заголовку `client_type` через `map` + `$request_id` для исключения.

Нагрузка: `rate_limiter.py` (WebUser/MobileUser, weight=1), 400 пользователей, spawn 25.

Результаты (`rate-limiter-run.log`):
- web: ~2.5k запросов, ~1.2k ошибок 429 (~45%), пропуск ~50 r/s
- mobile: ~1.3k запросов, ~400 ошибок 429 (~30%), пропуск ~30 r/s

Зоны в error.log (`02-limit-zones.log`) не пересекаются.

---

## Circuit Breaker

`nginx-circuit-breaker.conf`: upstream `logistics_backend` (9090) с `max_fails=5 fail_timeout=30s`, таймауты 3с, `proxy_intercept_errors on`, fallback JSON 503.

Тестовый upstream на 9090: `fast` (200), `error` (500), `slow` (limit_rate 10 → timeout), `random` (по IP), `unknown` (404).

Нагрузка: `circuit_breaker.py` (SCENARIO env).

**Открытие контура** (`SCENARIO=timeout,healthy`, 12 users):
- slow: ~130 запросов, 100% ошибок, медиана 3000мс
- fast: ~200 запросов, ~25% ошибок (во время закрытия контура)
- error.log: `upstream timed out`, `temporarily disabled`, `no live upstreams`

**Восстановление** (`SCENARIO=healthy` после 35с паузы):
- 123 запроса, 1 ошибка (0.8%), медиана 1–2мс

**Fallback** (`?type=error`):
- прокси (8080): JSON 503
- прямой (9090): сырой 500

---

## Скриншоты (Task4/screenshots/)
- `01-channel-separated.png` — оба канала 200
- `02-rate-limiter-trigger.png` — mobile ошибок больше
- `03-rate-limiter-429.png` — вкладка Failures с 429
- `04-fallback-vs-direct.png` — прокси JSON 503 vs прямой 500
- `05-circuit-open-trigger.png` — slow 100% ошибок, медиана 3с
- `06-circuit-recovery.png` — после паузы ошибки ~0%
- `07-fallback-response.png` — JSON 503 fallback