from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv('./.flaskenv')

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
