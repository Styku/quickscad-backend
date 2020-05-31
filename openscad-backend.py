from flask import Flask, json, send_file, request, jsonify
from flask_cors import CORS, cross_origin
from pathlib import Path
import subprocess
import glob

script_root = Path('scad-scripts')

api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'

@api.route('/stl', methods=['POST'])
@cross_origin()
def stl():
    data = request.json
    script_path = script_root / (data['script'] + '.scad')
    subprocess.run(["openscad", "-o", "api_test.stl", "-D", 'svg_path="svg/{}/{}.svg"'.format(data['category'], data['image']), str(script_path)])
    return send_file('api_test.stl')

@api.route('/script/<name>', methods=['GET'])
@cross_origin()
def script(name):
    return jsonify(
        params=[
            {'name': 'script', 'type': 'string', 'value': 'keychain'},
            {'name': 'category', 'type': 'string', 'value': 'solid'},
            {'name': 'image', 'type': 'string', 'value': 'anchor'}
        ]
    )

@api.route('/script', methods=['GET'])
@cross_origin()
def scripts():
    scripts = [Path(p).stem for p in glob.glob('scad-scripts/*.scad')]
    return jsonify(
        scripts
    )


if __name__ == '__main__':
    api.run()
