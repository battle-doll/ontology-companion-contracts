# Руководство для macOS / Windows / Linux

Целевые ОС — macOS, Windows и Linux; требуется Python 3.11+. Подтверждение выполнения на каждой ОС фиксируется отдельно от анализа кода и настройки матрицы CI.

| OS | Подтверждение выполнения |
| --- | --- |
| macOS | Локальные синтетические тесты Python 3.12.14 пройдены |
| Windows | `not_run` — CI настроен, выполнение ожидается |
| Linux | `not_run` — CI настроен, выполнение ожидается |
| Интеграция с хостом плагина | Ожидается; E2E хоста и публикация в каталоге не подтверждены |

Проверьте версию Python до создания окружения. Если она ниже 3.11, выберите уже установленный интерпретатор 3.11+. Активация не требуется: вызывайте Python окружения напрямую.

## macOS и Linux

```sh
python3 --version
python3 -m venv .venv
.venv/bin/python scripts/run.py validate examples/context-decision.json
.venv/bin/python scripts/check.py
```

## Windows PowerShell

```powershell
py -3 --version
py -3 -m venv .venv
.venv\Scripts\python.exe scripts/run.py validate examples/context-decision.json
.venv\Scripts\python.exe scripts/check.py
```

Основные примеры не требуют отдельного shell-установщика, Docker, Node.js, прав администратора, API-ключа или сетевого сервиса. Подготовка Python и поддержка хоста плагина — отдельные условия. Работа CLI на Linux не подтверждает наличие настольного хоста для Linux.

Команды запускают локальный код разработки. Они не устанавливают плагин и не создают размещённый сервис. Все примеры синтетические.

[Оглавление](README.md)
