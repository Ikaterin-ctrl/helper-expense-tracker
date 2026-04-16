# -*- coding: utf-8 -*-
"""
Modulo de Mensagens do Helper
Personalidade: Assistente esdruxulo dos anos 2000 - excessivamente feliz mas sarcastico
"""

import random
from datetime import datetime


class HelperMessages:
    """Gerador de mensagens com personalidade esdruxula"""
    
    # Mapeamento de contextos para moods
    MOOD_MAP = {
        'gasto_registrado': 'standard',
        'multiplos_gastos': 'standard',
        'dados_incompletos': 'confused',
        'conta_vencendo': 'alert',
        'gasto_faltando': 'alert',
        'aumento_suspeito': 'angry',
        'gasto_duplicado': 'angry',
        'ocr_sucesso': 'standard',
        'ocr_falha': 'confused',
        'auditoria_ok': 'standard',
        'auditoria_problemas': 'angry',
        'erro': 'confused'
    }
    
    @staticmethod
    def gasto_registrado(valor, descricao):
        """Mensagem ao registrar um gasto com sucesso"""
        mensagens = [
            f"Surpresa! Anotei seu gasto de R$ {valor:.2f} com {descricao}. Mais um tijolinho no muro das contas!",
            f"Eba! R$ {valor:.2f} em {descricao} devidamente registrado. O dinheiro voa, mas eu anoto tudo!",
            f"Maravilha! Gastou R$ {valor:.2f} com {descricao}. Estou aqui pra isso mesmo, anotar cada centavo que escapa!",
            f"Que alegria! R$ {valor:.2f} em {descricao} ja esta na planilha. Adoro ver o dinheiro indo embora... ops, digo, adoro organizar!",
            f"Registrado! R$ {valor:.2f} com {descricao}. Continua assim que logo a gente chega no vermelho... digo, no azul!"
        ]
        return random.choice(mensagens)
    
    @staticmethod
    def gasto_registrado_com_mood(valor, descricao):
        """Retorna mensagem e mood para gasto registrado"""
        return (HelperMessages.gasto_registrado(valor, descricao), 'standard')
    
    @staticmethod
    def multiplos_gastos_registrados(quantidade, total):
        """Mensagem ao registrar multiplos gastos de uma vez"""
        mensagens = [
            f"Uau! {quantidade} gastos de uma vez so! Total de R$ {total:.2f}. Voce e eficiente em gastar, hein?",
            f"Que produtividade! {quantidade} gastos registrados, somando R$ {total:.2f}. Meus parabens pela dedicacao em esvaziar a carteira!",
            f"Caramba! {quantidade} gastos num piscar de olhos! R$ {total:.2f} voaram. Mas relaxa, eu anotei tudo direitinho!",
            f"Impressionante! {quantidade} gastos (R$ {total:.2f}) registrados. Voce esta treinando pra maratona de compras?"
        ]
        return random.choice(mensagens)
    
    @staticmethod
    def dados_incompletos(campo_faltante):
        """Mensagem quando faltam dados obrigatorios"""
        mensagens = {
            'valor': [
                "Opa! Cadê o valor? Eu sou bom, mas não sou vidente! Me diz quanto gastou, vai?",
                "Ei! Faltou o valor aqui. Gastou quanto? Zero? Duvido! Me conta a verdade!",
                "Hmm... sem valor não rola. Quanto foi? Pode falar, eu não julgo... muito."
            ],
            'descricao': [
                "E ai? Gastou com o que? Preciso de uma descricao, nem que seja 'coisa'!",
                "Faltou me dizer o que foi. Gastou com ar? Luz? Agua? Me ajuda aqui!",
                "Descricao, por favor! Eu anoto tudo, mas preciso saber o que e esse 'tudo'!"
            ],
            'data': [
                "Quando foi isso? Hoje? Ontem? No seculo passado? Me da uma data!",
                "Faltou a data! Foi hoje? Se nao me disser, vou assumir que foi agora mesmo!",
                "Data, meu caro! Quando aconteceu esse gasto misterioso?"
            ]
        }
        return random.choice(mensagens.get(campo_faltante, ["Faltou alguma informacao importante! Revisa ai!"]))
    
    @staticmethod
    def conta_vencendo(descricao, valor, dias):
        """Alerta de conta proxima do vencimento"""
        if dias == 0:
            return f"ALERTA VERMELHO! A conta de {descricao} (R$ {valor:.2f}) vence HOJE! Corre!"
        elif dias == 1:
            return f"ATENCAO! A conta de {descricao} (R$ {valor:.2f}) vence AMANHA! Nao esquece!"
        else:
            return f"Lembrete amigavel: {descricao} (R$ {valor:.2f}) vence em {dias} dias. Ja separa o dinheiro!"
    
    @staticmethod
    def gasto_faltando(categoria, mes_anterior):
        """Alerta quando um gasto recorrente nao foi lancado"""
        mensagens = [
            f"Ei! Cadê o gasto de {categoria} deste mes? No mes passado voce lancou. Esqueceu ou ta sobrando dinheiro?",
            f"Opa! {categoria} sumiu da lista este mes. Mes passado tinha. Virou milionario ou so esqueceu de anotar?",
            f"Hmm... {categoria} apareceu em {mes_anterior} mas nao este mes. Explica isso ai!",
            f"Alerta! {categoria} esta ausente. Mes passado voce gastou com isso. O que houve?"
        ]
        return random.choice(mensagens)
    
    @staticmethod
    def aumento_suspeito(categoria, valor_anterior, valor_atual, percentual):
        """Alerta quando uma categoria aumentou mais de 30%"""
        mensagens = [
            f"EITAAAA! {categoria} subiu {percentual:.1f}%! Era R$ {valor_anterior:.2f}, agora e R$ {valor_atual:.2f}. Explica isso!",
            f"Calma la! {categoria} deu um pulo de {percentual:.1f}% (de R$ {valor_anterior:.2f} pra R$ {valor_atual:.2f}). Ta tudo bem?",
            f"ALERTA! {categoria} aumentou {percentual:.1f}%! Mes passado: R$ {valor_anterior:.2f}. Agora: R$ {valor_atual:.2f}. Que isso?",
            f"Opa opa! {categoria} disparou {percentual:.1f}%! De R$ {valor_anterior:.2f} pra R$ {valor_atual:.2f}. Aconteceu algo?"
        ]
        return random.choice(mensagens)
    
    @staticmethod
    def gasto_duplicado(descricao, valor, data):
        """Alerta de possivel gasto duplicado"""
        return f"Perai! Ja vi esse gasto de {descricao} (R$ {valor:.2f}) em {data}. Lancou duas vezes ou gastou de novo?"
    
    @staticmethod
    def ocr_sucesso(itens_encontrados):
        """Mensagem quando OCR processa imagem com sucesso"""
        mensagens = [
            f"Beleza! Li a imagem e encontrei {itens_encontrados} item(ns). Vou registrar tudo!",
            f"Imagem processada! Achei {itens_encontrados} gasto(s) aqui. Deixa comigo!",
            f"Pronto! Sua imagem revelou {itens_encontrados} item(ns). Anotando tudo!"
        ]
        return random.choice(mensagens)
    
    @staticmethod
    def ocr_falha():
        """Mensagem quando OCR falha"""
        mensagens = [
            "Ops! Nao consegui ler essa imagem. Ela ta muito borrada ou eu to precisando de oculos?",
            "Hmm... essa imagem ta dificil de ler. Tenta tirar outra foto mais clara?",
            "Nao deu certo! A imagem ta muito escura ou confusa. Manda outra?"
        ]
        return random.choice(mensagens)
    
    @staticmethod
    def auditoria_iniciada(mes):
        """Mensagem ao iniciar auditoria mensal"""
        return f"Bom dia! Vou bater o mes de {mes}. Preparado pra verdade nua e crua?"
    
    @staticmethod
    def auditoria_concluida(alertas_encontrados):
        """Mensagem ao concluir auditoria"""
        if alertas_encontrados == 0:
            mensagens = [
                "Auditoria concluida! Tudo certinho, nenhum alerta. Voce e um exemplo!",
                "Pronto! Revisei tudo e esta impecavel. Parabens pela organizacao!",
                "Auditoria finalizada! Zero alertas. Continua assim!"
            ]
        else:
            mensagens = [
                f"Auditoria concluida! Encontrei {alertas_encontrados} alerta(s). Vamos resolver?",
                f"Terminei a revisao! {alertas_encontrados} coisa(s) precisam de atencao.",
                f"Pronto! {alertas_encontrados} alerta(s) encontrado(s). Bora acertar isso!"
            ]
        return random.choice(mensagens)
    
    @staticmethod
    def aba_criada(mes):
        """Mensagem ao criar nova aba mensal"""
        return f"Opa! Criei a aba de {mes} pra voce. Mes novo, gastos novos. Vamos la!"
    
    @staticmethod
    def numero_nao_autorizado(numero):
        """Mensagem para numero nao autorizado"""
        return f"Desculpa, mas o numero {numero} nao esta autorizado. Eu so atendo a Catarina, Flavio e o Pai!"
    
    @staticmethod
    def erro_generico():
        """Mensagem de erro generico"""
        mensagens = [
            "Eita! Deu algum problema aqui. Tenta de novo?",
            "Ops! Algo deu errado. Nao foi culpa sua... acho.",
            "Hmm... erro inesperado. Vamos tentar novamente?"
        ]
        return random.choice(mensagens)
    
    @staticmethod
    def ajuda():
        """Mensagem de ajuda"""
        return """Oi! Sou o Helper, seu assistente de gastos esdruxulo!

Como usar:
- Manda "Padaria 20" pra registrar um gasto
- Ou varios de uma vez: "Padaria 20, Gasolina 250, Farmacia 80"
- Manda foto do recibo que eu leio pra voce
- Comeca com "Ontem" pra gastos retroativos
- Eu te aviso de contas vencendo e gastos suspeitos

Exemplos:
"Supermercado 150"
"Ontem: Cinema 40"
"Aluguel 1200, Luz 180, Agua 90"

Qualquer duvida, so chamar!"""

# Made with Bob
