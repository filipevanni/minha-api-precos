from flask import Flask, request, jsonify
import requests, csv, io
import unidecode
import os

app = Flask(__name__)

# =========================================================
# FONTES (CSV) — já preenchidas com seus links publicados
# (você pode sobrescrever com variáveis de ambiente no Render)
# =========================================================
SHEET_CSV_3_DEFAULT = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS4p-Chps89aJJiQP1OtmtPvEppL6xPfkpWkngh7HNDxJZ6SudSWE4M56qMPfn0cedgNqgstt90j2RB/pub?gid=0&single=true&output=csv"
SHEET_CSV_4_DEFAULT = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS4p-Chps89aJJiQP1OtmtPvEppL6xPfkpWkngh7HNDxJZ6SudSWE4M56qMPfn0cedgNqgstt90j2RB/pub?gid=923305865&single=true&output=csv"

SHEET_CSV_3 = os.getenv("SHEET_CSV_3", SHEET_CSV_3_DEFAULT).strip()
SHEET_CSV_4 = os.getenv("SHEET_CSV_4", SHEET_CSV_4_DEFAULT).strip()

FONTE_URLS = [SHEET_CSV_3, SHEET_CSV_4]

# =========================================================
# Normalização
# =========================================================
def norm_nome(txt: str) -> str:
    # minúsculo, sem acento, remove ' de ' solto, normaliza espaços e hífen
    t = unidecode.unidecode(txt.lower())
    t = t.replace(" de ", " ")
    t = t.replace("-", " ")
    t = " ".join(t.split())
    return t

def norm_chave(materiais):
    if isinstance(materiais, str):
        itens = [m.strip() for m in materiais.split(",")]
    else:
        itens = [str(m).strip() for m in materiais]
    itens = [i for i in itens if i]
    norm = [norm_nome(i) for i in itens]
    norm.sort()
    return "+".join(norm)

def parse_preco(valor: str) -> int:
    # aceita "1497", "1.497", "R$ 1.497,00" etc -> só dígitos
    digits = "".join(ch for ch in str(valor) if ch.isdigit())
    return int(digits) if digits else 0

# =========================================================
# Cache em memória (único mapa com todas as abas)
# =========================================================
CACHE = {}  # chave_normalizada -> {"preco": int, "categoria": str}

def carregar_csv(url: str) -> dict:
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    data = r.content.decode("utf-8")
    reader = csv.DictReader(io.StringIO(data))
    mapa = {}
    for row in reader:
        materiais_csv = (row.get("materiais") or "").strip()
        if not materiais_csv:
            continue
        preco = parse_preco(row.get("preco", "0"))
        categoria = (row.get("categoria") or "").strip()
        chave = norm_chave(materiais_csv)
        mapa[chave] = {"preco": preco, "categoria": categoria}
    return mapa

def recarregar_cache():
    global CACHE
    novo = {}
    for url in FONTE_URLS:
        if url:
            try:
                novo.update(carregar_csv(url))
            except Exception as e:
                print(f"[WARN] Falha ao carregar {url}: {e}")
    CACHE = novo
    print(f"[BOOT] Cache carregado: {len(CACHE)} combinações.")

# carrega na inicialização
recarregar_cache()

# =========================================================
# Endpoints
# =========================================================
@app.route("/")
def status():
    return jsonify({
        "ok": True,
        "total_combinacoes": len(CACHE),
        "fontes": FONTE_URLS
    })

@app.route("/reload", methods=["POST"])
def reload():
    # opcional: proteger com token via env (RELOAD_TOKEN)
    token_env = os.getenv("RELOAD_TOKEN", "").strip()
    token_req = (request.args.get("token") or "").strip()
    if token_env and token_req != token_env:
        return jsonify({"erro": "não autorizado"}), 401
    recarregar_cache()
    return jsonify({"ok": True, "total_combinacoes": len(CACHE)})

@app.route("/preco", methods=["GET"])
def preco():
    """
    GET /preco?materiais=CSV
    Ex.: /preco?materiais=Couro Bovino, Couro de Tilápia, Jeans
         /preco?materiais=Couro Bovino, Couro de Tilápia, Couro de Avestruz, Jeans
    Ordem e acentos não importam.
    """
    materiais = (request.args.get("materiais") or "").strip()
    if not materiais:
        return jsonify({"erro": "Materiais não informados"}), 400

    # valida quantidades (opcional, pode remover se quiser aceitar qualquer N)
    itens = [m.strip() for m in materiais.split(",") if m.strip()]
    if len(itens) not in (3, 4):
        return jsonify({
            "erro": "Informe 3 ou 4 materiais",
            "quantidade_recebida": len(itens),
            "materiais_recebidos": itens
        }), 400

    chave = norm_chave(itens)
    r = CACHE.get(chave)
    if r:
        return jsonify({
            "materiais": itens,
            "preco": r["preco"],
            "categoria": r["categoria"]
        })
    return jsonify({
        "erro": "Combinação não encontrada",
        "chave_buscada": chave
    }), 404

if __name__ == "__main__":
    app.run(port=5000)
