from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import unidecode
import os
from typing import Dict, List

app = Flask(__name__)

# --------------------------------------------------
# 1) LISTA DAS ABAS PUBLICADAS (adicione novas aqui)
#    Você pode também usar variáveis de ambiente:
#    FONTE_URLS="url1;url2;url3"
# --------------------------------------------------
FONTE_URLS: List[str] = [
    # 3 materiais (gid=0)
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vS4p-Chps89aJJiQP1OtmtPvEppL6xPfkpWkngh7HNDxJZ6SudSWE4M56qMPfn0cedgNqgstt90j2RB/pubhtml?gid=0&single=true",
    # 4 materiais (gid=923305865)
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vS4p-Chps89aJJiQP1OtmtPvEppL6xPfkpWkngh7HNDxJZ6SudSWE4M56qMPfn0cedgNqgstt90j2RB/pubhtml?gid=923305865&single=true",
]
_env_urls = os.getenv("FONTE_URLS", "").strip()
if _env_urls:
    # permite sobrescrever pelos envs da Render (se quiser)
    FONTE_URLS = [u.strip() for u in _env_urls.split(";") if u.strip()]

# --------------------------------------------------
# 2) NORMALIZAÇÃO
#    - remove acentos
#    - minúsculas
#    - remove " de " (apenas como palavra)
#    - troca hífen por espaço
#    - colapsa espaços
#    - ordena alfabeticamente
# --------------------------------------------------
def normaliza_nome(material: str) -> str:
    txt = unidecode.unidecode(material.lower())
    txt = txt.replace(" de ", " ")
    txt = txt.replace("-", " ")
    txt = " ".join(txt.split())
    return txt

def normaliza_lista(materiais) -> str:
    if isinstance(materiais, str):
        materiais = [m.strip() for m in materiais.split(",")]
    norm = [normaliza_nome(m) for m in materiais if m.strip()]
    norm.sort()
    return "+".join(norm)

# --------------------------------------------------
# 3) EXTRATOR DO GOOGLE SHEETS (publicado em HTML)
#    Espera colunas:
#      materiais | preco | categoria
# --------------------------------------------------
def extrair_dados_google_sheets(url: str) -> Dict[str, Dict]:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # a versão "pubhtml" rende tabelas <table> com linhas <tr>
    table = soup.find("table")
    if not table:
        return {}

    rows = table.find_all("tr")
    if not rows:
        return {}

    # cabeçalhos
    headers = [(" ".join(td.get_text(strip=True).split())).lower() for td in rows[0].find_all(["td", "th"])]

    # mapeia índices das colunas
    def idx(nome: str):
        for i, h in enumerate(headers):
            if nome in h:  # tolerante: "materiais", "preco", "categoria"
                return i
        return None

    i_mat = idx("materiais")
    i_pre = idx("preco")
    i_cat = idx("categoria")

    if i_mat is None or i_pre is None or i_cat is None:
        return {}

    resultado = {}
    for tr in rows[1:]:
        tds = tr.find_all("td")
        if len(tds) <= max(i_mat, i_pre, i_cat):
            continue

        materiais_raw = tds[i_mat].get_text(strip=True)
        preco_raw = tds[i_pre].get_text(strip=True).replace("R$", "").replace(".", "").replace(",", "").strip()
        cat_raw = tds[i_cat].get_text(strip=True)

        if not materiais_raw:
            continue

        # cria chave normalizada
        chave = normaliza_lista(materiais_raw)
        if not chave:
            continue

        # converte preço para int com tolerância
        preco = None
        try:
            preco = int(preco_raw)
        except Exception:
            # tenta encontrar números dentro do texto
            digits = "".join([c for c in preco_raw if c.isdigit()])
            if digits:
                try:
                    preco = int(digits)
                except Exception:
                    pass

        if preco is None:
            continue

        resultado[chave] = {
            "preco": preco,
            "categoria": cat_raw or "",
        }

    return resultado

# --------------------------------------------------
# 4) CACHE EM MEMÓRIA (carregado na inicialização)
# --------------------------------------------------
CACHE: Dict[str, Dict] = {}

def carregar_cache():
    global CACHE
    CACHE = {}
    for url in FONTE_URLS:
        try:
            dados = extrair_dados_google_sheets(url)
            CACHE.update(dados)
        except Exception as e:
            # não derruba a app se uma aba falhar
            print(f"[WARN] Falha ao carregar {url}: {e}")

# carrega ao iniciar
carregar_cache()

# --------------------------------------------------
# 5) ENDPOINTS
# --------------------------------------------------
@app.route("/preco", methods=["GET"])
def preco():
    materiais = request.args.get("materiais")
    if not materiais:
        return jsonify({"erro": "Materiais não informados"}), 400

    chave = normaliza_lista(materiais)
    resultado = CACHE.get(chave)

    if resultado:
        return jsonify({
            "materiais": [m.strip() for m in materiais.split(",")],
            "preco": resultado["preco"],
            "categoria": resultado["categoria"]
        })
    else:
        return jsonify({
            "erro": "Combinação não encontrada",
            "chave_buscada": chave
        }), 404

@app.route("/reload", methods=["POST"])
def reload_cache():
    # opcional: recarrega manualmente sem reiniciar o serviço
    carregar_cache()
    return jsonify({"status": "ok", "itens": len(CACHE)})

@app.route("/")
def raiz():
    return jsonify({"status": "ok", "itens_cache": len(CACHE)})

# --------------------------------------------------
# 6) DEV LOCAL
# --------------------------------------------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)
