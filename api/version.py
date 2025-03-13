import requests
from flask import Flask, jsonify

app = Flask(__name__)


def get_version():
    github_url = "https://api.github.com/repos/JiaLiFuNia/SmartHNU/releases/latest"
    res = requests.get(github_url).json()
    return res['tag_name']


@app.route("/version", methods=['get'])
def main():
    return jsonify(
        {
            'code': 200,
            'latest_version': get_version(),
        }
    )


if __name__ == '__main__':
    app.run(debug=True)
    app.json.ensure_ascii = False
