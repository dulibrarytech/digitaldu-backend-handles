import json
import os

from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
from waitress import serve

import handles_lib

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app_version = os.getenv('APP_VERSION')

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
prefix = '/api/'
version = 'v1'
endpoint = '/handles'


@app.route('/', methods=['GET'])
def index():
    """
    Renders Handles API Information
    @returns: String
    """

    return 'DigitalDU-HANDLES ' + app_version


@app.route(prefix + version + endpoint, methods=['GET'])
def get_handle():
    """"
    Creates a handle
    @param: api_key
    @param: uuid
    @returns: Boolean
    """

    api_key = request.args.get('api_key')
    uuid = request.args.get('uuid')
    errors = []

    if api_key is None:
        errors.append('Access denied.')
    elif api_key != os.getenv('API_KEY'):
        errors.append('Access denied.')

    if len(errors) > 0:
        return errors, 403

    response = handles_lib.get_handle(uuid)

    return response, 200


@app.route(prefix + version + endpoint, methods=['POST'])
def create_handle():
    """"
    Creates a handle
    @param: api_key
    @param: uuid
    @returns: Boolean
    """

    api_key = request.args.get('api_key')
    uuid = request.args.get('uuid')
    errors = []

    if api_key is None:
        errors.append('Access denied.')
    elif api_key != os.getenv('API_KEY'):
        errors.append('Access denied.')

    if len(errors) > 0:
        return json.dumps(errors), 403

    result = handles_lib.create_handle(uuid)

    return json.dumps(result), 200


@app.route(prefix + version + endpoint, methods=['PUT'])
def update_handle():
    """"
    Updates a handle
    @param: api_key
    @param: uuid
    @param: new_handle_target
    @returns: Boolean
    """

    api_key = request.args.get('api_key')
    uuid = request.args.get('uuid')
    new_handle_target = request.args.get('target')
    errors = []

    if api_key is None:
        errors.append('Access denied.')
    elif api_key != os.getenv('API_KEY'):
        errors.append('Access denied.')

    if len(errors) > 0:
        return json.dumps(errors), 403

    result = handles_lib.update_handle(uuid, new_handle_target)

    return json.dumps(result), 200


@app.route(prefix + version + endpoint, methods=['DELETE'])
def delete_handle():
    """"
    Deletes a handle
    @param: api_key
    @param: uuid
    @returns: Boolean
    """

    api_key = request.args.get('api_key')
    uuid = request.args.get('uuid')
    errors = []

    if api_key is None:
        errors.append('Access denied.')
    elif api_key != os.getenv('API_KEY'):
        errors.append('Access denied.')

    if len(errors) > 0:
        return json.dumps(errors), 403

    result = handles_lib.delete_handle(uuid)

    return json.dumps(result), 200


app.debug = True
serve(app, host='0.0.0.0', port=os.getenv('APP_PORT'))
