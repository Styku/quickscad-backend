from flask import Flask, json, send_file, request, jsonify
from flask_cors import CORS, cross_origin
from pathlib import Path
import subprocess
import glob
import re
import base64

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def img_to_base64(img_path):
    img = 'data:image/jpeg;base64,'
    with open(img_path, 'rb') as image:
        image_read = image.read()
        img = 'data:image/jpeg;base64,{}'.format(base64.encodebytes(image_read).decode('ascii'))
    return img

def parse_script_params(script_path):
    read_params = re.compile(r'//\s*@param\s([\w\s]+)\s*\((\w+)\)\s+(.*)\n+(\w+)\s*=\s*\"?([\w.-_]+)\"?;\s*(//\s*\[([0-9.]+):([0-9.]+)\])?(//\s*{([\w,\s]+)})?')
    with open(script_path, 'r') as file:
        script = file.read()

    params = []

    for m in read_params.finditer(script):
        params_dict = {
            'name': m.group(1), 
            'type': m.group(2), 
            'description': m.group(3), 
            'var_name': m.group(4), 
            'value': m.group(5)
        }
        if m.group(7) and m.group(8):
            params_dict['min'] = m.group(7)
            params_dict['max'] = m.group(8)
        if m.group(10):
            params_dict['allowed'] = [s.strip() for s in m.group(10).split(',')]
        params.append(params_dict)
    return params

def make_args_list(script_params, request_data):
    args_list = []
    for param in script_params:
            if param['var_name'] in request_data:
                val = request_data[param['var_name']]
                if param['type'] == 'string':
                    val = '"{}"'.format(val)
                args_list.append('{}={}'.format(param['var_name'],val))
    return ';'.join(args_list)

def run_openscad(request_json, result='stl'):
    if result not in ('stl', 'png'):
        result = 'stl'
    script_path = Path('scad-scripts') / (request_json['script'] + '.scad')
    args = make_args_list(parse_script_params(script_path), request_json)
    output_file = 'out.{}'.format(result)
    subprocess_args = ["openscad", "-o", output_file, "-D", args, str(script_path)]
    subprocess.run(subprocess_args)
    return output_file

@app.route('/stl', methods=['POST'])
@cross_origin()
def stl():
    file = run_openscad(request.json, 'stl')
    return send_file(file)

@app.route('/render', methods=['POST'])
@cross_origin()
def render():
    file = run_openscad(request.json, 'png')
    return send_file(file)
 
@app.route('/script/<name>', methods=['GET'])
@cross_origin()
def script(name):
    return jsonify(params = parse_script_params('scad-scripts/{}.scad'.format(name)))

@app.route('/script', methods=['GET'])
@cross_origin()
def scripts():
    scripts = [Path(p).stem for p in glob.glob('scad-scripts/*.scad')]
    ret = []
    for script in scripts:
        ret.append({'script': script, 'image': img_to_base64('scad-scripts/{}.png'.format(script))})
    return jsonify(ret)

if __name__ == '__main__':
    app.run()