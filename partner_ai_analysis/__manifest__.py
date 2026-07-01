# -*- coding: utf-8 -*-
{
    'name': 'AI Client Analyzer (Ollama Local)',
    'version': '19.0.1.0.0',
    'category': 'Sales/CRM',
    'summary': 'Free unlimited AI analysis of customer behavior and sales potential using a local LLM via Ollama.',
    'description': """
AI Client Analyzer for Odoo — Powered by Ollama (Local LLM)
============================================================
Generate instant AI-powered commercial analysis for any customer directly
from their Contact form (res.partner). Uses your own local Ollama instance —
no API costs, no cloud subscriptions, fully private.

Features:
---------
- One-click AI analysis on any contact/customer record
- Structured output: behavioral profile, purchase potential, sales recommendation
- Configurable Ollama URL and model from Settings > CRM (no hardcoding)
- Reads confirmed sale orders for richer context (requires 'sale' module)
- Chatter note logged on every generation (tracks model used and date)
- Full error handling with user-friendly messages (timeout, connection refused)
- Compatible with any Ollama model: Gemma, Llama 3, Mistral, Phi-3, etc.
- 4 unit tests included (mocked HTTP, no live Ollama required for CI)

Requirements:
-------------
- Ollama installed and running (https://ollama.com)
- A compatible model downloaded: ollama run gemma4:e2b
    """,
    'author': 'Jose Manuel Lopez',
    'website': 'https://www.linkedin.com/in/jose-manuel-lopez-33705a325/',
    'maintainer': 'Jose Manuel Lopez',
    'support': 'ljosemanuel057@gmail.com',
    'images': ['static/description/icon.png'],
    'depends': [
        'base',
        'crm',
        'sale',
    ],
    'data': [
        'data/ir_config_parameter_data.xml',
        'views/res_partner_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'price': 0,
    'currency': 'EUR',
}
