from flask import Blueprint, request, jsonify
from configs.database import supabase
from scripts.auth import require_auth
from datetime import datetime

authRoutes = Blueprint("auth", __name__)

ALLOWED_ROLES = {"farmer", "buyer"}


@authRoutes.route("/create", methods=["POST"])
@require_auth
def create_profile():
    try:
        data = request.get_json()
        user_id = request.user.id  
        email = request.user.email  

        if not data:
            return jsonify({"error": "Missing request body"}), 400

        profile = {
            "id": user_id,
            "email": email,
            "full_name": str(data.get("full_name", "")).strip(),
            "mobile": str(data.get("mobile", "")).strip(),
            "address": str(data.get("address", "")).strip(),
            "role": data.get("role") if data.get("role") in ALLOWED_ROLES else None,
            "updated_at": datetime.utcnow().isoformat()
        }

        res = supabase.table("profiles").upsert(profile).execute()

        return jsonify(res.data[0]), 201
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@authRoutes.route("/profile", methods=["GET"])
@require_auth
def get_profile():
    try:
        user_id = request.user.id
        res = supabase.table("profiles").select("*").eq("id", user_id).execute()

        if not res.data:
            return jsonify({"error": "Profile not found"}), 404

        return jsonify(res.data[0]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@authRoutes.route("/update", methods=["PATCH"])
@require_auth
def update_profile():
    try:
        data = request.get_json()
        user_id = request.user.id  

        if not data:
            return jsonify({"error": "Missing request body"}), 400

        update_data = {}
        allowed_fields = ["full_name", "mobile", "address", "role"]

        for field in allowed_fields:
            if field in data:
                value = data[field]
                if field == "role" and value not in ALLOWED_ROLES:
                    return jsonify({"error": f"Invalid role. Must be one of {list(ALLOWED_ROLES)}"}), 400
                update_data[field] = str(value).strip()

        if not update_data:
            return jsonify({"error": "No valid fields to update"}), 400

        update_data["updated_at"] = datetime.utcnow().isoformat()

        res = supabase.table("profiles").update(update_data).eq("id", user_id).execute()

        if not res.data:
            return jsonify({"error": "Profile not found"}), 404

        return jsonify(res.data[0]), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
