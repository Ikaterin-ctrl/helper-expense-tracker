# -*- coding: utf-8 -*-
"""
Helper Widget - Interface Windows
Notificacoes de contas a vencer e alertas de auditoria
"""

import customtkinter as ctk
from plyer import notification
from PIL import Image, ImageTk
import sys
import os
from datetime import datetime
import threading
import time
import requests
from typing import List, Dict, Optional

# Adiciona o diretorio backend ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'config', '.env'))

from sheets_manager import SheetsManager
from auditor import Auditor

# Configuracoes
GOOGLE_CREDENTIALS = os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
CHECK_INTERVAL = int(os.getenv('WIDGET_CHECK_INTERVAL_MINUTES', '30')) * 60
POSITION_X = int(os.getenv('WIDGET_POSITION_X', '100'))
POSITION_Y = int(os.getenv('WIDGET_POSITION_Y', '100'))

# Mapeamento de moods para imagens
MOOD_IMAGES = {
    'standard': 'helper_standard.png',
    'alert': 'helper_alert.png',
    'angry': 'helper_angry.png',
    'confused': 'helper_confused.png'
}


class HelperWidget(ctk.CTk):
    """Widget de notificacoes do Helper"""
    
    def __init__(self):
        super().__init__()
        
        # Configuracoes da janela
        self.title("Helper - Assistente de Gastos")
        self.geometry(f"400x500+{POSITION_X}+{POSITION_Y}")
        
        # Tema escuro
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Diretorio de assets
        self.assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
        
        # Cache de imagens carregadas
        self.mood_images_cache = {}
        self.load_mood_images()
        
        # Inicializa componentes
        try:
            self.sheets_manager = SheetsManager(GOOGLE_CREDENTIALS, SPREADSHEET_ID)
            self.auditor = Auditor(self.sheets_manager)
        except Exception as e:
            self.show_error(f"Erro ao conectar: {str(e)}")
            return
        
        # Estado
        self.alerts_shown = set()
        self.is_checking = False
        self.current_mood = 'standard'
        
        # Cria interface
        self.create_widgets()
        
        # Inicia verificacao automatica
        self.start_auto_check()
    
    def load_mood_images(self):
        """Carrega todas as imagens de mood no cache"""
        for mood, filename in MOOD_IMAGES.items():
            image_path = os.path.join(self.assets_dir, filename)
            try:
                if os.path.exists(image_path):
                    # Carrega e redimensiona imagem
                    pil_image = Image.open(image_path)
                    pil_image = pil_image.resize((64, 64), Image.Resampling.LANCZOS)
                    self.mood_images_cache[mood] = ctk.CTkImage(
                        light_image=pil_image,
                        dark_image=pil_image,
                        size=(64, 64)
                    )
                else:
                    print(f"Aviso: Imagem {filename} nao encontrada em {self.assets_dir}")
            except Exception as e:
                print(f"Erro ao carregar imagem {filename}: {str(e)}")
    
    def get_mood_image(self, mood: str = 'standard') -> Optional[ctk.CTkImage]:
        """
        Retorna a imagem do mood especificado
        Usa fallback para 'standard' se o mood nao existir
        """
        if mood in self.mood_images_cache:
            return self.mood_images_cache[mood]
        elif 'standard' in self.mood_images_cache:
            return self.mood_images_cache['standard']
        return None
    
    def set_mood(self, mood: str):
        """Atualiza o mood atual e a imagem do header"""
        self.current_mood = mood
        if hasattr(self, 'mood_image_label'):
            image = self.get_mood_image(mood)
            if image:
                self.mood_image_label.configure(image=image)
    
    def create_widgets(self):
        """Cria os widgets da interface"""
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        # Imagem do Helper (mood)
        mood_image = self.get_mood_image('standard')
        if mood_image:
            self.mood_image_label = ctk.CTkLabel(
                header_frame,
                image=mood_image,
                text=""
            )
            self.mood_image_label.pack(pady=(0, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Helper",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Seu assistente esdruxulo de gastos",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        subtitle_label.pack()
        
        # Area de alertas
        alerts_label = ctk.CTkLabel(
            self,
            text="Alertas e Notificacoes",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        alerts_label.pack(pady=(10, 5))
        
        # Frame scrollavel para alertas
        self.alerts_frame = ctk.CTkScrollableFrame(self, height=250)
        self.alerts_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Botoes
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=10)
        
        self.check_button = ctk.CTkButton(
            buttons_frame,
            text="Verificar Agora",
            command=self.check_now,
            height=40
        )
        self.check_button.pack(side="left", expand=True, padx=5)
        
        self.audit_button = ctk.CTkButton(
            buttons_frame,
            text="Auditar Mes",
            command=self.run_audit,
            height=40,
            fg_color="orange",
            hover_color="darkorange"
        )
        self.audit_button.pack(side="left", expand=True, padx=5)
        
        # Status
        self.status_label = ctk.CTkLabel(
            self,
            text="Pronto para verificar",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.status_label.pack(pady=5)
    
    def clear_alerts(self):
        """Limpa a area de alertas"""
        for widget in self.alerts_frame.winfo_children():
            widget.destroy()
    
    def add_alert(self, title: str, message: str, severity: str = "info", mood: str = "standard"):
        """Adiciona um alerta na interface com mood especifico"""
        # Define cores por severidade
        colors = {
            "alta": ("red", "darkred"),
            "media": ("orange", "darkorange"),
            "baixa": ("yellow", "gold"),
            "info": ("blue", "darkblue")
        }
        
        color, hover_color = colors.get(severity, colors["info"])
        
        # Atualiza mood do Helper
        self.set_mood(mood)
        
        # Frame do alerta
        alert_frame = ctk.CTkFrame(self.alerts_frame, fg_color=color)
        alert_frame.pack(fill="x", pady=5)
        
        # Titulo
        title_label = ctk.CTkLabel(
            alert_frame,
            text=title,
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        title_label.pack(fill="x", padx=10, pady=(10, 5))
        
        # Mensagem
        message_label = ctk.CTkLabel(
            alert_frame,
            text=message,
            font=ctk.CTkFont(size=11),
            anchor="w",
            wraplength=350
        )
        message_label.pack(fill="x", padx=10, pady=(0, 10))
    
    def check_now(self):
        """Verifica alertas manualmente"""
        if self.is_checking:
            return
        
        self.is_checking = True
        self.check_button.configure(state="disabled", text="Verificando...")
        self.status_label.configure(text="Verificando alertas...")
        
        # Executa em thread separada
        thread = threading.Thread(target=self._check_alerts)
        thread.daemon = True
        thread.start()
    
    def _check_alerts(self):
        """Verifica alertas (executa em thread)"""
        try:
            # Limpa alertas anteriores
            self.after(0, self.clear_alerts)
            
            # Verifica contas a vencer
            upcoming_bills = self.auditor.check_upcoming_bills(days_ahead=7)
            
            for bill in upcoming_bills:
                dias = bill['dias_restantes']
                severity = "alta" if dias <= 1 else "media"
                mood = "alert"  # Contas vencendo = alerta
                
                title = f"Conta Vencendo: {bill['descricao']}"
                message = f"R$ {bill['valor']:.2f} - Vence em {dias} dia(s)"
                
                self.after(0, lambda t=title, m=message, s=severity, mo=mood: self.add_alert(t, m, s, mo))
                
                # Notificacao do sistema
                if dias <= 1:
                    alert_key = f"bill_{bill['descricao']}_{bill['dia_vencimento']}"
                    if alert_key not in self.alerts_shown:
                        self.show_notification(title, message, mood)
                        self.alerts_shown.add(alert_key)
            
            # Verifica alertas de auditoria
            alerts = self.auditor.run_audit()
            
            for alert in alerts:
                if alert['tipo'] == 'gasto_faltante':
                    title = f"Gasto Faltante: {alert['categoria']}"
                    message = f"Presente em {alert['mes_anterior']}, ausente este mes"
                    mood = "alert"  # Gasto faltando = alerta
                    self.after(0, lambda t=title, m=message, s=alert['severidade'], mo=mood: self.add_alert(t, m, s, mo))
                
                elif alert['tipo'] == 'aumento_suspeito':
                    title = f"Aumento Suspeito: {alert['categoria']}"
                    message = f"Subiu {alert['percentual']:.1f}% (R$ {alert['valor_anterior']:.2f} -> R$ {alert['valor_atual']:.2f})"
                    mood = "angry"  # Aumento >30% = irritado
                    self.after(0, lambda t=title, m=message, s=alert['severidade'], mo=mood: self.add_alert(t, m, s, mo))
                
                elif alert['tipo'] == 'gasto_duplicado':
                    title = "Gasto Duplicado"
                    message = f"{alert['descricao']} - R$ {alert['valor']:.2f} em {alert['data']}"
                    mood = "angry"  # Duplicata = irritado
                    self.after(0, lambda t=title, m=message, s=alert['severidade'], mo=mood: self.add_alert(t, m, s, mo))
                
                elif alert['tipo'] == 'dados_incompletos':
                    title = f"Dados Incompletos (Linha {alert['linha']})"
                    campos = ', '.join(alert['campos_faltantes'])
                    message = f"{alert['descricao']} - Faltam: {campos}"
                    mood = "confused"  # Dados faltando = confuso
                    self.after(0, lambda t=title, m=message, s=alert['severidade'], mo=mood: self.add_alert(t, m, s, mo))
            
            # Se nao houver alertas
            if not upcoming_bills and not alerts:
                self.after(0, lambda: self.add_alert(
                    "Tudo Certo!",
                    "Nenhum alerta encontrado. Continue assim!",
                    "info",
                    "standard"  # Tudo OK = feliz
                ))
            
            # Atualiza status
            total_alerts = len(upcoming_bills) + len(alerts)
            status_text = f"Ultima verificacao: {datetime.now().strftime('%H:%M:%S')} - {total_alerts} alerta(s)"
            self.after(0, lambda: self.status_label.configure(text=status_text))
        
        except Exception as e:
            self.after(0, lambda: self.show_error(f"Erro ao verificar: {str(e)}"))
        
        finally:
            self.is_checking = False
            self.after(0, lambda: self.check_button.configure(state="normal", text="Verificar Agora"))
    
    def run_audit(self):
        """Executa auditoria completa"""
        self.audit_button.configure(state="disabled", text="Auditando...")
        
        thread = threading.Thread(target=self._run_audit)
        thread.daemon = True
        thread.start()
    
    def _run_audit(self):
        """Executa auditoria (em thread)"""
        try:
            summary = self.auditor.get_summary()
            
            title = f"Auditoria de {summary['mes_atual']}"
            message = f"Total: R$ {summary['total_atual']:.2f}\n"
            message += f"Variacao: {summary['variacao_percentual']:.1f}%\n"
            message += f"Alertas: {summary['total_alertas']}"
            
            # Define mood baseado no resultado da auditoria
            if summary['total_alertas'] == 0:
                mood = "standard"  # Tudo OK
            elif summary['alertas_alta'] > 0:
                mood = "angry"  # Problemas críticos
            else:
                mood = "alert"  # Alertas médios
            
            self.after(0, lambda: self.add_alert(title, message, "info", mood))
            self.show_notification(title, message, mood)
            
            # Verifica alertas
            self._check_alerts()
        
        except Exception as e:
            self.after(0, lambda: self.show_error(f"Erro na auditoria: {str(e)}"))
        
        finally:
            self.after(0, lambda: self.audit_button.configure(state="normal", text="Auditar Mes"))
    
    def show_notification(self, title: str, message: str, mood: str = "standard"):
        """Mostra notificacao do sistema com mood"""
        try:
            # Atualiza mood antes de notificar
            self.set_mood(mood)
            
            notification.notify(
                title=title,
                message=message,
                app_name="Helper",
                timeout=10
            )
        except Exception as e:
            print(f"Erro ao mostrar notificacao: {str(e)}")
    
    def show_error(self, message: str):
        """Mostra mensagem de erro"""
        self.add_alert("Erro", message, "alta", "confused")
        self.status_label.configure(text="Erro na ultima verificacao")
    
    def start_auto_check(self):
        """Inicia verificacao automatica periodica"""
        def auto_check_loop():
            while True:
                time.sleep(CHECK_INTERVAL)
                if not self.is_checking:
                    self.after(0, self.check_now)
        
        thread = threading.Thread(target=auto_check_loop)
        thread.daemon = True
        thread.start()
        
        # Primeira verificacao
        self.after(2000, self.check_now)


def main():
    """Funcao principal"""
    try:
        app = HelperWidget()
        app.mainloop()
    except Exception as e:
        print(f"Erro fatal: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

# Made with Bob
