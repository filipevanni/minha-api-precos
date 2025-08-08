from flask import Flask, request, jsonify
import unidecode

app = Flask(__name__)

COMBINACOES = {
    "couro avestruz+couro bovino+couro tilapia": {"preco": 1997, 
"categoria": "Couro Premium"},
    "couro avestruz+couro bovino+jeans": {"preco": 1667, "categoria": 
"Casual Urbano"},
    "couro avestruz+couro bovino+couro coelho": {"preco": 2337, 
"categoria": "Couro Premium"},
    "couro avestruz+couro bovino+couro pirarucu": {"preco": 2267, 
"categoria": "Couro Premium"},
    "couro avestruz+couro bovino+couro python": {"preco": 2497, 
"categoria": "Couro Premium"},
    "couro avestruz+couro bovino+couro jacare": {"preco": 2267, 
"categoria": "Couro Premium"},
    "couro avestruz+couro coelho+jeans": {"preco": 2167, "categoria": 
"Casual Urbano"},
    "couro avestruz+couro coelho+couro pirarucu": {"preco": 2767, 
"categoria": "Couro Premium"},
    "couro avestruz+couro coelho+couro python": {"preco": 2997, 
"categoria": "Couro Premium"},
    "couro avestruz+couro jacare+couro pirarucu": {"preco": 2697, 
"categoria": "Couro Premium"},
    "couro avestruz+couro jacare+jeans": {"preco": 2097, "categoria": 
"Casual Urbano"},
    "couro avestruz+couro jacare+couro python": {"preco": 2937, 
"categoria": "Couro Premium"},
    "couro avestruz+couro tilapia+jeans": {"preco": 1837, "categoria": 
"Casual Urbano"},
    "couro avestruz+couro tilapia+couro coelho": {"preco": 2497, 
"categoria": "Couro Premium"},
    "couro avestruz+couro tilapia+couro pirarucu": {"preco": 2437, 
"categoria": "Couro Premium"},
    "couro avestruz+couro tilapia+couro python": {"preco": 2667, 
"categoria": "Couro Premium"},
    "couro avestruz+jeans+couro pirarucu": {"preco": 2097, "categoria": 
"Casual Urbano"},
    "couro avestruz+jeans+couro python": {"preco": 2337, "categoria": 
"Casual Urbano"},
    "couro bovino+couro coelho+couro jacare": {"preco": 2437, "categoria": 
"Couro Premium"},
    "couro bovino+couro coelho+couro pirarucu": {"preco": 2437, 
"categoria": "Couro Premium"},
    "couro bovino+couro coelho+couro python": {"preco": 2667, "categoria": 
"Couro Premium"},
    "couro bovino+couro jacare+couro coelho": {"preco": 2437, "categoria": 
"Couro Premium"},
    "couro bovino+couro jacare+couro pirarucu": {"preco": 2367, 
"categoria": "Couro Premium"},
    "couro bovino+couro jacare+couro python": {"preco": 2597, "categoria": 
"Couro Premium"},
    "couro bovino+couro jacare+couro tilapia": {"preco": 2097, 
"categoria": "Couro Premium"},
    "couro bovino+couro pirarucu+couro python": {"preco": 2597, 
"categoria": "Couro Premium"},
    "couro bovino+couro tilapia+couro coelho": {"preco": 2167, 
"categoria": "Couro Premium"},
    "couro bovino+couro tilapia+couro pirarucu": {"preco": 2097, 
"categoria": "Couro Premium"},
    "couro bovino+couro tilapia+couro python": {"preco": 2337, 
"categoria": "Couro Premium"},
    "couro bovino+jeans+couro coelho": {"preco": 1837, "categoria": 
"Casual Urbano"},
    "couro bovino+jeans+couro jacare": {"preco": 1767, "categoria": 
"Casual Urbano"},
    "couro bovino+jeans+couro pirarucu": {"preco": 1767, "categoria": 
"Casual Urbano"},
    "couro bovino+jeans+couro python": {"preco": 1997, "categoria": 
"Casual Urbano"},
    "couro bovino+jeans+couro tilapia": {"preco": 1497, "categoria": 
"Casual Urbano"},
    "couro coelho+couro jacare+jeans": {"preco": 2267, "categoria": 
"Casual Urbano"},
    "couro coelho+couro jacare+couro pirarucu": {"preco": 2867, 
"categoria": "Couro Premium"},
    "couro coelho+couro jacare+couro python": {"preco": 3097, "categoria": 
"Couro Premium"},
    "couro coelho+couro pirarucu+jeans": {"preco": 2267, "categoria": 
"Casual Urbano"},
    "couro coelho+couro pirarucu+couro python": {"preco": 3097, 
"categoria": "Couro Premium"},
    "couro coelho+couro python+jeans": {"preco": 2497, "categoria": 
"Casual Urbano"},
    "couro jacare+couro pirarucu+jeans": {"preco": 2197, "categoria": 
"Casual Urbano"},
    "couro jacare+couro pirarucu+couro python": {"preco": 3037, 
"categoria": "Couro Premium"},
    "couro jacare+couro python+jeans": {"preco": 2437, "categoria": 
"Casual Urbano"},
    "couro jacare+couro tilapia+jeans": {"preco": 1937, "categoria": 
"Casual Urbano"},
    "couro jacare+couro tilapia+couro avestruz": {"preco": 2437, 
"categoria": "Couro Premium"},
    "couro jacare+couro tilapia+couro coelho": {"preco": 2597, 
"categoria": "Couro Premium"},
    "couro jacare+couro tilapia+couro pirarucu": {"preco": 2537, 
"categoria": "Couro Premium"},
    "couro jacare+couro tilapia+couro python": {"preco": 2767, 
"categoria": "Couro Premium"},
    "couro jacare+jeans+couro pirarucu": {"preco": 2197, "categoria": 
"Casual Urbano"},
    "couro jacare+jeans+couro python": {"preco": 2437, "categoria": 
"Casual Urbano"},
    "couro pirarucu+couro python+jeans": {"preco": 2437, "categoria": 
"Casual Urbano"},
    "couro tilapia+couro avestruz+couro coelho": {"preco": 2497, 
"categoria": "Couro Premium"},
    "couro tilapia+couro avestruz+couro pirarucu": {"preco": 2437, 
"categoria": "Couro Premium"},
    "couro tilapia+couro avestruz+couro python": {"preco": 2667, 
"categoria": "Couro Premium"},
    "couro tilapia+couro coelho+couro pirarucu": {"preco": 2597, 
"categoria": "Couro Premium"},
    "couro tilapia+couro coelho+couro python": {"preco": 2837, 
"categoria": "Couro Premium"},
    "couro tilapia+couro jacare+couro avestruz": {"preco": 2437, 
"categoria": "Couro Premium"},
    "couro tilapia+couro jacare+couro coelho": {"preco": 2597, 
"categoria": "Couro Premium"},
    "couro tilapia+couro jacare+couro pirarucu": {"preco": 2537, 
"categoria": "Couro Premium"},
    "couro tilapia+couro jacare+couro python": {"preco": 2767, 
"categoria": "Couro Premium"},
    "couro tilapia+jeans+couro coelho": {"preco": 1997, "categoria": 
"Casual Urbano"},
    "couro tilapia+jeans+couro pirarucu": {"preco": 1937, "categoria": 
"Casual Urbano"},
    "couro tilapia+jeans+couro python": {"preco": 2167, "categoria": 
"Casual Urbano"},
    "couro tilapia+jeans+couro avestruz": {"preco": 1837, "categoria": 
"Casual Urbano"},
    "jeans+couro pirarucu+couro python": {"preco": 2437, "categoria": 
"Casual Urbano"},
}


def normaliza_nome(material):
    material = unidecode.unidecode(material.lower())
    material = material.replace("de ", "")
    material = material.replace("-", " ")
    material = " ".join(material.split())
    return material

def normaliza_lista(materiais):
    if isinstance(materiais, str):
        materiais = [m.strip() for m in materiais.split(",")]
    norm = [normaliza_nome(m) for m in materiais]
    norm.sort()
    return "+".join(norm)

@app.route("/preco", methods=["GET"])
def preco():
    materiais = request.args.get("materiais")
    if not materiais:
        return jsonify({"erro": "Materiais não informados"}), 400

    chave = normaliza_lista(materiais)
    resultado = COMBINACOES.get(chave)

    if resultado:
        return jsonify({
            "materiais": materiais,
            "preco": resultado["preco"],
            "categoria": resultado["categoria"]
        })
    else:
        return jsonify({"erro": "Combinação não encontrada", 
"chave_buscada": chave}), 404

if __name__ == "__main__":
    app.run(port=5000)



