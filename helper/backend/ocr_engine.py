# -*- coding: utf-8 -*-
"""
Modulo de OCR (Optical Character Recognition)
Processa imagens de recibos e notas fiscais para extrair dados de gastos
Usa Tesseract OCR (gratuito)
"""

import pytesseract
from PIL import Image
import re
from typing import List, Dict, Optional
import io


class OCREngine:
    """Motor de processamento de imagens para extrair dados de gastos"""
    
    def __init__(self, tesseract_path: Optional[str] = None):
        """
        Inicializa o motor OCR
        
        Args:
            tesseract_path: Caminho para o executavel do Tesseract (Windows)
        """
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    def process_image(self, image_data: bytes) -> str:
        """
        Processa uma imagem e extrai o texto
        
        Args:
            image_data: Dados binarios da imagem
            
        Returns:
            Texto extraido da imagem
        """
        try:
            # Abre a imagem
            image = Image.open(io.BytesIO(image_data))
            
            # Converte para escala de cinza para melhor reconhecimento
            image = image.convert('L')
            
            # Extrai texto usando Tesseract
            text = pytesseract.image_to_string(image, lang='por')
            
            return text
            
        except Exception as e:
            raise Exception(f"Erro ao processar imagem: {str(e)}")
    
    def extract_expenses(self, text: str) -> List[Dict[str, any]]:
        """
        Extrai informacoes de gastos do texto OCR
        
        Args:
            text: Texto extraido da imagem
            
        Returns:
            Lista de dicionarios com os gastos encontrados
        """
        expenses = []
        
        # Padrao para encontrar valores monetarios
        # Exemplos: R$ 10,50 | 10,50 | R$10.50 | 10.50
        money_pattern = r'R?\$?\s*(\d+[.,]\d{2})'
        
        # Padrao para encontrar descricoes (palavras antes do valor)
        # Busca linhas que contem valor monetario
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Procura valores na linha
            matches = re.finditer(money_pattern, line, re.IGNORECASE)
            
            for match in matches:
                valor_str = match.group(1).replace(',', '.')
                
                try:
                    valor = float(valor_str)
                    
                    # Pega o texto antes do valor como descricao
                    descricao = line[:match.start()].strip()
                    
                    # Remove caracteres especiais da descricao
                    descricao = re.sub(r'[^\w\s]', '', descricao)
                    
                    # Se a descricao for muito curta, tenta pegar mais contexto
                    if len(descricao) < 3:
                        descricao = 'Item'
                    
                    # Limita tamanho da descricao
                    if len(descricao) > 50:
                        descricao = descricao[:50]
                    
                    # Adiciona o gasto se tiver descricao e valor valido
                    if descricao and valor > 0:
                        expenses.append({
                            'descricao': descricao.title(),
                            'valor': valor,
                            'categoria': self._guess_category(descricao)
                        })
                
                except ValueError:
                    continue
        
        # Remove duplicatas (mesmo valor e descricao)
        unique_expenses = []
        seen = set()
        
        for expense in expenses:
            key = (expense['descricao'], expense['valor'])
            if key not in seen:
                seen.add(key)
                unique_expenses.append(expense)
        
        return unique_expenses
    
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
                           'lanche', 'comida', 'bebida', 'cafe', 'bar'],
            'Transporte': ['gasolina', 'combustivel', 'uber', 'taxi', 'onibus', 
                          'metro', 'estacionamento', 'pedagio'],
            'Saude': ['farmacia', 'remedio', 'medicamento', 'medico', 'consulta', 
                     'exame', 'hospital', 'clinica'],
            'Moradia': ['aluguel', 'condominio', 'luz', 'agua', 'gas', 'internet', 
                       'telefone', 'energia'],
            'Lazer': ['cinema', 'teatro', 'show', 'ingresso', 'streaming', 
                     'netflix', 'spotify', 'jogo'],
            'Vestuario': ['roupa', 'calcado', 'sapato', 'tenis', 'camisa', 
                         'calca', 'vestido'],
            'Educacao': ['livro', 'curso', 'escola', 'faculdade', 'material', 
                        'apostila'],
            'Beleza': ['salao', 'cabelo', 'manicure', 'estetica', 'cosmetico', 
                      'perfume']
        }
        
        # Procura palavras-chave na descricao
        for categoria, palavras in categorias.items():
            for palavra in palavras:
                if palavra in descricao_lower:
                    return categoria
        
        # Se nao encontrar, retorna categoria generica
        return 'Outros'
    
    def extract_total(self, text: str) -> Optional[float]:
        """
        Tenta extrair o valor total do recibo
        
        Args:
            text: Texto extraido da imagem
            
        Returns:
            Valor total encontrado ou None
        """
        # Procura por linhas com "total", "valor total", etc
        total_pattern = r'(?:total|valor\s+total|subtotal)[\s:]*R?\$?\s*(\d+[.,]\d{2})'
        
        matches = re.finditer(total_pattern, text, re.IGNORECASE)
        
        totals = []
        for match in matches:
            valor_str = match.group(1).replace(',', '.')
            try:
                totals.append(float(valor_str))
            except ValueError:
                continue
        
        # Retorna o maior valor encontrado (provavelmente o total)
        return max(totals) if totals else None
    
    def validate_receipt(self, text: str) -> bool:
        """
        Valida se o texto parece ser de um recibo/nota fiscal
        
        Args:
            text: Texto extraido da imagem
            
        Returns:
            True se parecer um recibo valido
        """
        # Palavras-chave que indicam um recibo
        keywords = ['total', 'subtotal', 'valor', 'cupom', 'nota', 'fiscal', 
                   'cnpj', 'cpf', 'data', 'pagamento']
        
        text_lower = text.lower()
        
        # Conta quantas palavras-chave foram encontradas
        found = sum(1 for keyword in keywords if keyword in text_lower)
        
        # Verifica se tem pelo menos 2 palavras-chave e algum valor monetario
        has_money = bool(re.search(r'R?\$?\s*\d+[.,]\d{2}', text))
        
        return found >= 2 and has_money

# Made with Bob
