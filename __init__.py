from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify

import config
from data_interfaces import InterfaceManager

app = Flask(__name__)
interface_manager = InterfaceManager(config.API_KEYS)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/data')
def get_data():
    return jsonify(InterfaceManager.data)


if __name__ == "__main__":

    app.run(host='0.0.0.0', port=80)
