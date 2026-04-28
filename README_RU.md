# NOUZ — Семантический MCP-сервер для вашей базы знаний

Работает с Obsidian, Logseq и любыми директориями Markdown-файлов.

> *Структура появляется из содержания.*

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/protocol-MCP_stdio-lightgrey.svg)](https://modelcontextprotocol.io)
[![PyPI](https://img.shields.io/badge/pypi-nouz--mcp-orange.svg)](https://pypi.org/project/nouz-mcp/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19595850.svg)](https://doi.org/10.5281/zenodo.19595850)

🇬🇧 [English version](README_EN.md)

---

## Зачем нужен Nouz

Когда база знаний растёт — размещение документов по папкам перестаёт работать. Агент видит файлы, но не понимает, как связаны ваши идеи и документы.

NOUZ даёт агенту семантические координаты. Каждая заметка получает знак домена, уровень в иерархии и связи с другими заметками. Домен присваивается именно из содержания файла, или же вами вручную, если вы хотите строгую иерархию.

---

## Что делает

NOUZ выступает прослойкой между вашей базой заметок и AI-агентом. Он берет на себя всю работу по структурированию хаоса:

1. **Автоматическая классификация (Семантика)**  
   Вы задаете "Ядра" — базовые домены ваших интересов (например: 🧠 Системное мышление, 🧬 Наука, 💻 Код). Когда вы добавляете новую заметку, NOUZ читает ее текст, сравнивает векторы и автоматически присваивает ей правильный домен (Знак) или комбинацию доменов.

2. **Выявление скрытых связей (Мосты)**  
   Сервер не просто строит направленный граф (DAG). Он умеет находить неочевидные пересечения между дисциплинами:
   - *Семантические мосты:* две заметки из разных доменов говорят об одном и том же.
   - *Теговые мосты:* у заметок есть общие скрытые концепты на уровне тегов.
   - *Аналогии:* заметки играют одинаковую структурную роль в разных науках (например, "фреймворк" в IT и "таксономия" в биологии).

3. **Отслеживание эволюции базы (Дрейф)**  
   NOUZ умеет агрегировать данные снизу вверх. Если в папке "Философия" вы начали писать слишком много заметок про алгоритмы, система заметит это и покажет расхождение (core drift) — ваша папка эволюционировала.

В зависимости от ваших нужд, NOUZ может работать в трех режимах: от простого визуального графа (**LUCA**) до строгой 5-уровневой самоорганизующейся иерархии (**SLOI**).

---

## Как это работает

1. Вы описываете домены в `config.yaml` — чем каждый занимается, на каком языке говорит.
2. Сервер превращает описания в векторы-эталоны (локально, через LM Studio или Ollama).
3. Каждая новая заметка проецируется на эти оси. Знак определяется содержанием, или вами.
4. Модули автоматически получают `core_mix` — агрегированный состав ядер от всех своих квантов. Если `sign` модуля расходится с `core_mix` — сервер сообщает о `core_drift`.

**Три типа мостов** находят связи между заметками из разных доменов: семантические (тексты близки), теговые (концепты пересекаются), аналогические (похожая роль в графе).

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
| `add_entity` | Создать сущность в один шаг (авто sign, tags, parents) |
| `process_orphans` | Автозаполнение файлов без разметки |

---

## Конфигурация

Минимальный `config.yaml`:

```yaml
mode: prizma

etalons:
  - sign: S
    name: Systems Thinking
    text: >
      Methodology for analysing complex objects: feedback loops,
      emergent properties, self-regulation, bifurcation points.
      Cybernetics, synergetics, dissipative structures — tools for
      understanding how the whole exceeds the sum of its parts.
      Not data and not code — a way of thinking about complexity.
  - sign: D
    name: Data & Science
    text: >
      Physics and cosmology: Lagrangians, curvature tensors, quarks,
      fermions, plasma, vacuum fluctuations, cosmic microwave background.
      Pure science about the nature of matter, energy and spacetime.
  - sign: E
    name: Engineering
    text: >
      Software engineering, ML, infrastructure: writing and debugging
      code, deployment, containerisation, neural networks, inference,
      microservices, CI/CD, refactoring, APIs. The practical discipline
      of building computational systems from architecture to production.

thresholds:
  sign_spread: 0.05
  confident_spread: 60.0
  pattern_second_sign_threshold: 30.0
  semantic_bridge_threshold: 0.55
  structural_bridge_threshold: 0.55
  parent_link_threshold: 0.55
```

После настройки запустите `calibrate_cores` — сервер создаст эталонные векторы.
Проверьте попарные косинусы: mean-centered между разными доменами должен быть
заметно ниже сырого. Если все пары примерно одинаковые — усильте различия в текстах.

### Реальный пример расчёта

Вот фактические результаты для эталонов S/D/E с моделью `text-embedding-granite-embedding-278m-multilingual`:

```
=== Pairwise Cosine (raw) ===
S↔D: 0.5890    S↔E: 0.5853    D↔E: 0.6011

=== Pairwise Cosine (mean-centered) ===
S↔D: -0.5051   S↔E: -0.5120   D↔E: -0.4827
```

Отрицательные mean-centered значения — отличный результат: ядра семантически хорошо разделены. Самоклассификация: S→99.2%, D→97.6%, E→96.9%.

| Переменная | По умолчанию | Описание |
| --- | --- | --- |
| `OBSIDIAN_ROOT` | `./obsidian` | Путь к хранилищу |
| `MODE` | `luca` | `luca`, `prizma` или `sloi` |
| `EMBED_PROVIDER` | `openai` | `openai`, `lmstudio`, `ollama` |
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
