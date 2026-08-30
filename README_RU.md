# Stellar Burgers UI Tests

[![CI](https://github.com/Nellie-ai/stellar-burgers-ui-tests/actions/workflows/ci.yml/badge.svg)](https://github.com/Nellie-ai/stellar-burgers-ui-tests/actions/workflows/ci.yml)

[English](README.md) | Русский

## Обзор

Набор end-to-end UI-тестов для учебного веб-приложения [Stellar Burgers](https://stellarburgers.education-services.ru/). Проект использует Selenium, pytest, Page Object Model, подготовку тестовых данных через API и отчётность Allure.

## Технологический стек

| Область | Инструменты |
| --- | --- |
| Язык | Python 3.10+ (в CI используется Python 3.12) |
| Тестовый раннер | pytest |
| Автоматизация браузера | Selenium WebDriver |
| Подготовка данных | API-клиент на requests |
| Отчётность | Allure Pytest |
| Паттерн | Page Object Model |
| CI | GitHub Actions |

## Что тестируется / Покрытие

Набор содержит 8 логических сценариев. Каждый сценарий параметризован для Google Chrome и Mozilla Firefox, поэтому сборка содержит 16 тест-кейсов.

### Конструктор и навигация

- переход из ленты заказов в конструктор;
- переход из конструктора в ленту заказов;
- открытие модального окна с деталями ингредиента;
- закрытие модального окна с деталями ингредиента;
- увеличение счётчика ингредиента после добавления ингредиента.

### Лента заказов

- увеличение счётчика выполненных заказов за всё время;
- увеличение счётчика выполненных заказов за сегодня;
- появление номера нового заказа в секции «В работе».

## Структура проекта

```text
.
├── .github/workflows/
│   ├── ci.yml                    # проверки конструктора на PR, push и вручную
│   └── e2e.yml                   # полный E2E-запуск вручную и еженедельно
├── locators/                     # Selenium-локаторы
├── pages/                        # Page Objects и общие действия WebDriver
├── tests/
│   ├── test_constructor.py       # сценарии конструктора и навигации
│   └── test_order_feed.py        # сценарии создания и отображения заказов
├── utils/
│   ├── api_client.py             # создание и удаление пользователей через API
│   ├── constants.py              # URL и настраиваемые таймауты
│   └── data.py                   # модель и генерация тестового пользователя
├── conftest.py                   # фикстуры браузера, авторизации и скриншотов
├── pytest.ini                    # настройки pytest и браузерные markers
└── requirements.txt
```

Авторизация и подготовка пользователя выполняются через API. Пользовательские сценарии с ингредиентами и заказами проверяются через браузерный интерфейс.

## Локальный запуск

Требования:

- Python 3.10 или новее;
- Google Chrome и Mozilla Firefox;
- сетевой доступ к учебному веб-приложению и API Stellar Burgers;
- Allure CLI — только если нужен локальный HTML-отчёт.

Selenium Manager автоматически подбирает совместимые драйверы браузеров.

```bash
python -m venv .venv
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Активируйте виртуальное окружение способом, принятым в вашей операционной системе.

### Конфигурация

| Переменная | Значение по умолчанию | Назначение |
| --- | --- | --- |
| `STELLAR_BURGERS_URL` | `https://stellarburgers.education-services.ru` | URL веб-приложения |
| `STELLAR_BURGERS_API_URL` | значение `STELLAR_BURGERS_URL` | Базовый URL API |
| `SELENIUM_TIMEOUT` | `15` | Таймаут запросов по умолчанию в секундах |
| `ORDER_TIMEOUT` | `180` | Максимальное ожидание создания и появления заказа в секундах |

Пример:

```bash
ORDER_TIMEOUT=240 python -m pytest -m chrome -v
```

PowerShell:

```powershell
$env:ORDER_TIMEOUT = "240"
python -m pytest -m chrome -v
```

### Команды запуска тестов

```bash
python -m pytest -v
python -m pytest -m chrome -v
python -m pytest -m firefox -v
python -m pytest tests/test_constructor.py -v
```

### Allure

```bash
python -m pytest --alluredir=allure_results --clean-alluredir
allure serve allure_results
```

При ошибке на этапах setup или test набор прикладывает скриншот браузера, если WebDriver уже создан.

## CI

- `.github/workflows/ci.yml` запускает сценарии конструктора в Chrome и Firefox для pull request, push в `main` и ручного запуска; результаты Allure сохраняются отдельно для каждого браузера.
- `.github/workflows/e2e.yml` запускает полный набор в обоих браузерах вручную и каждый понедельник в 03:00 UTC; результаты Allure сохраняются отдельно для каждого браузера.

## Примечания / Ограничения

- Тесты зависят от доступности и поведения публичного учебного веб-приложения и API.
- Сценарии ленты создают реальные заказы, поэтому глобальные счётчики заказов на стенде изменяются.
- Проверки счётчиков могут занимать до трёх минут; параллельный запуск сценариев ленты не рекомендуется из-за общих глобальных счётчиков.
- В тестовых фикстурах браузеры запускаются в headless-режиме.
- `allure_results/` создаётся локально или в CI и не отслеживается Git.

## Лицензия / Происхождение

В репозитории присутствуют MIT LICENSE для оригинального тестового кода и PROVENANCE.md с описанием учебного происхождения сценариев и границ использования внешнего приложения. MIT License распространяется только на оригинальный тестовый код этого репозитория и не предоставляет прав на внешнее приложение или сторонние материалы.
