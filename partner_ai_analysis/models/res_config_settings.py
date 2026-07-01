# -*- coding: utf-8 -*-

from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ollama_url = fields.Char(
        string='URL de Ollama',
        config_parameter='partner_ai_analysis.ollama_url',
        help='URL del servicio local de Ollama (ej: http://localhost:11434)'
    )
    ollama_model = fields.Char(
        string='Modelo de Ollama',
        config_parameter='partner_ai_analysis.ollama_model',
        help='Nombre del modelo instalado en Ollama (ej: gemma4:e2b)'
    )
