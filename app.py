import logging
from flask import Flask
from flask import request
from time import strftime
from logging.handlers import RotatingFileHandler

MOCKED_RESPONSE = """<?xml version="1.0" encoding="UTF-8"?>
<callbacks_payment_response xmlns="http://api.forticom.com/1.0/">
    true
</callbacks_payment_response>
"""


app = Flask(__name__)


@app.route('/callback', methods=["GET"])
def callback_mock_get():
    ts = strftime('%Y-%b-%d %H:%M:%S')
    logger.debug("[{}] [{}]: [{}]".format(ts, request.method, request.args))
    return MOCKED_RESPONSE, {'Content-Type': 'application/xml'}


@app.route('/callback', methods=["POST"])
def callback_mock_post():
    ts = strftime('%Y-%b-%d %H:%M:%S')
    logger.debug("[{}] [{}]: [{}]".format(ts, request.method, request.data))
    return MOCKED_RESPONSE, {'Content-Type': 'application/xml'}


@app.route('/log', methods=["GET"])
def view_log():
    with open("app.log") as log_file:
        str_log = "<br/>".join(line.strip("\n") for line in log_file.readlines())
        return str_log


if __name__ == '__main__':
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    logger = logging.getLogger('__name__')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    app.run(debug=True, host="localhost", port=8000)
