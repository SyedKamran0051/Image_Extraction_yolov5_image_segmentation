import json
import cv2
import pytest
import os
import sys

# Get the current directory
current_dir = os.path.dirname(__file__)

# Calculate the path to the parent directory
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))

# Add the parent directory to the Python path
sys.path.append(parent_dir)
from prediction import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['status'] == 'healthy'

def test_predict_image_valid(client):
    payload = {
        "image_path": "E:/segmentation_model/datasets/Image_extraction-2/train/images/1064-flatalaska-4-_jpg.rf.e79d4bee51272da0f6979693851abb71.jpg"
    }
    headers = {'Content-Type': 'application/json'}
    response = client.post('/predict', json=payload, headers=headers)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'segmented_images' in data

def test_predict_image_invalid(client):
    payload = {
        "invalid_key": "invalid_value"
    }
    headers = {'Content-Type': 'application/json'}
    response = client.post('/predict', json=payload, headers=headers)
    data = json.loads(response.data)
    assert response.status_code == 400
    assert 'error' in data
