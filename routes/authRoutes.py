from flask import Blueprint, request, jsonify
from configs.database import supabase
from scripts.auth import require_auth
from datetime import datetime

authRoutes = Blueprint("auth", __name__)

ALLOWED_ROLES = {"farmer", "buyer"}


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
        # ✅ Only allow these fields
        allowed_fields = ["mobile", "address", "latitude", "longitude", "about"]

        for field in allowed_fields:
            if field in data:
                value = data[field]

                if field in ["latitude", "longitude"]:
                    try:
                        update_data[field] = float(value)
                    except ValueError:
                        return jsonify({"error": f"{field} must be a number"}), 400
                else:
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


@authRoutes.route("/role", methods=["PATCH"])
@require_auth
def change_role():
    try:
        data = request.get_json()
        user_id = request.user.id  

        if not data or "role" not in data:
            return jsonify({"error": "Missing role field"}), 400

        new_role = str(data["role"]).strip()

        if new_role not in ALLOWED_ROLES:
            return jsonify({"error": f"Invalid role. Must be one of {list(ALLOWED_ROLES)}"}), 400

        update_data = {
            "role": new_role,
            "updated_at": datetime.utcnow().isoformat()
        }

        res = supabase.table("profiles").update(update_data).eq("id", user_id).execute()

        if not res.data:
            return jsonify({"error": "Profile not found"}), 404

        return jsonify({
            "message": "Role updated successfully",
            "profile": res.data[0]
        }), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
