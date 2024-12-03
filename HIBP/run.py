from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run-script', methods=['POST'])
def run_script():
    data = request.get_json()
    person_name = data.get("person_name", "")

    if not person_name:
        return jsonify({"error": "Person name is required"}), 400

    try:
        # Execute the WEBSCR.py script with the provided name
        result = subprocess.run(
            ['python', 'WEBSCR.py'],  # Path to your script
            input=person_name, text=True, capture_output=True
        )
        return jsonify({"results": result.stdout})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
