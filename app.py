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

ERROR_RESPONSE = """<?xml version="1.0" encoding="UTF-8"?>
<ns2:error_response xmlns:ns2='http://api.forticom.com/1.0/'>
    <error_code>1001</error_code>
    <error_msg>CALLBACK_INVALID_PAYMENT : Payment is invalid and can not be processed</error_msg>
</ns2:error_response>
"""

BAD_PRODUCT_CODE = "product_error"

app = Flask(__name__)


@app.route('/callback', methods=["GET"])
def callback_mock_get():
    ts = strftime('%Y-%b-%d %H:%M:%S')
    logger.debug("[{}] [{}]: [{}]".format(ts, request.method, request.args))
    if request.args.get("product_code") == BAD_PRODUCT_CODE:
        return ERROR_RESPONSE, {'Content-Type': 'application/xml', 'Invocation-error': 1001}
    return MOCKED_RESPONSE, {'Content-Type': 'application/xml'}


@app.route('/callback', methods=["POST"])
def callback_mock_post():
    ts = strftime('%Y-%b-%d %H:%M:%S')
    logger.debug("[{}] [{}]: [{}]".format(ts, request.method, request.form))
    if request.args.get("product_code") == BAD_PRODUCT_CODE:
        return ERROR_RESPONSE, {'Content-Type': 'application/xml', 'Invocation-error': 1001}
    return MOCKED_RESPONSE, {'Content-Type': 'application/xml'}


@app.route('/callback_error', methods=["GET"])
def callback_error_mock_get():
    ts = strftime('%Y-%b-%d %H:%M:%S')
    logger.debug("[{}] [{}]: [{}]".format(ts, request.method, request.args))
    return ERROR_RESPONSE, {'Content-Type': 'application/xml', 'Invocation-error': 1001}


@app.route('/callback_error', methods=["POST"])
def callback_error_mock_post():
    ts = strftime('%Y-%b-%d %H:%M:%S')
    logger.debug("[{}] [{}]: [{}]".format(ts, request.method, request.form))
    return ERROR_RESPONSE, {'Content-Type': 'application/xml', 'Invocation-error': 1001}


@app.route('/log', methods=["GET"])
def view_log():
    with open("app.log") as log_file:
        str_log = "<br/>".join(line.strip("\n") for line in log_file.readlines())
        return str_log


@app.route('/flush_log', methods=["POST"])
def flush_log():
    open("app.log", 'w').close()


@app.route('/events', methods=["POST"])
def callback_events():
    ts = strftime('%Y-%b-%d %H:%M:%S')
    data = request.json
    logger.debug("[EVENTS] [{}] [{}]: [{}]".format(ts, request.method, data))
    if data["webhookType"] == "CONFIRMATION":
        return "84fhwgrd", {'Content-Type': 'application/text'}
    return "OK", {'Content-Type': 'application/text'}


if __name__ == '__main__':
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    logger = logging.getLogger('__name__')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    app.run(debug=True, host="localhost", port=8000)
