from flask import Flask, json, send_file, request
from pathlib import Path
import subprocess

script_root = Path('scad-scripts')

api = Flask(__name__)

@api.route('/stl', methods=['POST'])
def stl():
    data = request.form
    script_path = script_root / (data['base'] + '.scad')
    subprocess.run(["openscad", "-o", "api_test.stl", "-D", 'svg_path="svg/{}/{}.svg"'.format(data['category'], data['image']), str(script_path)])
    return send_file('api_test.stl')

if __name__ == '__main__':
    api.run()
