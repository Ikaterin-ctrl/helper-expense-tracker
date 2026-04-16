# -*- coding: utf-8 -*-
"""
Modulo de Processamento de Mensagens
Interpreta mensagens do WhatsApp e extrai informacoes de gastos
"""

import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import pytz


class MessageProcessor:
    """Processador de mensagens de gastos"""
    
    def __init__(self):
        self.tz = pytz.timezone('America/Sao_Paulo')
    
    def parse_message(self, message: str) -> Tuple[List[Dict], Optional[str]]:
        """
        Processa uma mensagem e extrai gastos
        
        Args:
            message: Texto da mensagem
            
        Returns:
            Tupla (lista de gastos, data customizada se houver)
        """
        message = message.strip()
        
        # Verifica se tem data customizada no inicio
        custom_date = self._extract_custom_date(message)
        
        if custom_date:
            # Remove a parte da data da mensagem
            message = re.sub(r'^(ontem|hoje|anteontem|\d{1,2}/\d{1,2}(/\d{2,4})?)[:\s]*', '', message, flags=re.IGNORECASE)
        
        # Extrai gastos da mensagem
        expenses = self._extract_expenses(message)
        
        return expenses, custom_date
    
    def _extract_custom_date(self, message: str) -> Optional[str]:
        """
        Extrai data customizada do inicio da mensagem
        
        Args:
            message: Texto da mensagem
            
        Returns:
            Data no formato DD/MM/YYYY ou None
        """
        message_lower = message.lower().strip()
        now = datetime.now(self.tz)
        
        # Verifica "ontem"
        if message_lower.startswith('ontem'):
            yesterday = now - timedelta(days=1)
            return yesterday.strftime('%d/%m/%Y')
        
        # Verifica "anteontem"
        if message_lower.startswith('anteontem'):
            day_before = now - timedelta(days=2)
            return day_before.strftime('%d/%m/%Y')
        
        # Verifica "hoje" (redundante mas aceita)
        if message_lower.startswith('hoje'):
            return now.strftime('%d/%m/%Y')
        
        # Verifica data no formato DD/MM ou DD/MM/YYYY
        date_match = re.match(r'^(\d{1,2}/\d{1,2}(?:/\d{2,4})?)[:\s]', message)
        if date_match:
            date_str = date_match.group(1)
            
            # Se so tem DD/MM, adiciona o ano atual
            if date_str.count('/') == 1:
                date_str += f'/{now.year}'
            
            # Valida e formata a data
            try:
                parts = date_str.split('/')
                day = int(parts[0])
                month = int(parts[1])
                year = int(parts[2])
                
                # Converte ano de 2 digitos para 4
                if year < 100:
                    year += 2000
                
                # Valida a data
                date_obj = datetime(year, month, day)
                return date_obj.strftime('%d/%m/%Y')
            
            except (ValueError, IndexError):
                pass
        
        return None
    
    def _extract_expenses(self, message: str) -> List[Dict]:
        """
        Extrai gastos da mensagem
        Suporta formatos:
        - "Padaria 20"
        - "Padaria 20, Gasolina 250"
        - "Padaria R$ 20,50"
        
        Args:
            message: Texto da mensagem (sem data)
            
        Returns:
            Lista de gastos extraidos
        """
        expenses = []
        
        # Padrao para encontrar: Descricao Valor
        # Aceita: "Padaria 20", "Padaria R$ 20", "Padaria 20,50", "Padaria R$20.50"
        pattern = r'([A-Za-zÀ-ÿ\s]+?)\s+R?\$?\s*(\d+(?:[.,]\d{2})?)'
        
        # Divide por virgula para processar multiplos gastos
        parts = message.split(',')
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            match = re.search(pattern, part, re.IGNORECASE)
            
            if match:
                descricao = match.group(1).strip()
                valor_str = match.group(2).replace(',', '.')
                
                try:
                    valor = float(valor_str)
                    
                    if valor > 0 and descricao:
                        expenses.append({
                            'descricao': descricao.title(),
                            'valor': valor,
                            'categoria': self._guess_category(descricao)
                        })
                
                except ValueError:
                    continue
        
        return expenses
    
    def _guess_category(self, descricao: str) -> str:
        """
        Tenta adivinhar a categoria baseado na descricao
        
        Args:
            descricao: Descricao do gasto
            
        Returns:
            Categoria sugerida
        """
        descricao_lower = descricao.lower()
        
        # Dicionario de palavras-chave por categoria
        categorias = {
            'Alimentacao': ['mercado', 'supermercado', 'padaria', 'restaurante', 
                           'lanche', 'comida', 'bebida', 'cafe', 'bar', 'pizza',
                           'hamburger', 'sushi', 'churrasco', 'delivery', 'ifood'],
            'Transporte': ['gasolina', 'combustivel', 'uber', 'taxi', 'onibus', 
                          'metro', 'estacionamento', 'pedagio', 'carro', 'moto',
                          'mecanico', 'oficina', '99', 'app'],
            'Saude': ['farmacia', 'remedio', 'medicamento', 'medico', 'consulta', 
                     'exame', 'hospital', 'clinica', 'dentista', 'laboratorio'],
            'Moradia': ['aluguel', 'condominio', 'luz', 'agua', 'gas', 'internet', 
                       'telefone', 'energia', 'iptu', 'seguro'],
            'Lazer': ['cinema', 'teatro', 'show', 'ingresso', 'streaming', 
                     'netflix', 'spotify', 'jogo', 'parque', 'viagem', 'hotel'],
            'Vestuario': ['roupa', 'calcado', 'sapato', 'tenis', 'camisa', 
                         'calca', 'vestido', 'loja', 'shopping'],
            'Educacao': ['livro', 'curso', 'escola', 'faculdade', 'material', 
                        'apostila', 'mensalidade', 'matricula'],
            'Beleza': ['salao', 'cabelo', 'manicure', 'estetica', 'cosmetico', 
                      'perfume', 'barbeiro', 'spa'],
            'Pets': ['veterinario', 'racao', 'pet', 'cachorro', 'gato', 'animal'],
            'Servicos': ['lavanderia', 'conserto', 'reparo', 'manutencao', 'limpeza']
        }
        
        # Procura palavras-chave na descricao
        for categoria, palavras in categorias.items():
            for palavra in palavras:
                if palavra in descricao_lower:
                    return categoria
        
        # Se nao encontrar, retorna categoria generica
        return 'Outros'
    
    def validate_expense(self, expense: Dict) -> Tuple[bool, Optional[str]]:
        """
        Valida se um gasto tem todos os dados necessarios
        
        Args:
            expense: Dicionario com dados do gasto
            
        Returns:
            Tupla (valido, mensagem de erro)
        """
        # Verifica descricao
        if not expense.get('descricao'):
            return False, 'descricao'
        
        # Verifica valor
        valor = expense.get('valor')
        if valor is None or valor <= 0:
            return False, 'valor'
        
        # Categoria e opcional, mas se nao tiver, adiciona "Outros"
        if not expense.get('categoria'):
            expense['categoria'] = 'Outros'
        
        return True, None
    
    def format_date(self, custom_date: Optional[str] = None) -> str:
        """
        Formata data para o padrao DD/MM/YYYY
        
        Args:
            custom_date: Data customizada ou None para usar hoje
            
        Returns:
            Data formatada
        """
        if custom_date:
            return custom_date
        
        now = datetime.now(self.tz)
        return now.strftime('%d/%m/%Y')
    
    def is_help_request(self, message: str) -> bool:
        """
        Verifica se a mensagem e um pedido de ajuda
        
        Args:
            message: Texto da mensagem
            
        Returns:
            True se for pedido de ajuda
        """
        help_keywords = ['ajuda', 'help', 'como usar', 'comandos', 'oi', 'ola', 'menu']
        message_lower = message.lower().strip()
        
        return any(keyword in message_lower for keyword in help_keywords)

# Made with Bob
