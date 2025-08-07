from flask import Flask, request, jsonify

app = Flask(__name__)

COMBINACOES = {
    "Couro Avestruz+Couro Bovino+Couro Tilápia": {"preco": 1997, 
"categoria": "Couro Premium"},
    "Couro Avestruz+Couro Bovino+Jeans": {"preco": 1667, "categoria": 
"Casual Urbano"},
    "Couro Avestruz+Couro Bovino+Couro Coelho": {"preco": 2337, 
"categoria": "Couro Premium"},
    "Couro Avestruz+Couro Bovino+Couro Pirarucu": {"preco": 2267, 
"categoria": "Couro Premium"},
    "Couro Avestruz+Couro Bovino+Couro Python": {"preco": 2497, 
"categoria": "Couro Premium"},
    "Couro Avestruz+Couro Bovino+Couro Jacaré": {"preco": 2267, 
"categoria": "Couro Premium"},
    "Couro Avestruz+Couro Coelho+Jeans": {"preco": 2167, "categoria": 
"Casual Urbano"},
    "Couro Avestruz+Couro Coelho+Couro Pirarucu": {"preco": 2767, 
"categoria": "Couro Premium"},
    "Couro Avestruz+Couro Coelho+Couro Python": {"preco": 2997, 
"categoria": "Couro Premium"},
    "Couro Avestruz+Couro Jacaré+Couro Pirarucu": {"preco": 2697, 
"categoria": "Couro Premium"},
    "Couro Avestruz+Couro Jacaré+Jeans": {"preco": 2097, "categoria": 
"Casual Urbano"},
    "Couro Avestruz+Couro Jacaré+Couro Python": {"preco": 2937, 
"categoria": "Couro Premium"},
    "Couro Avestruz+Couro Tilápia+Jeans": {"preco": 1837, "categoria": 
"Casual Urbano"},
    "Couro Avestruz+Couro Tilápia+Couro Coelho": {"preco": 2497, 
"categoria": "Couro Premium"},
    "Couro Avestruz+Couro Tilápia+Couro Pirarucu": {"preco": 2437, 
"categoria": "Couro Premium"},
    "Couro Avestruz+Couro Tilápia+Couro Python": {"preco": 2667, 
"categoria": "Couro Premium"},
    "Couro Avestruz+Jeans+Couro Pirarucu": {"preco": 2097, "categoria": 
"Casual Urbano"},
    "Couro Avestruz+Jeans+Couro Python": {"preco": 2337, "categoria": 
"Casual Urbano"},
    "Couro Bovino+Couro Coelho+Couro Jacaré": {"preco": 2437, "categoria": 
"Couro Premium"},
    "Couro Bovino+Couro Coelho+Couro Pirarucu": {"preco": 2437, 
"categoria": "Couro Premium"},
    "Couro Bovino+Couro Coelho+Couro Python": {"preco": 2667, "categoria": 
"Couro Premium"},
    "Couro Bovino+Couro Jacaré+Couro Coelho": {"preco": 2437, "categoria": 
"Couro Premium"},
    "Couro Bovino+Couro Jacaré+Couro Pirarucu": {"preco": 2367, 
"categoria": "Couro Premium"},
    "Couro Bovino+Couro Jacaré+Couro Python": {"preco": 2597, "categoria": 
"Couro Premium"},
    "Couro Bovino+Couro Jacaré+Couro Tilápia": {"preco": 2097, 
"categoria": "Couro Premium"},
    "Couro Bovino+Couro Pirarucu+Couro Python": {"preco": 2597, 
"categoria": "Couro Premium"},
    "Couro Bovino+Couro Tilápia+Couro Coelho": {"preco": 2167, 
"categoria": "Couro Premium"},
    "Couro Bovino+Couro Tilápia+Couro Pirarucu": {"preco": 2097, 
"categoria": "Couro Premium"},
    "Couro Bovino+Couro Tilápia+Couro Python": {"preco": 2337, 
"categoria": "Couro Premium"},
    "Couro Bovino+Jeans+Couro Coelho": {"preco": 1837, "categoria": 
"Casual Urbano"},
    "Couro Bovino+Jeans+Couro Jacaré": {"preco": 1767, "categoria": 
"Casual Urbano"},
    "Couro Bovino+Jeans+Couro Pirarucu": {"preco": 1767, "categoria": 
"Casual Urbano"},
    "Couro Bovino+Jeans+Couro Python": {"preco": 1997, "categoria": 
"Casual Urbano"},
    "Couro Bovino+Jeans+Couro Tilápia": {"preco": 1497, "categoria": 
"Casual Urbano"},
    "Couro Coelho+Couro Jacaré+Jeans": {"preco": 2267, "categoria": 
"Casual Urbano"},
    "Couro Coelho+Couro Jacaré+Couro Pirarucu": {"preco": 2867, 
"categoria": "Couro Premium"},
    "Couro Coelho+Couro Jacaré+Couro Python": {"preco": 3097, "categoria": 
"Couro Premium"},
    "Couro Coelho+Couro Pirarucu+Jeans": {"preco": 2267, "categoria": 
"Casual Urbano"},
    "Couro Coelho+Couro Pirarucu+Couro Python": {"preco": 3097, 
"categoria": "Couro Premium"},
    "Couro Coelho+Couro Python+Jeans": {"preco": 2497, "categoria": 
"Casual Urbano"},
    "Couro Jacaré+Couro Pirarucu+Jeans": {"preco": 2197, "categoria": 
"Casual Urbano"},
    "Couro Jacaré+Couro Pirarucu+Couro Python": {"preco": 3037, 
"categoria": "Couro Premium"},
    "Couro Jacaré+Couro Python+Jeans": {"preco": 2437, "categoria": 
"Casual Urbano"},
    "Couro Jacaré+Couro Tilápia+Jeans": {"preco": 1937, "categoria": 
"Casual Urbano"},
    "Couro Jacaré+Couro Tilápia+Couro Avestruz": {"preco": 2437, 
"categoria": "Couro Premium"},
    "Couro Jacaré+Couro Tilápia+Couro Coelho": {"preco": 2597, 
"categoria": "Couro Premium"},
    "Couro Jacaré+Couro Tilápia+Couro Pirarucu": {"preco": 2537, 
"categoria": "Couro Premium"},
    "Couro Jacaré+Couro Tilápia+Couro Python": {"preco": 2767, 
"categoria": "Couro Premium"},
    "Couro Jacaré+Jeans+Couro Pirarucu": {"preco": 2197, "categoria": 
"Casual Urbano"},
    "Couro Jacaré+Jeans+Couro Python": {"preco": 2437, "categoria": 
"Casual Urbano"},
    "Couro Pirarucu+Couro Python+Jeans": {"preco": 2437, "categoria": 
"Casual Urbano"},
    "Couro Tilápia+Couro Avestruz+Couro Coelho": {"preco": 2497, 
"categoria": "Couro Premium"},
    "Couro Tilápia+Couro Avestruz+Couro Pirarucu": {"preco": 2437, 
"categoria": "Couro Premium"},
    "Couro Tilápia+Couro Avestruz+Couro Python": {"preco": 2667, 
"categoria": "Couro Premium"},
    "Couro Tilápia+Couro Coelho+Couro Pirarucu": {"preco": 2597, 
"categoria": "Couro Premium"},
    "Couro Tilápia+Couro Coelho+Couro Python": {"preco": 2837, 
"categoria": "Couro Premium"},
    "Couro Tilápia+Couro Jacaré+Couro Avestruz": {"preco": 2437, 
"categoria": "Couro Premium"},
    "Couro Tilápia+Couro Jacaré+Couro Coelho": {"preco": 2597, 
"categoria": "Couro Premium"},
    "Couro Tilápia+Couro Jacaré+Couro Pirarucu": {"preco": 2537, 
"categoria": "Couro Premium"},
    "Couro Tilápia+Couro Jacaré+Couro Python": {"preco": 2767, 
"categoria": "Couro Premium"},
    "Couro Tilápia+Jeans+Couro Coelho": {"preco": 1997, "categoria": 
"Casual Urbano"},
    "Couro Tilápia+Jeans+Couro Pirarucu": {"preco": 1937, "categoria": 
"Casual Urbano"},
    "Couro Tilápia+Jeans+Couro Python": {"preco": 2167, "categoria": 
"Casual Urbano"},
    "Couro Tilápia+Jeans+Couro Avestruz": {"preco": 1837, "categoria": 
"Casual Urbano"},
    "Jeans+Couro Pirarucu+Couro Python": {"preco": 2437, "categoria": 
"Casual Urbano"},
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
    print(f"Chave buscada: '{chave}'")
    print("Materiais recebidos:", lista_materiais)

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

