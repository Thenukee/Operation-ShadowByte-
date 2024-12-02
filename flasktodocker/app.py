from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search_username():
    data = request.json
    username = data.get('username')

    if not username:
        return jsonify({"error": "Username is required"}), 400

    # Define the output file location
    results_file = "results.json"

    # Run Sherlock in Docker
    command = f"docker run -it --rm -v {os.getcwd()}:/output sherlock/sherlock {username} --json /output/{results_file}"
    subprocess.run(command, shell=True)

    # Check if the results file exists
    if os.path.exists(results_file):
        with open(results_file, "r") as file:
            results = file.read()
        return jsonify({"results": results})
    else:
        return jsonify({"error": "No results found or error occurred"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
