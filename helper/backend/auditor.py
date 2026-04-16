# -*- coding: utf-8 -*-
"""
Modulo Auditor - Bater o Mes
Compara gastos do mes atual com o anterior e identifica inconsistencias
"""

from typing import List, Dict, Tuple
from datetime import datetime
import pytz


class Auditor:
    """Auditor de gastos mensais"""
    
    def __init__(self, sheets_manager, alert_threshold: float = 30.0):
        """
        Inicializa o auditor
        
        Args:
            sheets_manager: Instancia do SheetsManager
            alert_threshold: Percentual de aumento para gerar alerta (padrao 30%)
        """
        self.sheets = sheets_manager
        self.alert_threshold = alert_threshold
        self.alerts = []
    
    def run_audit(self) -> List[Dict[str, any]]:
        """
        Executa auditoria completa do mes atual
        
        Returns:
            Lista de alertas encontrados
        """
        self.alerts = []
        
        # Verifica gastos faltantes
        self._check_missing_expenses()
        
        # Verifica aumentos suspeitos
        self._check_suspicious_increases()
        
        # Verifica duplicatas
        self._check_duplicates()
        
        # Verifica dados incompletos
        self._check_incomplete_data()
        
        return self.alerts
    
    def _check_missing_expenses(self):
        """Verifica se gastos recorrentes do mes anterior estao faltando"""
        current_month = self.sheets.get_current_month_name()
        previous_month = self.sheets.get_previous_month_name()
        
        # Pega categorias do mes anterior
        previous_categories = self.sheets.get_categories_from_previous_month()
        
        if not previous_categories:
            return
        
        # Pega categorias do mes atual
        current_expenses = self.sheets.get_all_expenses(current_month)
        current_categories = set()
        
        for expense in current_expenses:
            categoria = expense.get('Categoria', '')
            if categoria:
                current_categories.add(categoria)
        
        # Identifica categorias faltantes
        missing = set(previous_categories) - current_categories
        
        for categoria in missing:
            self.alerts.append({
                'tipo': 'gasto_faltante',
                'categoria': categoria,
                'mes_anterior': previous_month,
                'severidade': 'media'
            })
    
    def _check_suspicious_increases(self):
        """Verifica se alguma categoria aumentou mais que o threshold"""
        current_month = self.sheets.get_current_month_name()
        previous_month = self.sheets.get_previous_month_name()
        
        # Pega totais por categoria de ambos os meses
        current_totals = self.sheets.get_expenses_by_category(current_month)
        previous_totals = self.sheets.get_expenses_by_category(previous_month)
        
        # Compara categorias que existem em ambos os meses
        for categoria, current_value in current_totals.items():
            if categoria in previous_totals:
                previous_value = previous_totals[categoria]
                
                # Calcula percentual de aumento
                if previous_value > 0:
                    increase_percent = ((current_value - previous_value) / previous_value) * 100
                    
                    if increase_percent > self.alert_threshold:
                        self.alerts.append({
                            'tipo': 'aumento_suspeito',
                            'categoria': categoria,
                            'valor_anterior': previous_value,
                            'valor_atual': current_value,
                            'percentual': increase_percent,
                            'severidade': 'alta' if increase_percent > 50 else 'media'
                        })
    
    def _check_duplicates(self):
        """Verifica gastos duplicados no mes atual"""
        current_month = self.sheets.get_current_month_name()
        expenses = self.sheets.get_all_expenses(current_month)
        
        # Agrupa por descricao, valor e data
        seen = {}
        
        for expense in expenses:
            descricao = expense.get('Descricao', '').lower()
            valor_str = str(expense.get('Valor', '0')).replace(',', '.')
            data = expense.get('Data', '')
            
            try:
                valor = float(valor_str)
            except ValueError:
                continue
            
            key = (descricao, valor, data)
            
            if key in seen:
                self.alerts.append({
                    'tipo': 'gasto_duplicado',
                    'descricao': expense.get('Descricao', ''),
                    'valor': valor,
                    'data': data,
                    'severidade': 'alta'
                })
            else:
                seen[key] = True
    
    def _check_incomplete_data(self):
        """Verifica se ha gastos com dados incompletos"""
        current_month = self.sheets.get_current_month_name()
        expenses = self.sheets.get_all_expenses(current_month)
        
        for i, expense in enumerate(expenses, start=2):  # Linha 2 (depois do cabecalho)
            problemas = []
            
            # Verifica data
            data = expense.get('Data', '').strip()
            if not data:
                problemas.append('data')
            
            # Verifica descricao
            descricao = expense.get('Descricao', '').strip()
            if not descricao:
                problemas.append('descricao')
            
            # Verifica valor
            valor_str = str(expense.get('Valor', '')).strip()
            if not valor_str:
                problemas.append('valor')
            else:
                try:
                    valor = float(valor_str.replace(',', '.'))
                    if valor <= 0:
                        problemas.append('valor_invalido')
                except ValueError:
                    problemas.append('valor_invalido')
            
            # Verifica categoria
            categoria = expense.get('Categoria', '').strip()
            if not categoria:
                problemas.append('categoria')
            
            if problemas:
                self.alerts.append({
                    'tipo': 'dados_incompletos',
                    'linha': i,
                    'descricao': descricao if descricao else 'Sem descricao',
                    'campos_faltantes': problemas,
                    'severidade': 'alta' if 'valor' in problemas else 'media'
                })
    
    def get_alerts_by_severity(self, severity: str) -> List[Dict]:
        """
        Retorna alertas filtrados por severidade
        
        Args:
            severity: 'alta', 'media' ou 'baixa'
            
        Returns:
            Lista de alertas da severidade especificada
        """
        return [alert for alert in self.alerts if alert.get('severidade') == severity]
    
    def get_summary(self) -> Dict[str, any]:
        """
        Retorna resumo da auditoria
        
        Returns:
            Dicionario com estatisticas da auditoria
        """
        current_month = self.sheets.get_current_month_name()
        previous_month = self.sheets.get_previous_month_name()
        
        current_total = self.sheets.get_total_expenses(current_month)
        previous_total = self.sheets.get_total_expenses(previous_month)
        
        # Calcula variacao percentual
        if previous_total > 0:
            variation = ((current_total - previous_total) / previous_total) * 100
        else:
            variation = 0
        
        return {
            'mes_atual': current_month,
            'mes_anterior': previous_month,
            'total_atual': current_total,
            'total_anterior': previous_total,
            'variacao_percentual': variation,
            'total_alertas': len(self.alerts),
            'alertas_alta': len(self.get_alerts_by_severity('alta')),
            'alertas_media': len(self.get_alerts_by_severity('media')),
            'alertas_baixa': len(self.get_alerts_by_severity('baixa'))
        }
    
    def check_upcoming_bills(self, days_ahead: int = 7) -> List[Dict]:
        """
        Verifica contas que vencem nos proximos dias
        (Assume que gastos recorrentes tem data similar todo mes)
        
        Args:
            days_ahead: Quantos dias a frente verificar
            
        Returns:
            Lista de contas que podem estar vencendo
        """
        tz = pytz.timezone('America/Sao_Paulo')
        today = datetime.now(tz)
        current_day = today.day
        
        upcoming = []
        
        # Pega gastos do mes anterior
        previous_month = self.sheets.get_previous_month_name()
        previous_expenses = self.sheets.get_all_expenses(previous_month)
        
        # Pega gastos do mes atual
        current_month = self.sheets.get_current_month_name()
        current_expenses = self.sheets.get_all_expenses(current_month)
        
        # Cria set de descricoes ja pagas este mes
        paid_this_month = set()
        for expense in current_expenses:
            descricao = expense.get('Descricao', '').lower()
            paid_this_month.add(descricao)
        
        # Verifica gastos recorrentes do mes anterior
        for expense in previous_expenses:
            descricao = expense.get('Descricao', '')
            descricao_lower = descricao.lower()
            
            # Se ja foi pago este mes, ignora
            if descricao_lower in paid_this_month:
                continue
            
            # Extrai dia do mes anterior
            data_str = expense.get('Data', '')
            if not data_str:
                continue
            
            try:
                # Assume formato DD/MM/YYYY
                day = int(data_str.split('/')[0])
                
                # Verifica se esta dentro do periodo de alerta
                days_until = day - current_day
                
                if 0 <= days_until <= days_ahead:
                    valor_str = str(expense.get('Valor', '0')).replace(',', '.')
                    valor = float(valor_str)
                    
                    upcoming.append({
                        'descricao': descricao,
                        'valor': valor,
                        'dia_vencimento': day,
                        'dias_restantes': days_until,
                        'categoria': expense.get('Categoria', '')
                    })
            
            except (ValueError, IndexError):
                continue
        
        return upcoming

# Made with Bob
