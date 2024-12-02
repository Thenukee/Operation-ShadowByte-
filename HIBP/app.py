from flask import Flask, request, render_template, jsonify
import os
import json

app = Flask(__name__)

# Ensure the 'uploaded_files' directory exists
UPLOAD_FOLDER = 'uploaded_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return "Welcome to the Home Page. Navigate to <a href='/upload'>/upload</a> to upload a JSON file."

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file and file.filename.endswith('.json'):
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(save_path)
            return jsonify({"message": "File uploaded successfully!", "filename": file.filename}), 200
        else:
            return jsonify({"error": "Invalid file type. Please upload a JSON file."}), 400

    return render_template('upload.html')  # Render the upload form for GET requests

if __name__ == '__main__':
    print("Available routes:")
    print(app.url_map)
    # Bind to all interfaces by setting host to '0.0.0.0'
    app.run(host='0.0.0.0', port=5000, debug=True)
