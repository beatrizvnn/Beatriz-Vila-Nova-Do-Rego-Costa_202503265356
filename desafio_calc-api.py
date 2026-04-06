"""
Projeto: Calculadora API com FastAPI
Disciplina: RAD - Python
Integrantes:
- Esther Vila Nova do Rêgo Costa - 202502412371
- Beatriz Vila Nova do Rêgo Costa - 202503265356

Data: Março de 2026
"""

from fastapi import FastAPI

# Cria a API
app = FastAPI()

# O decorador @app.get define:
# 1. O métod0 HTTP (GET): Indica que os dados virão visíveis por meio da URL
# 2. A rota ("/"): É o endereço final que o usuário vai acessar no navegador
@app.get("/")

# Recebe dois números e a operação desejada via URL e depois retorna o cálculo
def calcular_resultado(a: float, b: float, tipo: str):
    # Definindo os tipos (float, str) nos parâmetros acima, o FastAPI faz 3 coisas:
    # 1. Puxa esses valores da URL
    # 2. Converte de texto (padrão da URL) para número (float)
    # 3. Bloqueia a requisição e avisa o usuário se ele digitar outra coisa no lugar do número ou esquecer um campo

    # Lógica da calculadora. Usa listas para aceitar acentuação e padroniza as respostas com .lower() para que os inputs sejam lidos em lowercase
    if tipo.lower() == "soma":
        resultado = a + b
    elif tipo.lower() in ["subtração", "subtracao"]:
        resultado = a - b
    elif tipo.lower() in ["multiplicação", "multiplicacao"]:
        resultado = a * b
    elif tipo.lower() in ["divisão", "divisao"]:
        if a == 0:
             # Prevenção contra o erro de divisão por zero
             return {"erro": "Não é possível dividir por zero."}
        resultado = a / b
    else:
        # Tratamento caso o usuário escreva algo fora das 4 opções esperadas na URL
        return {"erro": "Operação inválida."}

    # O FastAPI pega este dicionário e transforma automaticamente em um JSON para o usuário ler
    return {
        "a": a,
        "b": b,
        "resultado": resultado
    }