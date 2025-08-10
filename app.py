import os
import requests
import csv
import io
from flask import Flask, request, jsonify
import unidecode

app = Flask(__name__)

# =========================
# Normalização
# =========================
def _norm_nome(txt: str) -> str:
    """Remove acentos, deixa minúsculo, tira 'de' isolado, normaliza hífen e espaços"""
    t = unidecode.unidecode(txt.lower())
    t = t.replace(" de ", " ")
    t = t.replace("-", " ")
    t = " ".join(t.split())
    return t

def chave_normalizada(materiais) -> str:
    """
    Aceita string CSV ou lista, normaliza cada item e ordena.
    Retorna 'a+b+c...'
    """
    if isinstance(materiais, str):
        itens = [p.strip() for p in materiais.split(",") if p.strip()]
    else:
        itens = [str(p).strip() for p in materiais if str(p).strip()]
    norm = [_norm_nome(p) for p in itens]
    norm.sort()
    return "+".join(norm)

# =========================
# Cache das combinações
# =========================
CACHE = {}  # chave normalizada -> {"preco": int, "categoria": str}

# URLs do Google Sheets via variáveis de ambiente
FONTE_URL_1 = os.getenv("FONTE_URL_1")  # exemplo: planilha de 3 materiais
FONTE_URL_2 = os.getenv("FONTE_URL_2")  # exemplo: planilha de 4 materiais

def carregar_dados():
    """Carrega todas as combinações das planilhas no cache"""
    global CACHE
    CACHE.clear()
    fontes = [FONTE_URL_1, FONTE_URL_2]
    
    for url in fontes:
        if not url:
            continue
        # Troca /pubhtml? por /pub?output=csv para ler como CSV
        csv_url = url.replace("/pubhtml?", "/pub?output=csv&")
        resp = requests.get(csv_url)
        resp.raise_for_status()

        f = io.StringIO(resp.text)
        reader = csv.DictReader(f)
        for row in reader:
            materiais_str = row.get("materiais", "")
            preco_str = row.get("preco", "0")
            categoria = row.get("categoria", "")

            if not materiais_str or not preco_str:
                continue

            key = chave_normalizada(materiais_str)
            CACHE[key] = {
                "preco": int(preco_str),
                "categoria": categoria
            }

# =========================
# Rotas
# =========================
@app.route("/")
def home():
    return jsonify({"status": "API de preços ativa", "total_combinacoes": len(CACHE)})

@app.route("/preco", methods=["GET"])
def preco():
    materiais = request.args.get("materiais")
    if not materiais:
        return jsonify({"erro": "Materiais não informados"}), 400

    key = chave_normalizada(materiais)
    dados = CACHE.get(key)

    if not dados:
        return jsonify({
            "erro": "Combinação não encontrada",
            "chave_buscada": key
        }), 404

    return jsonify({
        "materiais": [m.strip() for m in materiais.split(",")],
        "preco": dados["preco"],
        "categoria": dados["categoria"]
    })

# =========================
# Inicialização
# =========================
if __name__ == "__main__":
    carregar_dados()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    carregar_dados()
