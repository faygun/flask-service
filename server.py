import os, pathlib, logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from model import create_app
from auth import token_util
from order_svc import order
from product_svc import product
from utility import config
from flask_cors import CORS

server, db = create_app()

CORS(server, origins=["*"], methods=["GET", "POST"], allow_headers="*")

loggingPath = os.path.join(pathlib.Path().resolve(), 'logs', 'error_log.log')

if os.path.exists(loggingPath) == False:
    f = open(loggingPath, "w")

handler = RotatingFileHandler(loggingPath, maxBytes=102400, backupCount=10)
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

handler.setFormatter(logging_format)
server.logger.addHandler(handler)


@server.errorhandler(404)
def page_not_found(error):
    server.logger.error(error)

    return 'This page does not exist', 404


@server.errorhandler(500)
def special_exception_handler(error):
    server.logger.error(error)
    return '500 error', 500


def page_not_found(error):
    return 'This page does not exist', 404


server.error_handler_spec[None][404] = page_not_found

@server.after_request
def add_header(response):
    response.headers.add('access-control-allow-origin', '*')
    response.headers.add('access-control-allow-headers', 'content-type,authorization')
    response.headers.add('access-control-allow-methods', 'get,put,post,delete')
    return response

@server.route("/ping", methods=["GET"])
def ping():
    result = "pong"
    new_line = "\n"
    resp = token_util.getTokenFromDB(db)
    deleteToken = request.args.get("deleteToken")

    if resp and deleteToken and deleteToken == "True":
        token_util.deleteToken(db, resp)
        result = f"{result}{new_line}token was deleted."
    
    if resp:
        result = f"{result}{new_line}{resp.to_json()}"

    return result, 200

@server.route("/token", methods=["GET"])
def token():
    token = token_util.generateToken(db)
    return token.to_json(), 200

@server.route("/api/v1/orders", methods=["POST"])
def getOrders():
    filter = request.get_json()
    response = order.getOrders(db, filter)
    
    
    return response, 200


@server.route("/api/v1/products/upload", methods=["POST"])
def uploadProductFile():
    try:
        response = product.uploadProductFile(request)
        return jsonify(result = response), 200
    
    except Exception as err:
        return jsonify(error = err), 500

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)