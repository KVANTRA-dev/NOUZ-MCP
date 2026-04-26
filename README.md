# NOUZ — Семантический движок знаний для Obsidian

> *Структура появляется из содержания.*

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/protocol-MCP_stdio-lightgrey.svg)](https://modelcontextprotocol.io)
[![PyPI](https://img.shields.io/badge/pypi-nouz--mcp-orange.svg)](https://pypi.org/project/nouz-mcp/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19595850.svg)](https://doi.org/10.5281/zenodo.19595850)

---

## Зачем нужен Nouz

Когда база знаний растёт — размещение документов по папкам перестаёт работать. Агент видит файлы, но не понимает, как связаны ваши идеи и документы.

NOUZ даёт агенту семантические координаты. Каждая заметка получает знак домена, уровень в иерархии и связи с другими заметками. Домен присваивается именно из содержания файла, или же вами вручную, если вы хотите строгую иерархию.

---

## Что делает

**Ядра** — домены, которые вы задаёте сами. Примеры: Технология / Наука / Гуманитарные, или Системное мышление / Данные / Код. Сервер превращает описания в векторы-эталоны и проецирует заметки на эти оси.

**Знак (sign)** — координата заметки в пространстве доменов. Квант про нейросети лежит в модуле системного мышления, но по тексту тянет к вычислениям → знак составится из двух ядер.

**DAG вместо дерева** — направленный ациклический граф. У заметки может быть несколько родителей, несколько типов связей.

**Три режима работы:**

| Режим | Граф | Семантика | Иерархия |
|-------|------|-----------|----------|
| **LUCA** | ✅ | ❌ | Свободная |
| **PRIZMA** | ✅ | Ядра, мосты, drift | Свободная |
| **SLOI** | ✅ | ✅ | Строгая 5-уровневая |

---

## Как это работает

1. Вы описываете домены в `config.yaml` — чем каждый занимается, на каком языке говорит.
2. Сервер превращает описания в векторы-эталоны (локально, через LM Studio или Ollama).
3. Каждая новая заметка проецируется на эти оси. Знак определяется содержанием, или вами.
4. Модули автоматически получают `core_mix` — агрегированный состав ядер от всех своих квантов. Если `sign` модуля расходится с `core_mix` — сервер сообщает о `core_drift`.

**Три типа мостов** находят связи между заметками из разных доменов: семантические (тексты близки), теговые (концепты пересекаются), аналогические (похожая роль в графе).

> Вдохновлено исследованием рекурсивной самоорганизации — [статья на Zenodo](https://doi.org/10.5281/zenodo.19595850).

---

## Быстрый старт

```bash
pip install nouz-mcp
OBSIDIAN_ROOT=/path/to/vault nouz-mcp
```

Без `config.yaml` сервер стартует в режиме **LUCA** — граф без семантики, работает сразу.

Или из исходников:

```bash
git clone https://github.com/KVANTRA-dev/NOUZ-MCP
cd NOUZ-MCP
pip install -r requirements.txt
OBSIDIAN_ROOT=./vault python server.py
```

Подключение к Claude Desktop, Cursor, Opencode или любому MCP-клиенту:

```json
{
  "mcpServers": {
    "nouz": {
      "command": "nouz-mcp",
      "env": {
        "OBSIDIAN_ROOT": "/path/to/vault",
        "MODE": "prizma",
        "EMBED_API_URL": "http://127.0.0.1:1234/v1"
      }
    }
  }
}
```

---

## Инструменты MCP

| Инструмент | Зачем |
|------------|-------|
| `suggest_metadata` | Знак, уровень, мосты, drift-предупреждения |
| `write_file` | Записать заметку с YAML-разметкой |
| `read_file` | Прочитать заметку + метаданные |
| `calibrate_cores` | Обновить векторы-эталоны ядер |
| `recalc_signs` | Пересчитать знаки всех заметок |
| `recalc_core_mix` | Пересчитать агрегацию снизу вверх |
| `index_all` | Переиндексировать всю базу |
| `format_entity_compact` | Формула `(дети)[знак]{родители}` |
| `embed` | Получить вектор для текста |
| `list_files` | Список с фильтрами по уровню, знаку |
| `get_children` / `get_parents` | Траверс графа |
| `suggest_parents` | Найти родителей для сироты |

---

## Конфигурация

Минимальный `config.yaml`:

```yaml
mode: prizma

etalons:
  - sign: T
    name: Технология
    text: "программирование архитектура инфраструктура машинное обучение нейросети алгоритмы"
  - sign: S
    name: Наука
    text: "физика математика космология научная методология данные эксперимент"
  - sign: H
    name: Гуманитарные
    text: "философия психология история литература этика когнитивные науки"

thresholds:
  confident_spread: 60.0
  semantic_bridge_threshold: 0.55
```

После настройки запустите `calibrate_cores` — сервер создаст эталонные векторы.

| Переменная | По умолчанию | Описание |
| --- | --- | --- |
| `OBSIDIAN_ROOT` | `./obsidian` | Путь к хранилищу |
| `MODE` | `luca` | `luca`, `prizma` или `sloi` |
| `EMBED_PROVIDER` | `openai` | `openai`, `lmstudio`, `ollama`, `gigachat` |
| `EMBED_API_URL` | `http://127.0.0.1:1234/v1` | Эндпоинт для эмбеддингов |
| `EMBED_API_KEY` | *(пусто)* | API-ключ, если нужен |
| `EMBED_MODEL` | *(пусто)* | Имя модели |

---

## Приватность

| Компонент | Локально? |
|-----------|-----------|
| Эмбеддинги (LM Studio / Ollama) | ✅ Да |
| Ваши заметки | ✅ Да |
| Сервер NOUZ | ✅ Да |
| Контекст AI-агента (Claude, ChatGPT) | ❌ Уходит в облако |

Всё критичное остаётся на вашей машине.

---

## Разработка

```bash
git clone https://github.com/KVANTRA-dev/NOUZ-MCP
cd NOUZ-MCP
pip install -e .
python -m pytest test_server.py
```

---

## Ссылки

- 🌐 [kvantra.tech](https://kvantra.tech)
- 📦 [PyPI](https://pypi.org/project/nouz-mcp/)
- 🗂️ [Glama Registry](https://glama.ai/mcp/servers/KVANTRA-dev/NOUZ-MCP)
- 💬 [Telegram](https://t.me/volnaya_sreda)
- 🐙 [GitHub](https://github.com/KVANTRA-dev/NOUZ-MCP)
- 📄 [Статья "Рекурсивная самоорганизация как универсальный принцип"](https://doi.org/10.5281/zenodo.19595850)

---

MIT License © 2026 KVANTRA

*Косинусы считаются. Синтаксис меняется. Семантика остаётся.*

<!-- mcp-name: io.github.KVANTRA-dev/NOUZ-MCP -->
