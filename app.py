from flask import Flask, request

from domain_parser import parse_domains
from response import Response

app = Flask(__name__)


@app.route('/domains', methods=['GET'])
def domains():
    url = request.args.get('url')
    return Response(data=parse_domains(url)).json()


if __name__ == '__main__':
    app.run()
