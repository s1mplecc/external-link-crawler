from flask import Flask, request

from domain_parser import parse_domains

app = Flask(__name__)


@app.route('/domains', methods=['POST', 'GET'])
def domains():
    if request.method == 'GET':
        url = request.args.get('url')
        return parse_domains(url)
    else:
        data = request.form
        return data


if __name__ == '__main__':
    app.run()
