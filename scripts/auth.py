from functools import wraps
from flask import request, jsonify
from configs.database import supabase

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid token"}), 401

        token = auth_header.split(" ")[1]

        try:
            user_response = supabase.auth.get_user(token)
            user = getattr(user_response, "user", None) or user_response
            if not user:
                return jsonify({"error": "Invalid token"}), 401
        except Exception as e:
            return jsonify({"error": "Auth error", "details": str(e)}), 401

        request.user = user
        return f(*args, **kwargs)

    return decorated


