from flask import (
    Flask,
    request
)
from celery_worker_1 import lobot

app = Flask(__name__)


@app.route('/runlobot', methods=['POST'])
def run_lobot():
    data = request.get_json()
    uid = data["UserId"]
    lobot.delay(uid)
    return "Request Submitted"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)