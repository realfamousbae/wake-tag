# wake-tag

Telegram-бот, который реализует тег `/all` в групповых чатах: по команде упоминает всех участников группы.

## Команды

| Команда | Что делает |
|---|---|
| `/all` | Упоминает всех участников группы (кроме автора, ботов и удалённых аккаунтов) |
| `/start`, `/help` | Приветствие и справка |

Особенности:
- До 500 участников в группе; упоминания отправляются пачками по 50 штук.
- Тем, у кого нет `@username`, упоминание делается ссылкой по id.
- Для получения списка участников боту нужны права администратора (в больших группах это обязательно).

## Настройка

1. Создайте бота в [@BotFather](https://t.me/BotFather) и получите токен.
   Удобно задать права по умолчанию: `/mybots` → бот → *Bot Settings* → *Group Admin Rights*.
2. Получите `api_id` и `api_hash` на [my.telegram.org](https://my.telegram.org) → *API development tools*.
3. Передайте ключи **одним из способов**:
   - переменные окружения `TG_API_ID`, `TG_API_HASH`, `TG_BOT_TOKEN`;
   - файл `config.yaml` в корне (создаётся шаблон при первом запуске), секция `tech`: `api_id`, `api_hash`, `bot_token`.

Ключи нельзя коммитить: `config.yaml` и `.env` уже в `.gitignore`.

## Локальный запуск

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Тесты: `pip install -r requirements-dev.txt && pytest`.

## Деплой на Railway

Репозиторий готов к деплою: `railway.json` задаёт команду запуска, версия Python берётся из `.python-version`.
В сервисе задайте переменные `TG_API_ID`, `TG_API_HASH`, `TG_BOT_TOKEN`. Порты и домен не нужны — бот работает как фоновый воркер.

## Лицензия

GNU AGPL v3, см. [LICENSE.txt](LICENSE.txt).
