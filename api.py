from flask import Flask, request
from subprocess import Popen, PIPE
from threading import Timer
import json
import os

app = Flask(__name__)
mlModel = "model2.py"
timeout = 10


@app.route('/predict', methods=['POST'])
def predict():
    with Popen(["python", os.path.join("models", mlModel)], stdin=PIPE, stdout=PIPE, encoding='ascii') as model:
        try:
            model.stdout.readline()
            timer = Timer(timeout, model.kill)
            timer.start()
            response = model.communicate(json.dumps(request.json), timeout=timeout)
            timer.cancel()
            lines = response[0].splitlines()
            result = next(x.replace('result: ', '', 1) for x in lines if x.startswith('result'))
            return json.loads(result)

        except Exception:
            return {'error': 'model timeout'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
