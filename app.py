from flask import Flask, request, jsonify

app = Flask(__name__)

COMBINACOES = {
    "Couro Bovino+Couro de Tilápia+Jeans": {"preco": 1497, "categoria": 
"Casual Urbano"},
    "Couro Bovino+Couro de Avestruz+Jeans": {"preco": 1667, "categoria": 
"Casual Urbano"},
    "Couro Bovino+Couro de Jacaré+Jeans": {"preco": 1767, "categoria": 
"Casual Urbano"},
    "Couro Bovino+Couro de Pirarucu+Jeans": {"preco": 1767, "categoria": 
"Casual Urbano"},
    "Couro Bovino+Couro de Coelho+Jeans": {"preco": 1837, "categoria": 
"Casual Urbano"},
    "Couro de Tilápia+Couro de Avestruz+Jeans": {"preco": 1837, 
"categoria": "Casual Urbano"},
    "Couro de Jacaré+Couro de Tilápia+Jeans": {"preco": 1937, "categoria": 
"Casual Urbano"},
    "Couro de Tilápia+Couro de Pirarucu+Jeans": {"preco": 1937, 
"categoria": "Casual Urbano"},
    "Couro Bovino+Couro de Tilápia+Couro de Avestruz": {"preco": 1997, 
"categoria": "Couro Premium"},
    "Couro Bovino+Couro de Python+Jeans": {"preco": 1997, "categoria": 
"Casual Urbano"},
    "Couro de Tilápia+Couro de Coelho+Jeans": {"preco": 1997, "categoria": 
"Casual Urbano"},
    "Couro de Avestruz+Couro de Pirarucu+Jeans": {"preco": 2097, 
"categoria": "Casual Urbano"},
    "Couro de Jacaré+Couro de Avestruz+Jeans": {"preco": 2097, 
"categoria": "Casual Urbano"},
    "Couro Bovino+Couro de Tilápia+Couro de Pirarucu": {"preco": 2097, 
"categoria": "Couro Premium"},
    "Couro Bovino+Couro de Jacaré+Couro de Tilápia": {"preco": 2097, 
"categoria": "Couro Premium"},
    "Couro de Tilápia+Couro de Python+Jeans": {"preco": 2167, "categoria": 
"Casual Urbano"},
    "Couro Bovino+Couro de Tilápia+Couro de Coelho": {"preco": 2167, 
"categoria": "Couro Premium"},
    "Couro de Coelho+Couro de Avestruz+Jeans": {"preco": 2167, 
"categoria": "Casual Urbano"},
    "Couro de Jacaré+Couro de Pirarucu+Jeans": {"preco": 2197, 
"categoria": "Casual Urbano"},
    "Couro Bovino+Couro de Jacaré+Couro de Avestruz": {"preco": 2267, 
"categoria": "Couro Premium"},
    "Couro de Jacaré+Couro de Coelho+Jeans": {"preco": 2267, "categoria": 
"Casual Urbano"},
    "Couro de Coelho+Couro de Pirarucu+Jeans": {"preco": 2267, 
"categoria": "Casual Urbano"},
    "Couro Bovino+Couro de Avestruz+Couro de Pirarucu": {"preco": 2267, 
"categoria": "Couro Premium"},
    "Couro de Avestruz+Couro de Python+Jeans": {"preco": 2337, 
"categoria": "Casual Urbano"},
    "Couro Bovino+Couro de Coelho+Couro de Avestruz": {"preco": 2337, 
"categoria": "Couro Premium"},
    "Couro Bovino+Couro de Tilápia+Couro de Python": {"preco": 2337, 
"categoria": "Couro Premium"},
    "Couro Bovino+Couro de Jacaré+Couro de Pirarucu": {"preco": 2367, 
"categoria": "Couro Premium"},
    "Couro de Jacaré+Couro de Python+Jeans": {"preco": 2437, "categoria": 
"Casual Urbano"},
    "Couro Bovino+Couro de Jacaré+Couro de Coelho": {"preco": 2437, 
"categoria": "Couro Premium"},
    "Couro de Pirarucu+Couro de Python+Jeans": {"preco": 2437, 
"categoria": "Casual Urbano"},
    "Couro Bovino+Couro de Coelho+Couro de Pirarucu": {"preco": 2437, 
"categoria": "Couro Premium"},
    "Couro de Jacaré+Couro de Tilápia+Couro de Avestruz": {"preco": 2437, 
"categoria": "Couro Premium"},
    "Couro de Tilápia+Couro de Avestruz+Couro de Pirarucu": {"preco": 
2437, "categoria": "Couro Premium"},
    "Couro Bovino+Couro de Avestruz+Couro de Python": {"preco": 2497, 
"categoria": "Couro Premium"},
    "Couro de Coelho+Couro de Python+Jeans": {"preco": 2497, "categoria": 
"Casual Urbano"},
    "Couro de Tilápia+Couro de Coelho+Couro de Avestruz": {"preco": 2497, 
"categoria": "Couro Premium"},
    "Couro de Jacaré+Couro de Tilápia+Couro de Pirarucu": {"preco": 2537, 
"categoria": "Couro Premium"},
    "Couro de Tilápia+Couro de Coelho+Couro de Pirarucu": {"preco": 2597, 
"categoria": "Couro Premium"},
    "Couro Bovino+Couro de Jacaré+Couro de Python": {"preco": 2597, 
"categoria": "Couro Premium"},
    "Couro de Jacaré+Couro de Tilápia+Couro de Coelho": {"preco": 2597, 
"categoria": "Couro Premium"},
    "Couro Bovino+Couro de Pirarucu+Couro de Python": {"preco": 2597, 
"categoria": "Couro Premium"},
    "Couro Bovino+Couro de Coelho+Couro de Python": {"preco": 2667, 
"categoria": "Couro Premium"},
    "Couro de Tilápia+Couro de Avestruz+Couro de Python": {"preco": 2667, 
"categoria": "Couro Premium"},
    "Couro de Jacaré+Couro de Avestruz+Couro de Pirarucu": {"preco": 2697, 
"categoria": "Couro Premium"},
    "Couro de Jacaré+Couro de Coelho+Couro de Avestruz": {"preco": 2767, 
"categoria": "Couro Premium"},
    "Couro de Coelho+Couro de Avestruz+Couro de Pirarucu": {"preco": 2767, 
"categoria": "Couro Premium"},
    "Couro de Tilápia+Couro de Pirarucu+Couro de Python": {"preco": 2767, 
"categoria": "Couro Premium"},
    "Couro de Jacaré+Couro de Tilápia+Couro de Python": {"preco": 2767, 
"categoria": "Couro Premium"},
    "Couro de Tilápia+Couro de Coelho+Couro de Python": {"preco": 2837, 
"categoria": "Couro Premium"},
    "Couro de Jacaré+Couro de Coelho+Couro de Pirarucu": {"preco": 2867, 
"categoria": "Couro Premium"},
    "Couro de Avestruz+Couro de Pirarucu+Couro de Python": {"preco": 2937, 
"categoria": "Couro Premium"},
    "Couro de Jacaré+Couro de Avestruz+Couro de Python": {"preco": 2937, 
"categoria": "Couro Premium"},
    "Couro de Coelho+Couro de Avestruz+Couro de Python": {"preco": 2997, 
"categoria": "Couro Premium"},
    "Couro de Jacaré+Couro de Pirarucu+Couro de Python": {"preco": 3037, 
"categoria": "Couro Premium"},
    "Couro de Coelho+Couro de Pirarucu+Couro de Python": {"preco": 3097, 
"categoria": "Couro Premium"},
    "Couro de Jacaré+Couro de Coelho+Couro de Python": {"preco": 3097, 
"categoria": "Couro Premium"},
}

def normaliza(materiais):
    return "+".join(sorted([m.strip() for m in materiais]))

@app.route("/preco", methods=["GET"])
def preco():
    materiais = request.args.get("materiais")
    if not materiais:
        return jsonify({"erro": "Materiais não informados"}), 400

    lista_materiais = [m.strip() for m in materiais.split(",")]
    chave = normaliza(lista_materiais)
    resultado = COMBINACOES.get(chave)

    if resultado:
        return jsonify({
            "materiais": lista_materiais,
            "preco": resultado["preco"],
            "categoria": resultado["categoria"]
        })
    else:
        return jsonify({"erro": "Combinação não encontrada"}), 404

if __name__ == "__main__":
    app.run(port=5000)

