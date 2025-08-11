from flask import Flask, request, jsonify
import csv
import io
import os
import re
import requests
import unidecode

app = Flask(__name__)

# ----------------------------
# Normalização de materiais
# ----------------------------
def normaliza_nome(material: str) -> str:
    if material is None:
        return ""
    txt = unidecode.unidecode(material.lower())
    # remove " de " como palavra solta
    txt = re.sub(r"\bde\b", " ", txt)
    # troca hífen por espaço e colapsa espaços
    txt = txt.replace("-", " ")
    txt = " ".join(txt.split())
    return txt

def chave_normalizada(materiais):
    """
    Aceita string CSV (ex.: "A, B, C") ou lista ["A","B","C"].
    Normaliza cada item e ORDENA para que a chave seja estável.
    """
    if isinstance(materiais, str):
        partes = [p.strip() for p in materiais.split(",") if p.strip()]
    else:
        partes = [str(p).strip() for p in materiais if str(p).strip()]
    norm = [normaliza_nome(p) for p in partes]
    norm = [n for n in norm if n]  # remove vazios
    norm.sort()
    return "+".join(norm)

# ----------------------------
# Utilidades de planilha
# ----------------------------
def to_csv_url(url: str) -> str:
    """
    Converte pubhtml -> CSV automaticamente.
    Aceita já CSV também.
    """
    if not url:
        return url
    # já é CSV?
    if "output=csv" in url:
        return url
    # pubhtml?...gid=XXX&single=true  -> pub?gid=XXX&single=true&output=csv
    if "/pubhtml" in url:
        url = url.replace("/pubhtml", "/pub")
        if "output=csv" not in url:
            sep = "&" if "?" in url else "?"
            url = f"{url}{sep}output=csv"
    return url

def parse_preco(v):
    """
    Converte '1.997', '1997', '1.997,00' -> int(1997)
    """
    if v is None:
        return None
    s = str(v).strip()
    if not s:
        return None
    # tira pontos de milhar
    s = s.replace(".", "")
    # vírgula decimal -> ponto
    s = s.replace(",", ".")
    try:
        return int(round(float(s)))
    except Exception:
        return None

# ----------------------------
# Cache: chave_normalizada -> {preco, categoria}
# ----------------------------
CACHE = {}

def carregar_dados():
    """
    Lê FONTE_URL_1..FONTE_URL_5, faz download (CSV),
    e popula o CACHE com chaves normalizadas.
    Requer pelo menos 1 fonte.
    """
    global CACHE
    CACHE.clear()

    fontes = []
    for i in range(1, 6):
        u = os.getenv(f"FONTE_URL_{i}")
        if u:
            fontes.append(u)

    if not fontes:
        app.logger.warning("Nenhuma FONTE_URL_n definida. Defina FONTE_URL_1 (e 2..5 se quiser).")
        return

    total_linhas = 0
    total_ativas = 0

    for raw_url in fontes:
        url = to_csv_url(raw_url)
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            app.logger.error(f"Erro ao baixar planilha: {url} -> {e}")
            continue

        # lê CSV
        try:
            content = resp.content.decode("utf-8", errors="ignore")
            reader = csv.DictReader(io.StringIO(content))
        except Exception as e:
            app.logger.error(f"Erro ao ler CSV de {url}: {e}")
            continue

        for row in reader:
            total_linhas += 1
            # nomes das colunas esperadas
            materiais_raw = row.get("materiais") or row.get("Materiais") or row.get("MATERIAIS")
            preco_raw = row.get("preco") or row.get("Preço") or row.get("preco (R$)")
            categoria = row.get("categoria") or row.get("Categoria")
            ativo = row.get("ativo") or row.get("Ativo")

            # se houver coluna 'ativo' e ela não for TRUE, ignora
            if ativo is not None and str(ativo).strip().upper() != "TRUE":
                continue

            if not materiais_raw:
                continue

            chave = chave_normalizada(materiais_raw)
            if not chave:
                continue

            preco = parse_preco(preco_raw)
            if preco is None:
                # sem preço válido, ignora
                continue

            total_ativas += 1
            CACHE[chave] = {
                "preco": preco,
                "categoria": str(categoria).strip() if categoria is not None else ""
            }

    app.logger.info(f"Planilhas carregadas. Linhas lidas: {total_linhas}, registradas: {total_ativas}, chaves no cache: {len(CACHE)}")

# carrega na inicialização
carregar_dados()

# ----------------------------
# Endpoints
# ----------------------------
@app.route("/health")
def health():
    return jsonify({"ok": True, "itens_cache": len(CACHE)})

@app.route("/preco")
def preco():
    """
    GET /preco?materiais=A,B,C[,D...]
    Retorna {materiais: [...], preco, categoria} ou 404 com chave_buscada.
    """
    materiais = request.args.get("materiais", "").strip()
    if not materiais:
        return jsonify({"erro": "Materiais não informados"}), 400

    chave = chave_normalizada(materiais)
    resultado = CACHE.get(chave)

    if resultado:
        # ecoa materiais como lista "bonita" (cada item strip)
        lista = [m.strip() for m in materiais.split(",") if m.strip()]
        return jsonify({
            "materiais": lista,
            "preco": resultado["preco"],
            "categoria": resultado.get("categoria", "")
        })
    else:
        return jsonify({
            "erro": "Combinação não encontrada",
            "chave_buscada": chave
        }), 404

if __name__ == "__main__":
    # Para rodar local: python app.py
    app.run(host="0.0.0.0", port=5000)
