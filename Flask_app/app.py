from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv('./.flaskenv')

app = Flask(__name__)

@app.route('/alim', methods=['GET'])
def insertion():
    return render_template('alimentation.html')


@app.route('/', methods=['GET'])
def search():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
