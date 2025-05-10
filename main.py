from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import whois

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

@app.route('/whois', methods=['POST'])
def whois_lookup():
    try:
        data = request.get_json()
        domain = data.get("domain")

        if not domain:
            return jsonify({"error": "Domain name is required"}), 400

        domain_info = whois.whois(domain)

        if not domain_info:
            return jsonify({"error": "WHOIS data not available"}), 404

        response = {
            "domain_name": domain_info.domain_name,
            "registrar": domain_info.registrar,
            "creation_date": str(domain_info.creation_date),
            "expiration_date": str(domain_info.expiration_date),
            "updated_date": str(domain_info.updated_date),
            "name_servers": domain_info.name_servers,
            "status": domain_info.status,
            "owner": domain_info.org
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": f"Unable to perform WHOIS lookup: {str(e)}"}), 500

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
