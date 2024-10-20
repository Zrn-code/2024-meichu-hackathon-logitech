import os
import random
import requests
from .TextGenAPI import background_to_text, sketch_to_one_text
from basicFunction import get_id, encode_image, read_image_by_id_b64



stability_api_key = os.getenv('STABILITY_AI_API_KEY')

def sketch_to_image(background_id,sketch_id,sketch_prompt,strength=0.5):
    
    background_info = background_to_text(read_image_by_id_b64(background_id,'background'))
    sketch_info = ""
    if sketch_prompt != None:
        sketch_info = sketch_prompt
    else:
        sketch_info = sketch_to_one_text(read_image_by_id_b64(sketch_id,'sketch'))
    sketch_path = os.path.join(os.getenv('SKETCH_DIR'),f"{sketch_id}.png")
    
    prompt = f"a {sketch_info} on a {background_info} present it from a slightly angled, 3D perspective."
    print(prompt)
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/control/sketch",
        headers={
            "authorization": f"Bearer {stability_api_key}",
            "accept": "image/*"
        },
        files={
            "image": open(sketch_path, "rb")
        },
        data={
            "prompt": f"{prompt}",
            "control_strength": strength,
            "output_format": "png"
        },
    )

    result_id = get_id()
    filename = os.path.join(os.getenv('RESULT_DIR'), f"{result_id}.png")
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))
    
    return {"result": encode_image(filename),"result_id": result_id}
    
