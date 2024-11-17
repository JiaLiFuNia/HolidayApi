from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/version", methods=['get'])
def main():
    return jsonify(
        {
            'code': 200,
            'version': '2.0.28',
        }
    )


if __name__ == '__main__':
    app.run(debug=True)
    app.json.ensure_ascii = False
