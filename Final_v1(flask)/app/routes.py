# routes.py
from flask import Blueprint, request, jsonify, send_file
from app.services.dorking import (
    generate_name_variants,
    create_suspect_folder,
    load_cache,
    perform_instagram_scraping,
    save_cache,
    perform_searches,
    process_results,
    save_to_json,
    perform_dorking
)
import os
import json
import shutil
import threading
import uuid

api = Blueprint('api', __name__)

@api.route('/add-suspect', methods=['POST'])
def add_suspect():
    try:
        data = request.json
        suspect_name = data.get('suspect_name')
        email = data.get('email', '')
        nic = data.get('nic', '')
        social_media = data.get('social_media', '')

        if not suspect_name:
            return jsonify({"status": "error", "error": "Suspect name is required."}), 400

        # Path to the suspects.json file
        suspects_file = os.path.join('suspects', 'suspects.json')

        # Load existing suspects
        if os.path.exists(suspects_file):
            with open(suspects_file, 'r', encoding='utf-8') as f:
                suspects = json.load(f)
        else:
            suspects = []

        # Check if the suspect already exists
        for suspect in suspects:
            if suspect['name'].lower() == suspect_name.lower():
                return jsonify({
                    "status": "exists",
                    "message": "Suspect already exists.",
                    "suspect_id": suspect['id']
                }), 200

        # Generate a unique suspect ID
        suspect_id = str(uuid.uuid4())

        # Create suspect folder
        suspect_folder = create_suspect_folder(suspect_id)

        # Save suspect details
        suspect_details = {
            "id": suspect_id,
            "name": suspect_name,
            "email": email,
            "nic": nic,
            "social_media": social_media
        }
        details_file = os.path.join(suspect_folder, 'details.json')
        with open(details_file, 'w', encoding='utf-8') as f:
            json.dump(suspect_details, f, ensure_ascii=False, indent=4)

        # Append new suspect to the suspects list and save it
        suspects.append(suspect_details)
        with open(suspects_file, 'w', encoding='utf-8') as f:
            json.dump(suspects, f, ensure_ascii=False, indent=4)

        # Initialize cache
        cache = load_cache(suspect_folder)
        save_cache(suspect_folder, cache)

        return jsonify({
            "status": "success",
            "message": f"Suspect '{suspect_name}' added successfully.",
            "suspect_id": suspect_id
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@api.route('/delete-suspect', methods=['DELETE'])
def delete_suspect():
    try:
        data = request.json
        suspect_id = data.get('suspect_id')

        if not suspect_id:
            return jsonify({"status": "error", "error": "Suspect ID is required."}), 400

        suspect_folder = os.path.join('suspects', suspect_id)

        if not os.path.exists(suspect_folder):
            return jsonify({"status": "error", "error": "Suspect not found."}), 404

        shutil.rmtree(suspect_folder)

        connections_file = os.path.join('connections.json')
        if os.path.exists(connections_file):
            with open(connections_file, 'r', encoding='utf-8') as f:
                connections = json.load(f)
            updated_connections = [conn for conn in connections if conn['source'] != suspect_id and conn['target'] != suspect_id]
            with open(connections_file, 'w', encoding='utf-8') as f:
                json.dump(updated_connections, f, ensure_ascii=False, indent=4)

        return jsonify({"status": "success", "message": f"Suspect with ID '{suspect_id}' deleted successfully."}), 200

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@api.route('/add-connection', methods=['POST'])
def add_connection():
    try:
        data = request.json
        source_id = data.get('source_id')
        target_id = data.get('target_id')

        if not source_id or not target_id:
            return jsonify({"status": "error", "error": "Source and target IDs are required."}), 400

        if source_id == target_id:
            return jsonify({"status": "error", "error": "Source and target cannot be the same."}), 400

        connections_file = os.path.join('connections.json')

        if os.path.exists(connections_file):
            with open(connections_file, 'r', encoding='utf-8') as f:
                connections = json.load(f)
        else:
            connections = []

        if {"source": source_id, "target": target_id} in connections or {"source": target_id, "target": source_id} in connections:
            return jsonify({"status": "error", "error": "Connection already exists."}), 400

        connections.append({"source": source_id, "target": target_id})

        with open(connections_file, 'w', encoding='utf-8') as f:
            json.dump(connections, f, ensure_ascii=False, indent=4)

        return jsonify({"status": "success", "message": f"Connection added between '{source_id}' and '{target_id}'."}), 200

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@api.route('/get-results', methods=['GET'])
def get_results():
    try:
        suspect_id = request.args.get('suspect_id')
        if not suspect_id:
            return jsonify({"status": "error", "error": "Suspect ID is required."}), 400

        suspect_folder = os.path.join('suspects', suspect_id)
        results_file = os.path.join(suspect_folder, 'results.json')

        if not os.path.exists(results_file):
            # Indicate that the results are still being processed
            return jsonify({"status": "processing", "message": "Results are being processed."}), 202

        with open(results_file, 'r', encoding='utf-8') as f:
            results_data = json.load(f)

        return jsonify({"status": "success", "data": results_data}), 200

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@api.route('/dork-suspect', methods=['POST'])
def dork_suspect():
    try:
        data = request.json
        suspect_id = data.get('suspect_id')
        search_all = data.get('search_all', False)
        search_engines = data.get('search_engines', [])

        if not suspect_id:
            return jsonify({"status": "error", "error": "Suspect ID is required."}), 400

        suspect_folder = os.path.join('suspects', suspect_id)

        if not os.path.exists(suspect_folder):
            return jsonify({"status": "error", "error": "Suspect not found. Please add the suspect first."}), 404

        # Clear existing results before re-scraping
        results_file = os.path.join(suspect_folder, 'results.json')
        if os.path.exists(results_file):
            os.remove(results_file)

        def run_dorking():
            try:
                perform_dorking(suspect_id, search_all, search_engines)
            except Exception as e:
                print(f"Error during dorking for {suspect_id}: {e}")

        dorking_thread = threading.Thread(target=run_dorking, daemon=True)
        dorking_thread.start()

        return jsonify({"status": "success", "message": f"Dorking initiated for suspect ID {suspect_id}."}), 200

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@api.route('/download-results', methods=['GET'])
def download_results():
    """
    API endpoint to download the results.json file for a suspect.
    Expects query parameter 'suspect_id'.
    """
    try:
        suspect_id = request.args.get('suspect_id')
        if not suspect_id:
            return jsonify({"status": "error", "error": "Suspect ID is required."}), 400

        suspect_folder = os.path.join('suspects', suspect_id)
        results_file = os.path.join(suspect_folder, 'results.json')

        if not os.path.exists(results_file):
            return jsonify({"status": "error", "error": "Results not found for the given suspect."}), 404

        return send_file(results_file, as_attachment=True)

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@api.route('/get-suspect', methods=['GET'])
def get_suspect():
    try:
        suspect_id = request.args.get('suspect_id')
        if not suspect_id:
            return jsonify({"status": "error", "error": "Suspect ID is required."}), 400

        suspect_folder = os.path.join('suspects', suspect_id)
        details_file = os.path.join(suspect_folder, 'details.json')

        if not os.path.exists(details_file):
            return jsonify({"status": "error", "error": "Suspect not found."}), 404

        with open(details_file, 'r', encoding='utf-8') as f:
            suspect_details = json.load(f)

        return jsonify({"status": "success", "data": suspect_details}), 200

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@api.route('/instagram-scrape', methods=['POST'])
def instagram_scrape():
    try:
        data = request.json
        suspect_id = data.get('suspect_id')

        if not suspect_id:
            return jsonify({"status": "error", "error": "Suspect ID is required."}), 400

        suspect_folder = os.path.join('suspects', suspect_id)
        details_file = os.path.join(suspect_folder, 'details.json')

        if not os.path.exists(details_file):
            return jsonify({"status": "error", "error": "Suspect details not found."}), 404

        with open(details_file, 'r', encoding='utf-8') as f:
            suspect_details = json.load(f)

        suspect_name = suspect_details.get('name')
        if not suspect_name:
            return jsonify({"status": "error", "error": "Suspect name not found."}), 400

        # Perform Instagram Scraping
        instagram_data = perform_instagram_scraping(suspect_name)

        return jsonify({"status": "success", "data": instagram_data}), 200

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500