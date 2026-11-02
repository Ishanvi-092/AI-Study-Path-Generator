from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

client = Groq(api_key="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")

@app.route('/v1/answer', methods=['POST'])
def answer():
    data = request.get_json()
    query = data.get('query', '')
    assets = data.get('assets', [])

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=50,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You answer questions in exactly one sentence. "
                    "For math: use 'The sum/difference/product/quotient is X.' "
                    "Output ONLY that one sentence. No intro, no explanation, no punctuation other than the final period."
                )
            },
            {
                "role": "user",
                "content": "What is 10 + 15?"
            },
            {
                "role": "assistant",
                "content": "The sum is 25."
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )

    answer_text = response.choices[0].message.content.strip()
    return jsonify({"output": answer_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)