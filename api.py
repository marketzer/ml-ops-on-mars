from flask import Flask, request
from subprocess import Popen, PIPE
import json

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    model = Popen(["python", "model1.py"], stdin=PIPE, stdout=PIPE, encoding='ascii')
    model.stdout.readline()
    lines = model.communicate(json.dumps(request.json))[0].splitlines()
    result = next(x.replace('result: ', '', 1) for x in lines if x.startswith('result'))
    return json.loads(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
