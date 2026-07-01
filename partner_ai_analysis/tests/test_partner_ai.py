# -*- coding: utf-8 -*-

from unittest.mock import patch
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
import requests

class TestPartnerAI(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Creamos un cliente de prueba para los tests
        cls.partner = cls.env['res.partner'].create({
            'name': 'Cliente de Prueba',
            'email': 'prueba@example.com',
            'comment': 'Nota comercial de prueba para análisis.',
        })

    def test_01_default_config_parameters(self):
        """Verificar que los valores de configuración por defecto se instalaron correctamente"""
        url = self.env['ir.config_parameter'].sudo().get_param('partner_ai_analysis.ollama_url')
        model = self.env['ir.config_parameter'].sudo().get_param('partner_ai_analysis.ollama_model')
        
        self.assertEqual(url, 'http://localhost:11434')
        self.assertEqual(model, 'gemma4:e2b')

    @patch('requests.post')
    def test_02_action_generate_ai_analysis_success(self, mock_post):
        """Probar generación exitosa de análisis mockeando Ollama"""
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'response': 'Este es un excelente cliente de prueba con alto potencial.'
        }
        
        # Ejecutamos la acción del modelo
        self.partner.action_generate_ai_analysis()
        
        # Comprobamos que el texto del análisis se haya guardado en el partner
        self.assertEqual(self.partner.ai_analysis, 'Este es un excelente cliente de prueba con alto potencial.')
        
        # Validamos que se haya ejecutado el POST con los parámetros correctos
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        
        # Validamos el endpoint de destino armado dinámicamente
        self.assertEqual(args[0], 'http://localhost:11434/api/generate')
        
        # Validamos el modelo enviado en el json payload
        self.assertEqual(kwargs['json']['model'], 'gemma4:e2b')

    @patch('requests.post')
    def test_03_action_generate_ai_analysis_timeout(self, mock_post):
        """Probar la captura correcta de una excepción de Timeout"""
        mock_post.side_effect = requests.exceptions.Timeout("Timeout")
        
        # Validamos que se eleve el error de usuario traducido
        with self.assertRaises(UserError) as e:
            self.partner.action_generate_ai_analysis()
            
        self.assertIn("tiempo de espera", str(e.exception))

    @patch('requests.post')
    def test_04_action_generate_ai_analysis_connection_error(self, mock_post):
        """Probar la captura correcta de un error de conexión (ej: Ollama apagado)"""
        mock_post.side_effect = requests.exceptions.ConnectionError("Connection Refused")
        
        # Validamos que se eleve el error de usuario traducido indicando la URL
        with self.assertRaises(UserError) as e:
            self.partner.action_generate_ai_analysis()
            
        self.assertIn("No se pudo conectar con el servicio local", str(e.exception))
