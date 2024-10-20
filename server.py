from flask import Flask, render_template, request, jsonify
from PIL import Image
import os
import io
import base64
import json
from dotenv import load_dotenv
from api.TextGenAPI import background_to_text,sketch_to_text
from api.ImgGenAPI import sketch_to_image
from api.ModelGenAPI import image_to_3d_tripo,download_result
from basicFunction import get_id,encode_image,read_image_by_id_b64,save_scene_to_obj
import threading

app = Flask(__name__)

load_dotenv()

data_file = './gallery/src/generated_data.json'

if not os.path.exists(data_file):
    with open(data_file, 'w') as f:
        json.dump([], f)

BACKGROUND_DIR = os.getenv('BACKGROUND_DIR')
SKETCH_DIR = os.getenv('SKETCH_DIR')
RESULT_DIR = os.getenv('RESULT_DIR')
FINAL_RESULT_DIR = os.getenv('FINAL_RESULT_DIR')
OBJ_DIR = os.getenv('OBJ_DIR')

os.makedirs(BACKGROUND_DIR, exist_ok=True)
os.makedirs(SKETCH_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)
os.makedirs(FINAL_RESULT_DIR, exist_ok=True)
os.makedirs(OBJ_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display')
def display():
    return render_template('display.html')  


@app.route('/upload', methods=['POST'])
def upload_images():
    data = request.get_json()
    
    image1_data = base64.b64decode(data['background'])
    image2_data = base64.b64decode(data['sketch'])

    background = Image.open(io.BytesIO(image1_data))
    sketch = Image.open(io.BytesIO(image2_data))
    
    background.thumbnail((800, 800))
    sketch.thumbnail((800, 800))

    background_id = get_id()
    sketch_id = get_id()

    background_filename = f"{background_id}.png"
    sketch_filename = f"{sketch_id}.png"

    background.save(os.path.join(BACKGROUND_DIR, background_filename))
    sketch.save(os.path.join(SKETCH_DIR, sketch_filename)) 
    
    background_base64 = encode_image(os.path.join(BACKGROUND_DIR, background_filename))
    sketch_base64 = encode_image(os.path.join(SKETCH_DIR, sketch_filename))
    
    response = {}
    
    response["background_id"] = background_id
    response["background"] = background_to_text(background_base64)
    response["sketch_id"] = sketch_id
    response["sketch"] = sketch_to_text(sketch_base64)
    
    return jsonify(response)

@app.route('/upload-sketch', methods=['POST'])
def upload_sketch():
    data = request.get_json()
    
    image_data = base64.b64decode(data['sketch'])
    sketch = Image.open(io.BytesIO(image_data))
    sketch.thumbnail((800, 800))

    sketch_id = get_id()
    sketch_filename = f"{sketch_id}.png"
    sketch.save(os.path.join(SKETCH_DIR, sketch_filename)) 
    sketch_base64 = encode_image(os.path.join(SKETCH_DIR, sketch_filename))
    
    response = {}
    
    response["sketch_id"] = sketch_id
    response["sketch"] = sketch_to_text(sketch_base64)
    
    return jsonify(response)

@app.route('/generate-preview', methods=['POST'])
def generate_preview():
    data = request.get_json()
    background_id = data.get('background_id')
    sketch_id = data.get('sketch_id')
    prompt = data.get('prompt')
    if data.get('strength'):
        strength = float(data.get('strength'))
    else:
        strength = 0.5
    result = sketch_to_image(background_id,sketch_id,prompt,strength)
    result_id = result['result_id']
    with open(data_file, 'r+') as f:
        data = json.load(f)
        new_entry = {
            'result_id': result_id,
            'sketch_id': sketch_id,
            'background_id': background_id,
            'model_id': None 
        }
        data.append(new_entry)
        f.seek(0)
        json.dump(data, f, indent=4)
    
    return jsonify(result)

@app.route('/generate-3d-tripo', methods=['POST'])
def generate_3d_tripo():
    data = request.get_json()
    print(data)
    result_id = data['result_id']
    final_result_id = image_to_3d_tripo(result_id)
    thread = threading.Thread(target=save_scene_to_obj,args=(final_result_id,))
    thread.start()
    model = encode_image(os.path.join(FINAL_RESULT_DIR, f"{final_result_id}.glb"))
    with open(data_file, 'r+') as f:
        data = json.load(f)
        for entry in data:
            if entry['result_id'] == result_id:
                entry['model_id'] = final_result_id
                break
        f.seek(0)
        json.dump(data, f, indent=4)
    return jsonify(model)

@app.route('/show-background-ids', methods=['GET'])
def show_background_ids():
    background_ids = os.listdir(BACKGROUND_DIR)
    return jsonify(background_ids)

@app.route('/show-sketch-ids', methods=['GET'])
def show_sketch_ids():
    sketch_ids = os.listdir(SKETCH_DIR)
    return jsonify(sketch_ids)

@app.route('/show-result-ids', methods=['GET'])
def show_result_ids():
    result_ids = os.listdir(RESULT_DIR)
    return jsonify(result_ids)

@app.route('/show-final-result-ids', methods=['GET'])
def show_final_result_ids():
    final_result_ids = os.listdir(FINAL_RESULT_DIR)
    return jsonify(final_result_ids)

@app.route('/show-background/<background_id>', methods=['GET'])
def show_background(background_id):
    background = read_image_by_id_b64(background_id,'background')
    return jsonify(background)

@app.route('/show-sketch/<sketch_id>', methods=['GET'])
def show_sketch(sketch_id):
    sketch = read_image_by_id_b64(sketch_id,'sketch')
    return jsonify(sketch)

@app.route('/show-result/<result_id>', methods=['GET'])
def show_result(result_id):
    result = read_image_by_id_b64(result_id,'result')
    return jsonify(result)

@app.route('/show-final-result/<final_result_id>', methods=['GET'])
def show_final_result(final_result_id):
    final_result = read_image_by_id_b64(final_result_id,'final_result')
    return jsonify(final_result)

@app.route('/find-preview/<final_result_id>',methods = ['GET'])
def find_preview(final_result_id):
    with open('./gallery/src/generated_data.json','r', encoding='utf-8') as file:
        data = json.load(file)
    response = {}
    for entry in data:
        if entry['model_id'] == final_result_id:
            response['result_id'] = entry['result_id']
            response['background_id'] = entry['background_id']
            response['sketch_id'] = entry['sketch_id']
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5183,debug=True)
    