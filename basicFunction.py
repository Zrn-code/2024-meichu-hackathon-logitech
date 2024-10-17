import random
import os
import base64


def get_id():
    return ''.join(random.choices('0123456789', k=10))

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def decode_image(image_base64):
    return base64.b64decode(image_base64)

def read_image_by_id_b64(image_id,type):
    image_path = ""
    if type == 'background':
        image_path = os.path.join(os.getenv('BACKGROUND_DIR'), f"{image_id}.png")
    elif type == 'sketch':
        image_path = os.path.join(os.getenv('SKETCH_DIR'), f"{image_id}.png")
    elif type == 'result':
        image_path = os.path.join(os.getenv('RESULT_DIR'), f"{image_id}.png")
    elif type == 'final_result':
        image_path = os.path.join(os.getenv('FINAL_RESULT_DIR'), f"{image_id}.glb")
    else:
        raise Exception("Invalid type")
    
    return encode_image(image_path)
        