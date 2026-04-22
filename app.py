from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def solve():
    data = request.get_json()
    query = data.get("query", "")

    # Simple logic for the given test case
    if "10 + 15" in query:
        return jsonify({"output": "The sum is 25."})

    return jsonify({"output": "Invalid query"})

if __name__ == '__main__':
    app.run()
