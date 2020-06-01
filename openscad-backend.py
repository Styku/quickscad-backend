from flask import Flask, json, send_file, request, jsonify
from flask_cors import CORS, cross_origin
from pathlib import Path
import subprocess
import glob
import re

script_root = Path('scad-scripts')

api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'

def parse_script_params(script_path):
    read_params = re.compile(r'//\s*@param\s(\w+)\s*\((\w+)\)\s+(.*)\n+(\w+)\s*=\s*\"?([^\"]+)\"?;')
    with open(script_path, 'r') as file:
        script = file.read()

    params = []

    for m in read_params.finditer(script):
        params.append({'name': m.group(1), 'type': m.group(2), 'description': m.group(3), 'var_name': m.group(4), 'value': m.group(5)})

    return params


@api.route('/stl', methods=['POST'])
@cross_origin()
def stl():
    data = request.json
    script_path = script_root / (data['script'] + '.scad')
    args_list = []

    for param in parse_script_params(script_path):
        if param['var_name'] in data:
            val = data[param['var_name']]
            if param['type'] == 'string':
                val = '"{}"'.format(val)
            args_list.append('{}={}'.format(param['var_name'],val))

    subprocess_args = ["openscad", "-o", "api_test.stl", "-D", ';'.join(args_list), str(script_path)]
    print(subprocess_args)
    subprocess.run(subprocess_args)
    return send_file('api_test.stl')

@api.route('/render', methods=['POST'])
@cross_origin()
def render():
    data = request.json
    script_path = script_root / (data['script'] + '.scad')
    subprocess.run(["openscad", "-o", "render.png", "-D", 'category="{}";image="{}"'.format(data['category'], data['image']), str(script_path)])
    return send_file('render.png')
 
@api.route('/script/<name>', methods=['GET'])
@cross_origin()
def script(name):
    return jsonify(
        params = parse_script_params('scad-scripts/{}.scad'.format(name))
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