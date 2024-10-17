import os
import requests
import wget
import datetime

tripo3d_api_key = os.getenv('TRIPO3D_API_KEY')

def image_to_3d_tripo(result_id):
    result_path = os.path.join(os.getenv('RESULT_DIR'), f"{result_id}.png")
    url = "https://api.tripo3d.ai/v2/openapi/upload"
    headers = {
        "Authorization": f"Bearer {tripo3d_api_key}"
    }


    with open(result_path, 'rb') as f:
        files = {'file': (result_path, f, 'image/png')}
        response = requests.post(url, headers=headers, files=files)
        response = response.json()
        print(response)
        
    url = "https://api.tripo3d.ai/v2/openapi/task"

    data = {
        "type": "image_to_model",
        "model_version": "v2.0-20240919",
        "file": {
            "type": "png",
            "file_token": f"{response['data']['image_token']}"
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {tripo3d_api_key}"
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.json())
    response = response.json()
    return response


def download_result(task_id):
    url = f"https://api.tripo3d.ai/v2/openapi/task/{task_id}"
    headers = {"Authorization": f"Bearer {tripo3d_api_key}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json().get("data", {})
        output = data.get("output")
        print(f"Output data received: {output}")  

        if output:
            folder_name = datetime.now().strftime("%y%m%d_%H_%M_%S")
            os.makedirs(folder_name, exist_ok=True)
            model_url = output.get("pbr_model")
            if model_url:
                static_model_filename = os.path.join(folder_name, "model.glb")
                wget.download(model_url, static_model_filename)
                print(f"Static model downloaded to {static_model_filename}")
        else:
            print("Error: No output data found for the task.")
    else:
        print("Error:", response.text)    



'''
def image_to_3d(result_id):
    
    result_path = os.path.join(os.getenv('RESULT_DIR'), f"{result_id}.png")
    
    response = requests.post(
    f"https://api.stability.ai/v2beta/3d/stable-fast-3d",
    headers={
        "authorization": f"Bearer ",
    },
    files={
        "image": open(result_path, "rb")
    },
    data={"texture_resolution": 2048},
    )
    
    final_result_id = get_id()
    filename = os.path.join(FINAL_RESULT_DIR, f"{final_result_id}.glb")
    
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        encoded_content = base64.b64encode(response.content).decode('utf-8')
        return {"final_result": encoded_content,"final_result_id": final_result_id}
    
    else:
        raise Exception(str(response.json()))
    
'''