# -*- coding: utf-8 -*-
"""
Helper - Backend Flask
Webhook para receber mensagens do WhatsApp via Evolution API
"""

from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import requests
from typing import Dict, Optional
import base64

from sheets_manager import SheetsManager
from ocr_engine import OCREngine
from message_processor import MessageProcessor
from messages import HelperMessages
from auditor import Auditor

# Carrega variaveis de ambiente
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')

# Configuracoes
GOOGLE_CREDENTIALS = os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
EVOLUTION_API_URL = os.getenv('EVOLUTION_API_URL')
EVOLUTION_API_KEY = os.getenv('EVOLUTION_API_KEY')
EVOLUTION_INSTANCE = os.getenv('EVOLUTION_INSTANCE_NAME')
AUTHORIZED_NUMBERS = os.getenv('AUTHORIZED_NUMBERS', '').split(',')
ALERT_THRESHOLD = float(os.getenv('ALERT_THRESHOLD_PERCENT', '30'))

# Inicializa componentes
sheets_manager = SheetsManager(GOOGLE_CREDENTIALS, SPREADSHEET_ID)
ocr_engine = OCREngine()
message_processor = MessageProcessor()
helper_messages = HelperMessages()
auditor = Auditor(sheets_manager, ALERT_THRESHOLD)


def is_authorized(phone_number: str) -> bool:
    """Verifica se o numero esta autorizado"""
    # Remove caracteres especiais e espacos
    clean_number = ''.join(filter(str.isdigit, phone_number))
    
    for authorized in AUTHORIZED_NUMBERS:
        clean_authorized = ''.join(filter(str.isdigit, authorized))
        if clean_number.endswith(clean_authorized) or clean_authorized.endswith(clean_number):
            return True
    
    return False


def send_whatsapp_message(phone_number: str, message: str) -> bool:
    """
    Envia mensagem via Evolution API
    
    Args:
        phone_number: Numero do destinatario
        message: Texto da mensagem
        
    Returns:
        True se enviado com sucesso
    """
    try:
        url = f"{EVOLUTION_API_URL}/message/sendText/{EVOLUTION_INSTANCE}"
        
        headers = {
            'Content-Type': 'application/json',
            'apikey': EVOLUTION_API_KEY
        }
        
        payload = {
            'number': phone_number,
            'text': message
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.status_code == 200
    
    except Exception as e:
        print(f"Erro ao enviar mensagem: {str(e)}")
        return False


def process_text_message(phone_number: str, message_text: str):
    """Processa mensagem de texto"""
    try:
        # Verifica se e pedido de ajuda
        if message_processor.is_help_request(message_text):
            response = helper_messages.ajuda()
            send_whatsapp_message(phone_number, response)
            return
        
        # Processa a mensagem
        expenses, custom_date = message_processor.parse_message(message_text)
        
        if not expenses:
            response = helper_messages.dados_incompletos('valor')
            send_whatsapp_message(phone_number, response)
            return
        
        # Formata data
        data = message_processor.format_date(custom_date)
        
        # Registra cada gasto
        registered = 0
        total = 0.0
        
        for expense in expenses:
            # Valida o gasto
            valid, error_field = message_processor.validate_expense(expense)
            
            if not valid:
                response = helper_messages.dados_incompletos(error_field)
                send_whatsapp_message(phone_number, response)
                continue
            
            # Verifica duplicata
            if sheets_manager.check_duplicate(
                expense['descricao'],
                expense['valor'],
                data
            ):
                response = helper_messages.gasto_duplicado(
                    expense['descricao'],
                    expense['valor'],
                    data
                )
                send_whatsapp_message(phone_number, response)
                continue
            
            # Adiciona na planilha
            success = sheets_manager.add_expense(
                data=data,
                descricao=expense['descricao'],
                categoria=expense['categoria'],
                valor=expense['valor']
            )
            
            if success:
                registered += 1
                total += expense['valor']
        
        # Envia confirmacao
        if registered > 0:
            if registered == 1:
                response = helper_messages.gasto_registrado(
                    expenses[0]['valor'],
                    expenses[0]['descricao']
                )
            else:
                response = helper_messages.multiplos_gastos_registrados(
                    registered,
                    total
                )
            
            send_whatsapp_message(phone_number, response)
    
    except Exception as e:
        print(f"Erro ao processar mensagem: {str(e)}")
        response = helper_messages.erro_generico()
        send_whatsapp_message(phone_number, response)


def process_image_message(phone_number: str, image_data: bytes):
    """Processa mensagem com imagem (OCR)"""
    try:
        # Processa a imagem
        text = ocr_engine.process_image(image_data)
        
        # Valida se parece um recibo
        if not ocr_engine.validate_receipt(text):
            response = helper_messages.ocr_falha()
            send_whatsapp_message(phone_number, response)
            return
        
        # Extrai gastos
        expenses = ocr_engine.extract_expenses(text)
        
        if not expenses:
            response = helper_messages.ocr_falha()
            send_whatsapp_message(phone_number, response)
            return
        
        # Envia confirmacao inicial
        response = helper_messages.ocr_sucesso(len(expenses))
        send_whatsapp_message(phone_number, response)
        
        # Registra cada gasto
        data = message_processor.format_date()
        registered = 0
        
        for expense in expenses:
            success = sheets_manager.add_expense(
                data=data,
                descricao=expense['descricao'],
                categoria=expense['categoria'],
                valor=expense['valor']
            )
            
            if success:
                registered += 1
        
        # Envia resumo
        if registered > 0:
            total = sum(e['valor'] for e in expenses)
            response = helper_messages.multiplos_gastos_registrados(registered, total)
            send_whatsapp_message(phone_number, response)
    
    except Exception as e:
        print(f"Erro ao processar imagem: {str(e)}")
        response = helper_messages.erro_generico()
        send_whatsapp_message(phone_number, response)


@app.route('/webhook', methods=['POST'])
def webhook():
    """Endpoint do webhook para receber mensagens"""
    try:
        data = request.json
        
        # Extrai informacoes da mensagem
        message_data = data.get('data', {})
        phone_number = message_data.get('key', {}).get('remoteJid', '').split('@')[0]
        
        # Verifica autorizacao
        if not is_authorized(phone_number):
            response = helper_messages.numero_nao_autorizado(phone_number)
            send_whatsapp_message(phone_number, response)
            return jsonify({'status': 'unauthorized'}), 403
        
        # Verifica tipo de mensagem
        message_type = message_data.get('messageType')
        
        if message_type == 'conversation' or message_type == 'extendedTextMessage':
            # Mensagem de texto
            message_text = message_data.get('message', {}).get('conversation', '')
            if not message_text:
                message_text = message_data.get('message', {}).get('extendedTextMessage', {}).get('text', '')
            
            if message_text:
                process_text_message(phone_number, message_text)
        
        elif message_type == 'imageMessage':
            # Mensagem com imagem
            image_message = message_data.get('message', {}).get('imageMessage', {})
            
            # Baixa a imagem (Evolution API fornece URL ou base64)
            image_url = image_message.get('url')
            if image_url:
                response = requests.get(image_url, timeout=30)
                if response.status_code == 200:
                    process_image_message(phone_number, response.content)
        
        return jsonify({'status': 'success'}), 200
    
    except Exception as e:
        print(f"Erro no webhook: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/audit', methods=['POST'])
def run_audit():
    """Endpoint para executar auditoria manual"""
    try:
        # Executa auditoria
        alerts = auditor.run_audit()
        summary = auditor.get_summary()
        
        # Envia resumo para os numeros autorizados
        message = f"Auditoria de {summary['mes_atual']} concluida!\n\n"
        message += f"Total atual: R$ {summary['total_atual']:.2f}\n"
        message += f"Total anterior: R$ {summary['total_anterior']:.2f}\n"
        message += f"Variacao: {summary['variacao_percentual']:.1f}%\n\n"
        message += f"Alertas encontrados: {summary['total_alertas']}\n"
        message += f"- Alta: {summary['alertas_alta']}\n"
        message += f"- Media: {summary['alertas_media']}\n"
        
        for number in AUTHORIZED_NUMBERS:
            send_whatsapp_message(number, message)
        
        return jsonify({
            'status': 'success',
            'summary': summary,
            'alerts': alerts
        }), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'Helper Backend',
        'version': '1.0.0'
    }), 200


if __name__ == '__main__':
    # Garante que a aba do mes atual existe
    sheets_manager.ensure_current_month_exists()
    
    # Inicia o servidor
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

# Made with Bob
