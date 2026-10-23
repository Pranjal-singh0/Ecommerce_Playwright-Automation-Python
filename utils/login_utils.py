# utils/login_utils.py

import yaml
import os

def load_credentials(user_type):
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'credentials.yaml')
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data.get(user_type)

def load_user_profile(user_type):
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'credentials.yaml')
    with open(file_path, 'r') as f:
        profiles = yaml.safe_load(f)
    return profiles.get(user_type)

