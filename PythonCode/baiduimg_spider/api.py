from flask import Flask, request
import time
import re
import sys
import os
import json

app = Flask(__name__)


@app.route('/t', methods=['GET'])
def test():
    return str(time.time())

if __name__ == '__main__':
    app.run(debug=True)
