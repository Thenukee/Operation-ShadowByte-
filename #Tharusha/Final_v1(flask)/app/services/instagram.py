# routes/instagram.py

from flask import Blueprint, jsonify, request, redirect, session
import requests
import os
import json

instagram_bp = Blueprint('instagram_bp', __name__)

# Load configuration
def load_config():
    config_file = 'config.json'
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    required_keys = ['INSTAGRAM_APP_ID', 'INSTAGRAM_APP_SECRET', 'REDIRECT_URI']
    for key in required_keys:
        if key not in config or not config[key]:
            raise KeyError(f"'{key}' is missing or empty in the configuration file.")
    return config

config = load_config()
INSTAGRAM_APP_ID = config['INSTAGRAM_APP_ID']
INSTAGRAM_APP_SECRET = config['INSTAGRAM_APP_SECRET']
REDIRECT_URI = config['REDIRECT_URI']

# In-memory storage for access tokens (use a database in production)
ACCESS_TOKENS = {}

@instagram_bp.route('/auth', methods=['GET'])
def instagram_auth():
    auth_url = (
        f'https://api.instagram.com/oauth/authorize'
        f'?client_id={INSTAGRAM_APP_ID}'
        f'&redirect_uri={REDIRECT_URI}'
        f'&scope=user_profile,user_media'
        f'&response_type=code'
    )
    return redirect(auth_url)

@instagram_bp.route('/authorize', methods=['GET'])
def authorize():
    code = request.args.get('code')
    if code:
        # Exchange code for a short-lived access token
        token_url = 'https://api.instagram.com/oauth/access_token'
        payload = {
            'client_id': INSTAGRAM_APP_ID,
            'client_secret': INSTAGRAM_APP_SECRET,
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'code': code
        }
        response = requests.post(token_url, data=payload)
        if response.status_code == 200:
            data = response.json()
            access_token = data.get('access_token')
            user_id = data.get('user_id')
            # Store access token (use a secure method in production)
            ACCESS_TOKENS[user_id] = access_token
            return jsonify({'message': 'Authorization successful', 'user_id': user_id})
        else:
            return jsonify({'error': 'Failed to obtain access token'}), 400
    else:
        return jsonify({'error': 'Authorization code not provided'}), 400

@instagram_bp.route('/user/<user_id>', methods=['GET'])
def get_instagram_user_data(user_id):
    access_token = ACCESS_TOKENS.get(user_id)
    if access_token:
        user_data = get_user_info(user_id, access_token)
        if user_data:
            return jsonify(user_data)
        else:
            return jsonify({'error': 'Failed to retrieve user data'}), 400
    else:
        return jsonify({'error': 'Access token not found for this user'}), 404

def get_user_info(user_id, access_token):
    url = f'https://graph.instagram.com/{user_id}?fields=id,username,account_type,media_count&access_token={access_token}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

@instagram_bp.route('/user/<user_id>/media', methods=['GET'])
def get_user_media_route(user_id):
    access_token = ACCESS_TOKENS.get(user_id)
    if access_token:
        media_data = get_user_media(user_id, access_token)
        if media_data:
            return jsonify(media_data)
        else:
            return jsonify({'error': 'Failed to retrieve media data'}), 400
    else:
        return jsonify({'error': 'Access token not found for this user'}), 404

def get_user_media(user_id, access_token):
    url = f'https://graph.instagram.com/{user_id}/media?fields=id,caption,media_type,media_url,permalink,thumbnail_url,timestamp&access_token={access_token}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Additional endpoint to get details of a specific media item
@instagram_bp.route('/media/<media_id>', methods=['GET'])
def get_media_details(media_id):
    # In a real application, you'd need to know which user's token to use
    # For this example, we'll just use the first token we have
    if ACCESS_TOKENS:
        access_token = next(iter(ACCESS_TOKENS.values()))
        media_data = get_media_info(media_id, access_token)
        if media_data:
            return jsonify(media_data)
        else:
            return jsonify({'error': 'Failed to retrieve media details'}), 400
    else:
        return jsonify({'error': 'No access tokens available'}), 404

def get_media_info(media_id, access_token):
    url = f'https://graph.instagram.com/{media_id}?fields=id,media_type,media_url,username,timestamp,caption&access_token={access_token}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None
