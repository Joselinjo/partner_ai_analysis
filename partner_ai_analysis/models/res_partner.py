# -*- coding: utf-8 -*-
import json
import logging
import requests
from odoo import models, fields, _
# pyrefly: ignore [missing-import]
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    ai_analysis = fields.Text(
        string='Análisis de IA',
        help='Análisis detallado de comportamiento, potencial y recomendaciones de venta generado por IA.'
    )

    def action_generate_ai_analysis(self):
        """
        Recoge datos del partner, construye el prompt, prepara el payload para Ollama
        y realiza la petición HTTP al servicio local.
        """
        self.ensure_one()

        # 1. Recolección de datos básicos y comerciales del cliente
        partner_name = self.name or _('Sin nombre')
        commercial_notes = self.comment or _('Sin notas comerciales registradas')
        industry = self.industry_id.name if 'industry_id' in self._fields and self.industry_id else _('No especificada')
        tags = ", ".join(self.category_id.mapped('name')) if self.category_id else _('Sin etiquetas')
        
        # También podemos obtener información básica adicional
        email = self.email or _('No especificado')
        phone = self.phone or _('No especificado')
        
        # Opcional: Obtener historial de ventas si el módulo sale está instalado y tiene registros
        sales_summary = ""
        if 'sale_order_ids' in self._fields:
            completed_sales = self.sale_order_ids.filtered(lambda s: s.state in ('sale', 'done'))
            if completed_sales:
                total_spent = sum(completed_sales.mapped('amount_total'))
                sales_count = len(completed_sales)
                sales_summary = f"\n- Pedidos de Venta confirmados: {sales_count}\n- Total gastado: {total_spent:.2f} {self.env.company.currency_id.name}"
            else:
                sales_summary = "\n- Historial de ventas: Sin pedidos de venta confirmados"

        # 2. Preparación del Prompt
        prompt = (
            f"Actua como analista de ventas y analiza el siguiente perfil de cliente para proponer una estrategia comercial:\n\n"
            f"Cliente: {partner_name}\n"
            f"Sector/Industria: {industry}\n"
            f"Etiquetas de clasificacion: {tags}\n"
            f"Contacto: Email: {email} | Telefono: {phone}\n"
            f"Notas comerciales del vendedor: {commercial_notes}\n"
            f"{sales_summary}\n\n"
            f"Por favor,  genera un analisis breve estructurado en los siguientes puntos:\n"
            f"1. Comportamiento y Perfil General: ¿Que tipo de cliente tiene pinta de ser?\n"
            f"2. Potencial de Compra: ¿Cual es su potencial estimado y valor a largo plazo?\n"
            f"3. Recomendacion de Venta: ¿Que estrategia u oferta se adaptaria mejor a este cliente basandonos en sus datos?\n"
            f"Responde de manera concisa y clara, la salida debe ser SOLO el analisis en modo informe,  sin caracteres raros."
        )

        # 3. Preparación del Payload para Ollama
        # Recuperamos la URL y el modelo de ir.config_parameter
        config_parameter = self.env['ir.config_parameter'].sudo()
        ollama_base_url = config_parameter.get_param('partner_ai_analysis.ollama_url', 'http://localhost:11434').rstrip('/')
        url = f"{ollama_base_url}/api/generate"
        model_name = config_parameter.get_param('partner_ai_analysis.ollama_model', 'gemma4:e2b')
        
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }

        # Registramos en el log de Odoo el payload que vamos a enviar (para depuración)
        _logger.info("Preparando petición para Ollama. Payload: %s", json.dumps(payload, indent=2))

        # 4. Envío de la petición HTTP a Ollama
        try:
            # timeout=180 para dar tiempo al LLM local de procesar y responder (especialmente si es un modelo pesado como gemma4)
            response = requests.post(url, json=payload, timeout=180)
            response.raise_for_status()
            
            result = response.json()
            response_text = result.get('response', '')
            
            if response_text:
                # Escribimos el análisis en el campo del cliente
                self.ai_analysis = response_text
                # Escribimos una nota en el chatter para registrar la fecha del análisis
                if hasattr(self, 'message_post'):
                    self.message_post(body=_(
                        "Se ha generado un nuevo análisis de IA utilizando el modelo %s."
                    ) % model_name)
            else:
                raise UserError(_("La IA de Ollama respondió correctamente pero no devolvió ningún texto en el campo 'response'."))

        except requests.exceptions.Timeout:
            raise UserError(_("Se agotó el tiempo de espera (timeout) al conectar con el servidor local de Ollama. "
                              "Es posible que el modelo esté tardando demasiado en procesar o cargarse en memoria."))
        except requests.exceptions.RequestException as e:
            _logger.error("Error al conectar con Ollama en %s: %s", url, str(e))
            # Mensaje de ayuda descriptivo para que el desarrollador solucione el problema localmente
            raise UserError(_("No se pudo conectar con el servicio local de Ollama en %s.\n\n"
                              "Por favor, verifica lo siguiente:\n"
                              "1. Ollama está instalado y corriendo en tu máquina local.\n"
                              "2. Has descargado el modelo ejecutando en tu terminal: 'ollama run %s'\n"
                              "3. El puerto y dirección son correctos y accesibles.") % (url, model_name))
