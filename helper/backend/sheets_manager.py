# -*- coding: utf-8 -*-
"""
Modulo de Gerenciamento do Google Sheets
Responsavel por criar abas, ler/escrever dados e manter a estrutura da planilha
"""

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
from typing import List, Dict, Optional
import pytz


class SheetsManager:
    """Gerenciador de operacoes no Google Sheets"""
    
    # Cabecalho padrao das abas mensais
    HEADER = ['Data', 'Descricao', 'Categoria', 'Valor', 'Forma_Pagamento', 'Observacoes']
    
    def __init__(self, credentials_file: str, spreadsheet_id: str):
        """
        Inicializa o gerenciador de planilhas
        
        Args:
            credentials_file: Caminho para o arquivo JSON de credenciais
            spreadsheet_id: ID da planilha do Google Sheets
        """
        self.credentials_file = credentials_file
        self.spreadsheet_id = spreadsheet_id
        self.client = None
        self.spreadsheet = None
        self._connect()
    
    def _connect(self):
        """Estabelece conexao com Google Sheets"""
        try:
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            creds = Credentials.from_service_account_file(
                self.credentials_file,
                scopes=scopes
            )
            
            self.client = gspread.authorize(creds)
            self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            
        except Exception as e:
            raise Exception(f"Erro ao conectar com Google Sheets: {str(e)}")
    
    def get_current_month_name(self) -> str:
        """Retorna o nome da aba do mes atual (ex: Abril_2026)"""
        tz = pytz.timezone('America/Sao_Paulo')
        now = datetime.now(tz)
        meses = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Marco', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        return f"{meses[now.month]}_{now.year}"
    
    def get_previous_month_name(self) -> str:
        """Retorna o nome da aba do mes anterior"""
        tz = pytz.timezone('America/Sao_Paulo')
        now = datetime.now(tz)
        
        mes = now.month - 1
        ano = now.year
        
        if mes == 0:
            mes = 12
            ano -= 1
        
        meses = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Marco', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        return f"{meses[mes]}_{ano}"
    
    def sheet_exists(self, sheet_name: str) -> bool:
        """Verifica se uma aba existe"""
        try:
            self.spreadsheet.worksheet(sheet_name)
            return True
        except gspread.exceptions.WorksheetNotFound:
            return False
    
    def create_month_sheet(self, sheet_name: Optional[str] = None) -> str:
        """
        Cria uma nova aba mensal com o cabecalho padrao
        
        Args:
            sheet_name: Nome da aba (se None, usa mes atual)
            
        Returns:
            Nome da aba criada
        """
        if sheet_name is None:
            sheet_name = self.get_current_month_name()
        
        if self.sheet_exists(sheet_name):
            return sheet_name
        
        # Cria a aba
        worksheet = self.spreadsheet.add_worksheet(
            title=sheet_name,
            rows=1000,
            cols=len(self.HEADER)
        )
        
        # Adiciona cabecalho
        worksheet.append_row(self.HEADER)
        
        # Formata cabecalho (negrito)
        worksheet.format('A1:F1', {
            'textFormat': {'bold': True},
            'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
        })
        
        return sheet_name
    
    def ensure_current_month_exists(self) -> str:
        """Garante que a aba do mes atual existe"""
        month_name = self.get_current_month_name()
        if not self.sheet_exists(month_name):
            self.create_month_sheet(month_name)
        return month_name
    
    def add_expense(self, data: str, descricao: str, categoria: str, 
                    valor: float, forma_pagamento: str = '', 
                    observacoes: str = '', sheet_name: Optional[str] = None) -> bool:
        """
        Adiciona um gasto na planilha
        
        Args:
            data: Data do gasto (formato DD/MM/YYYY)
            descricao: Descricao do gasto
            categoria: Categoria do gasto
            valor: Valor do gasto
            forma_pagamento: Forma de pagamento (opcional)
            observacoes: Observacoes adicionais (opcional)
            sheet_name: Nome da aba (se None, usa mes atual)
            
        Returns:
            True se sucesso, False caso contrario
        """
        try:
            if sheet_name is None:
                sheet_name = self.ensure_current_month_exists()
            
            worksheet = self.spreadsheet.worksheet(sheet_name)
            
            # Formata valor com 2 casas decimais
            valor_formatado = f"{valor:.2f}"
            
            row = [data, descricao, categoria, valor_formatado, forma_pagamento, observacoes]
            worksheet.append_row(row)
            
            return True
            
        except Exception as e:
            print(f"Erro ao adicionar gasto: {str(e)}")
            return False
    
    def get_all_expenses(self, sheet_name: Optional[str] = None) -> List[Dict]:
        """
        Retorna todos os gastos de uma aba
        
        Args:
            sheet_name: Nome da aba (se None, usa mes atual)
            
        Returns:
            Lista de dicionarios com os gastos
        """
        try:
            if sheet_name is None:
                sheet_name = self.get_current_month_name()
            
            if not self.sheet_exists(sheet_name):
                return []
            
            worksheet = self.spreadsheet.worksheet(sheet_name)
            records = worksheet.get_all_records()
            
            return records
            
        except Exception as e:
            print(f"Erro ao buscar gastos: {str(e)}")
            return []
    
    def get_expenses_by_category(self, sheet_name: Optional[str] = None) -> Dict[str, float]:
        """
        Retorna o total de gastos por categoria
        
        Args:
            sheet_name: Nome da aba (se None, usa mes atual)
            
        Returns:
            Dicionario com categoria: total
        """
        expenses = self.get_all_expenses(sheet_name)
        
        totals = {}
        for expense in expenses:
            categoria = expense.get('Categoria', 'Sem Categoria')
            valor_str = str(expense.get('Valor', '0')).replace(',', '.')
            
            try:
                valor = float(valor_str)
            except ValueError:
                valor = 0.0
            
            if categoria in totals:
                totals[categoria] += valor
            else:
                totals[categoria] = valor
        
        return totals
    
    def get_total_expenses(self, sheet_name: Optional[str] = None) -> float:
        """
        Retorna o total de gastos de uma aba
        
        Args:
            sheet_name: Nome da aba (se None, usa mes atual)
            
        Returns:
            Total de gastos
        """
        expenses = self.get_all_expenses(sheet_name)
        
        total = 0.0
        for expense in expenses:
            valor_str = str(expense.get('Valor', '0')).replace(',', '.')
            try:
                total += float(valor_str)
            except ValueError:
                continue
        
        return total
    
    def check_duplicate(self, descricao: str, valor: float, data: str, 
                       sheet_name: Optional[str] = None) -> bool:
        """
        Verifica se existe um gasto duplicado
        
        Args:
            descricao: Descricao do gasto
            valor: Valor do gasto
            data: Data do gasto
            sheet_name: Nome da aba (se None, usa mes atual)
            
        Returns:
            True se encontrar duplicata, False caso contrario
        """
        expenses = self.get_all_expenses(sheet_name)
        
        for expense in expenses:
            if (expense.get('Descricao', '').lower() == descricao.lower() and
                expense.get('Data', '') == data):
                
                valor_str = str(expense.get('Valor', '0')).replace(',', '.')
                try:
                    valor_existente = float(valor_str)
                    if abs(valor_existente - valor) < 0.01:  # Tolerancia de 1 centavo
                        return True
                except ValueError:
                    continue
        
        return False
    
    def get_categories_from_previous_month(self) -> List[str]:
        """
        Retorna lista de categorias unicas do mes anterior
        
        Returns:
            Lista de categorias
        """
        previous_month = self.get_previous_month_name()
        
        if not self.sheet_exists(previous_month):
            return []
        
        expenses = self.get_all_expenses(previous_month)
        categories = set()
        
        for expense in expenses:
            categoria = expense.get('Categoria', '')
            if categoria:
                categories.add(categoria)
        
        return list(categories)

# Made with Bob
