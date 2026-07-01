# partner_ai_analysis

Odoo 19 module that adds an AI-powered analysis tab to the customer form (`res.partner`), using a locally running [Ollama](https://ollama.com) instance as the backend. No cloud APIs, no subscriptions.

## What it does

When you open a contact in Odoo and click **Generate AI Analysis**, the module gathers available data from that record — sector, tags, internal notes, confirmed sale orders — and sends a structured prompt to your local LLM. The response is saved directly on the contact and a note is posted in the chatter with the model used and the date.

The analysis is broken into three sections:

1. **Behavioral profile** — what kind of buyer this contact appears to be
2. **Purchase potential** — estimated long-term value based on available data
3. **Sales recommendation** — a concrete approach for the sales rep

## Configuration

The Ollama server URL and model name are stored in `ir.config_parameter` and can be changed from **Settings → CRM** without touching any code. Defaults are `http://localhost:11434` and `gemma4:e2b`.

## Requirements

- Odoo Community 19.0
- [Ollama](https://ollama.com) running locally or on an accessible server
- A compatible model pulled: `ollama run gemma4:e2b`
- Python `requests` library (included in Odoo's standard dependencies)

## Installation

1. Clone or copy this repository into your Odoo `addons` path.
2. Restart Odoo and update the module list.
3. Install **AI Client Analyzer (Ollama Local)** from the Apps menu.
4. Go to **Settings → CRM** and verify the Ollama URL and model name match your setup.

## Compatibility

| Odoo version | Status |
|---|---|
| 19.0 Community | ✓ Tested |

## License

LGPL-3
