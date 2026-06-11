<h1 align="center">
  <img src="resources/prompt-icon.svg" alt="pfuzz">
  pfuzz
  <img src="resources/prompt-icon.svg" alt="pfuzz">
</h1>

<h3 align="center">
  The open-source tool to harden your GenAI applications against prompt attacks
</h3>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/python-3.9%20--%203.12-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/LLM%20providers-16-purple.svg" alt="Providers">
  <img src="https://img.shields.io/badge/attacks-16%2B-red.svg" alt="Attacks">
  <img src="https://img.shields.io/badge/tests-93%20passing-brightgreen.svg" alt="Tests">
</p>

<p align="center">
  <b>Maintained by Osvaldo Janeri Filho</b>
</p>

---

> ### 🙏 Credits / Créditos
> **pfuzz** is a fork of the excellent open-source [**ps-fuzz (Prompt Fuzzer)**](https://github.com/prompt-security/ps-fuzz),
> originally created by **[Prompt Security](https://prompt.security)** — *the Complete Platform for GenAI Security*.
> All original research, attack design and engineering credit belongs to the ps-fuzz authors. This fork preserves
> their work under the MIT License, modernizes the codebase, and adds a Portuguese/English bilingual direction.
>
> **pfuzz** é um fork da excelente ferramenta open-source [**ps-fuzz (Prompt Fuzzer)**](https://github.com/prompt-security/ps-fuzz),
> originalmente criada pela **[Prompt Security](https://prompt.security)**. Todo o crédito de pesquisa, design dos
> ataques e engenharia original pertence aos autores do ps-fuzz. Este fork preserva o trabalho deles sob a licença MIT.

---

## 📑 Table of Contents

- [What is pfuzz?](#-what-is-pfuzz)
- [Why & when to use it](#-why--when-to-use-it)
- [How it works](#-how-it-works)
- [Installation](#-installation)
- [Quick start](#-quick-start)
- [Usage & modes](#-usage--modes)
- [Command-line options](#-command-line-options)
- [Environment variables & providers](#-environment-variables--llm-providers)
- [Examples](#-examples)
- [Supported attacks](#-supported-attacks)
- [Understanding the results](#-understanding-the-results)
- [Development](#-development)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ What is pfuzz?

**pfuzz** is an interactive command-line tool that **assesses the security of your GenAI
application's system prompt** by simulating a wide range of dynamic, LLM-driven attacks against it.

It does three things:

1. **Attacks your system prompt** with 16+ adversarial techniques (jailbreaks, prompt injection,
   RAG poisoning, system-prompt extraction) — *tailored dynamically* to your app's domain.
2. **Scores the outcome** — for each attack it tells you whether your prompt was **Broken**,
   **Resilient**, or returned **Errors**.
3. **Gives you a Playground** — an interactive chat where you iterate on your system prompt and
   re-test until it is hardened.

> ⚠️ **pfuzz is a defensive tool.** Use it to test **your own** GenAI applications. Running it
> consumes LLM tokens, which costs money on paid providers.

---

## 🎯 Why & when to use it

| Use it when… | What it helps with |
|--------------|--------------------|
| You are **building a GenAI app** (chatbot, agent, assistant) | Find weaknesses in your system prompt *before* attackers do |
| You are about to **ship to production** | A pre-launch security gate for prompt robustness |
| You maintain a **RAG / vector-DB** pipeline | Detect data-poisoning that overrides your instructions |
| You want to **iterate on a prompt** | The Playground lets you harden and re-test in a loop |
| You run **security reviews / red-teaming** | A reproducible, scriptable battery of prompt attacks |
| You need **CI gating** | Batch mode runs unattended and is automation-friendly |

**Not** a tool for attacking third-party systems you do not own or have permission to test.

---

## 🧠 How it works

```
        ┌──────────────┐      generates attacks      ┌──────────────┐
        │  Attack LLM   │ ──────────────────────────▶ │  Target LLM   │
        │ (the "attacker")│                            │ (your system │
        └──────────────┘ ◀────── responses ────────── │   prompt)     │
                │                                      └──────────────┘
                ▼
        ┌───────────────────────────────┐
        │  Scoring: Broken / Resilient / │
        │  Errors  → results table        │
        └───────────────────────────────┘
```

pfuzz reads context from **your system prompt**, asks an **attack model** to craft adversarial
inputs adapted to that context, sends them to the **target model** running your prompt, and
evaluates whether your prompt held up. Tests run **multi-threaded** for speed.

---

## 🚀 Installation

> Requires **Python 3.9 – 3.12**.

### From source (recommended for this fork)

```bash
git clone https://github.com/ojaneri/pfuzz.git
cd pfuzz
python -m venv .venv && source .venv/bin/activate     # or: uv venv --python 3.11
pip install -e .                                       # add ".[dev]" for tests
```

### Set your provider key and run

```bash
export OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXX
pfuzz
```

---

## ⚡ Quick start

```bash
# 1. Interactive mode (default) — guided menu + Playground
pfuzz

# 2. See what attacks are available (no tokens spent)
pfuzz --list-attacks

# 3. See all supported LLM providers
pfuzz --list-providers

# 4. Batch mode against a system-prompt file
pfuzz -b ./system_prompt.examples/medium_system_prompt.txt
```

Then: **input your system prompt → run the tests → use the Playground to iterate** until your
prompt resists the attacks.

---

## 💻 Usage & modes

**pfuzz supports:**

- 🧞 **16 LLM providers** (OpenAI, Anthropic, Azure, Cohere, Google, Ollama, and more)
- 🔫 **16+ attack types** across 4 categories
- 💬 **Interactive mode** with a Playground chat
- 🤖 **CLI / batch mode** for automation & CI
- 🧵 **Multi-threaded** test execution
- 🔌 **Custom & self-hosted endpoints** (Ollama, vLLM, LocalAI, LM Studio)

| Mode | Command | When to use |
|------|---------|-------------|
| Interactive | `pfuzz` | Exploration, hardening, the Playground |
| Batch | `pfuzz -b <prompt-file>` | Scripting, CI, unattended runs |
| List attacks | `pfuzz --list-attacks` | Discover available tests (free) |
| List providers | `pfuzz --list-providers` | See supported LLMs (free) |

---

## 🛠 Command-line options

| Option | Description |
|--------|-------------|
| `--list-providers` | List all available LLM providers and exit |
| `--list-attacks` | List available attacks and exit |
| `--attack-provider` / `--attack-model` | Provider/model used to **generate** attacks |
| `--target-provider` / `--target-model` | Provider/model **under test** (runs your prompt) |
| `-n, --num-attempts` | Number of different attack prompts per test |
| `-t, --num-threads` | Number of worker threads |
| `-a, --attack-temperature` | Temperature for the attack model |
| `-d, --debug-level` | Debug level (0–2) |
| `-b, --batch` | Run unattended (batch) mode |
| `--ollama-base-url` | Base URL for a self-hosted Ollama API |
| `--openai-base-url` | Base URL for OpenAI-compatible endpoints |
| `--embedding-provider` | Embedding provider (`ollama` or `open_ai`) — required for RAG tests |
| `--embedding-model` | Embedding model name — required for RAG tests |
| `--embedding-ollama-base-url` / `--embedding-openai-base-url` | Base URLs for embeddings |
| `--custom-benchmark` | Path to a custom benchmark CSV |
| `--tests` | JSON list to run only a subset of attacks, e.g. `'["ucar","dan"]'` |

---

## 🔑 Environment variables & LLM providers

Set the API key for your preferred provider. The default is `OPENAI_API_KEY`. You can also place
the key in a `.env` file in the current directory.

<details><summary><b>Full list of supported providers (click to expand)</b></summary>

| Environment key | Provider |
|-----------------|----------|
| `OPENAI_API_KEY` | OpenAI chat models |
| `ANTHROPIC_API_KEY` | Anthropic chat models |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI Chat Completion |
| `ANYSCALE_API_KEY` | Anyscale chat models |
| `BAICHUAN_API_KEY` | Baichuan chat models |
| `COHERE_API_KEY` | Cohere chat models |
| `EVERLYAI_API_KEY` | EverlyAI chat models |
| `FIREWORKS_API_KEY` | Fireworks chat models |
| `GIGACHAT_CREDENTIALS` | GigaChat models |
| `GOOGLE_API_KEY` | Google PaLM chat models |
| `JINA_API_TOKEN` | Jina AI chat models |
| `KONKO_API_KEY` | ChatKonko chat models |
| `MINIMAX_API_KEY`, `MINIMAX_GROUP_ID` | Minimax models |
| `PROMPTLAYER_API_KEY` | PromptLayer + OpenAI |
| `QIANFAN_AK`, `QIANFAN_SK` | Baidu Qianfan chat models |
| `YC_API_KEY` | YandexGPT models |

</details>

---

## 📚 Examples

**Single batch run:**
```bash
pfuzz -b ./system_prompt.examples/medium_system_prompt.txt
```

**Custom benchmark:**
```bash
pfuzz -b ./system_prompt.examples/medium_system_prompt.txt \
      --custom-benchmark=pfuzz/attack_data/custom_benchmark1.csv
```

**Run only a subset of attacks:**
```bash
pfuzz -b ./system_prompt.examples/medium_system_prompt.txt --tests='["ucar","dan"]'
```

**RAG poisoning test (needs embeddings):**
```bash
pfuzz -b ./system_prompt.examples/medium_system_prompt.txt \
      --embedding-provider=open_ai \
      --embedding-model=text-embedding-ada-002 \
      --tests='["rag_poisoning"]'
```

**Self-hosted / OpenAI-compatible endpoint:**
```bash
pfuzz -b ./system_prompt.examples/medium_system_prompt.txt \
      --target-provider=open_ai \
      --target-model=custom-model \
      --openai-base-url=http://your-endpoint:8000/v1
```

---

## ⚔️ Supported attacks

pfuzz uses a **dynamic** approach — it derives context from your system prompt and adapts the
fuzzing accordingly.

#### 🔓 Jailbreak
- **AIM Jailbreak** — Machiavelli roleplay to elicit instructions on illegal activities.
- **Affirmative Suffix** — appends a suffix that coaxes affirmative responses to prohibited content.
- **Amnesia** — makes the LLM forget/ignore its system prompt.
- **Contextual Redirection** — tricks the LLM into a role that bypasses restrictions.
- **DAN (Do Anything Now)** — classic roleplay to break restrictions.
- **Harmful Behavior** — challenges the LLM with a harmful-behavior dataset.
- **Linguistic Evasion** — uses non-English languages to bypass filters.
- **Self Refine** — refines responses toward unethical directions.
- **UCAR** — asks the LLM to ignore content filters.
- **Base64 Evasion** — hides harmful prompts as base64.

#### 💉 Prompt Injection
- **Authoritative Role Impersonation** — impersonates an authority to misdirect outputs.
- **Complimentary Transition** — tests standards when switching topics after a compliment.
- **Ethical Compliance** — probes resistance on sensitive topics.
- **Typoglycemia Attack** — omits characters to exploit text-processing weaknesses.

#### 🧪 RAG & Vector Database
- **RAG Poisoning (Hidden Parrot)** — checks if malicious instructions embedded in vector-DB
  documents can override your system prompt.

#### 🕵️ System Prompt Extraction
- **System Prompt Stealer** — attempts to extract your internal configuration.

---

## 📊 Understanding the results

| Verdict | Meaning |
|---------|---------|
| 🔴 **Broken** | The LLM succumbed to the attack — a weakness to fix. |
| 🟢 **Resilient** | The LLM resisted the attack. |
| ⚪ **Errors** | Inconclusive result (e.g., API error). |

Aim for **Resilient** across the board. Use the **Playground** to tweak your system prompt and
re-run the failing attacks until they turn green.

---

## 🧰 Development

```bash
pip install -e ".[dev]"
pytest -v        # 93 tests
```

> **Note:** this fork migrated off the deprecated `pkg_resources` to `importlib.resources`, so it
> runs cleanly on modern `setuptools` (≥ 82) with **0 warnings**.

Project layout:

```
pfuzz/
├── cli.py                 # entry point (`pfuzz` command)
├── prompt_injection_fuzzer.py   # orchestration + scoring
├── attacks/               # the 16+ attack implementations
├── chat_clients.py        # provider-agnostic LLM clients (LangChain)
├── interactive_mode.py    # interactive shell + Playground
└── app_config.py          # CLI args & config
```

---

## 🌈 Roadmap

- [ ] **EN / PT-BR bilingual UX** (i18n) — *primary direction of this fork*
- [ ] Structured report export (JSON / HTML / Markdown)
- [ ] Per-attack hardening recommendations
- [ ] Run history & prompt-score comparison
- [ ] New GenAI attack types
- [ ] Docker image
- [ ] CI (lint + tests) on the fork

---

## 🍻 Contributing

Contributions are welcome! The easiest way to contribute is by **adding a new attack** —
see [`CONTRIBUTING.md`](CONTRIBUTING.md). In short: add a class under `pfuzz/attacks/`, register
it in `pfuzz/attack_loader.py`, add a test, and open a PR.

---

## 📄 License

[MIT](LICENSE) © Osvaldo Janeri Filho — fork of [ps-fuzz](https://github.com/prompt-security/ps-fuzz)
by Prompt Security (also MIT). Original credits preserved.
