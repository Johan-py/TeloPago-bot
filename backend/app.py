from flask import Flask, request, jsonify
from response import get_semantic_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Registro temporal para saber si es la primera interacción por sesión
user_sessions = {}

# Mensaje de bienvenida estilo "Serufu"
def get_intro_message():
    return (
        "¡Oh! ¡Hola hola! ヾ(＾∇＾)\n\n"
        "Soy *Mili*, tu ayudante de TeloPago ✨. Estoy aquí para ayudarte a pagar tus compras en tiendas como *AliExpress*, "
        "hacer transferencias a bancos y explicarte cómo funciona todo.\n\n"
        "¡Aunque soy un poco torpe a veces... siempre intento aprender más cada día! 😅💪\n\n"
        "Aquí tienes algunas preguntas que me suelen hacer:\n"
        "• ¿Cómo puedo pagar en AliExpress?\n"
        "• ¿Puedo pagar con QR?\n"
        "• ¿Qué es TeloPago?\n"
        "• ¿Cómo transfiero a Banco Unión?\n\n"
        "¡Pregúntame lo que quieras! Y si no sé algo, lo guardaré en mi libretita para mejorar 🧠✨."
    )

@app.route('/message', methods=['POST'])
def handle_message():
    data = request.get_json()
    user_message = data.get("message", "")
    session_id = data.get("session_id", "default_user")

    print(f"📩 Mensaje recibido desde WhatsApp: {user_message}")

    # Primera interacción
    if session_id not in user_sessions:
        user_sessions[session_id] = True
        return jsonify({"reply": get_intro_message()})

    # Obtener respuesta semántica
    answer = get_semantic_response(user_message)

    if answer:
        return jsonify({"reply": answer})
    else:
        return jsonify({
            "reply": "Disculpa, no tengo una respuesta para eso aún... pero la anotaré para aprender más 📝🤖."
        })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
