from flask import Flask, json, send_file, request, jsonify
from flask_cors import CORS, cross_origin
from pathlib import Path
import subprocess
import glob
import re
import base64
import os
import tempfile
import uuid

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def img_to_base64(img_path):
    img = 'data:image/jpeg;base64,'
    with open(img_path, 'rb') as image:
        image_read = image.read()
        img = 'data:image/jpeg;base64,{}'.format(
            base64.encodebytes(image_read).decode('ascii'))
    return img


def parse_script(script_path):
    with open(script_path, 'r') as file:
        script = file.read()

    params = parse_script_params(script)
    name = parse_script_metadata(script, 'name')
    description = parse_script_metadata(script, 'description')
    author = parse_script_metadata(script, 'author')
    url = parse_script_metadata(script, 'url')
    tags = parse_script_metadata(script, 'tags')

    return {'params': params, 'source': script, 'name': name, 'description': description, 'author': author, 'url': url, 'tags': tags}


def parse_script_metadata(script, key):
    regex = re.compile(r'@{}\s+(.+)'.format(key))
    m = regex.search(script)
    if m:
        return m.group(1)
    return None


def parse_script_params(script):
    read_params = re.compile(
        r'//\s*@param\s([\w\s]+)\s*\((\w+)\)\s+(.*)\n+(\w+)\s*=\s*\"?([\w.-_]+)\"?;\s*(//\s*\[([0-9.]+):([0-9.]+)\])?(//\s*{([\w,\s]+)})?')

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
            params_dict['allowed'] = [s.strip()
                                      for s in m.group(10).split(',')]
        params.append(params_dict)
    return params


def make_args_list(script_params, request_data):
    args_list = []
    for param in script_params:
        if param['var_name'] in request_data:
            val = request_data[param['var_name']]
            if param['type'] in ('string', 'image'):
                val = '"{}"'.format(val)
            args_list.append('{}={}'.format(param['var_name'], val))
    return ';'.join(args_list)


def run_openscad(request_json, result='stl'):
    if result not in ('stl', 'png'):
        result = 'stl'
    fp = tempfile.NamedTemporaryFile(suffix='.{}'.format(result), mode='w+b')
    temp_file_path = Path(tempfile.gettempdir()) / \
        '{}.{}'.format(uuid.uuid4().hex, result)
    script_path = Path('scad-scripts') / (request_json['script'] + '.scad')

    with open(script_path, 'r') as file:
        script = file.read()
        args = make_args_list(parse_script_params(script), request_json)
        subprocess_args = ["openscad", "-o",
                           temp_file_path, "-D", args, str(script_path)]
        subprocess.run(subprocess_args)

    with open(temp_file_path, 'rb') as temp_fp:
        while True:
            chunk = temp_fp.read(1024*4)
            if not chunk:
                break
            fp.write(chunk)
    os.remove(temp_file_path)
    fp.seek(0)
    return fp


def get_image_tree():
    images = []
    categories = []
    for p in Path('scad-scripts/svg').iterdir():
        if p.is_dir():
            categories.append(p.stem)
            images += ['{}/{}'.format(p.stem, img.stem)
                       for img in p.glob('*.svg')]
    return images, categories


@app.route('/out/<ext>', methods=['POST'])
@cross_origin()
def out(ext):
    fp = run_openscad(request.json, ext)
    return send_file(fp, as_attachment=True, attachment_filename='out.{}'.format(ext))


@app.route('/script/<name>', methods=['GET'])
@cross_origin()
def script(name):
    return jsonify(parse_script('scad-scripts/{}.scad'.format(name)))


@app.route('/images', methods=['GET'])
@cross_origin()
def images():
    images, categories = get_image_tree()
    return jsonify({'images': images, 'categories': categories})


@app.route('/script', methods=['GET'])
@cross_origin()
def scripts():
    scripts = glob.glob('scad-scripts/*.scad')
    ret = []
    for script in scripts:
        s = parse_script(script)
        script_fname = Path(script).stem
        ret.append({
            'script': script_fname,
            'image': img_to_base64('scad-scripts/{}.png'.format(script_fname)),
            'name': s['name'],
            'tags': s['tags']
        })
    return jsonify(ret)


if __name__ == '__main__':
    app.run()
