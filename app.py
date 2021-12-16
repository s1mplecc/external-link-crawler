from urllib.parse import urlparse

from flask import Flask, request

from domain_parser import parse_domains
from response import Response, ResponseCode

app = Flask(__name__)


@app.route('/external-link-domains', methods=['GET'])
def external_link_domains():
    url = request.args.get('url')
    if not urlparse(url).netloc:
        return Response(code=ResponseCode.BAD_REQUEST, msg=f'invalid param url value: {url}').json()
    try:
        return Response(data=parse_domains(url)).json()
    except Exception as e:
        return Response(code=ResponseCode.INTERNAL_SERVER_ERROR, msg=e).json()


if __name__ == '__main__':
    app.run()
