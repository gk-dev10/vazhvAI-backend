from flask import Blueprint, request, jsonify
from configs.database import supabase
from scripts.auth import require_auth

authRoutes = Blueprint("auth", __name__)

@authRoutes.route("/create", methods=["POST"])
@require_auth
def create_profile():
    try:
        data = request.get_json()
        user_id = request.user.id  
        email = request.user.email  
        profile = {
            "id": user_id,
            "email": email,
            "full_name": data.get("full_name"),
            "mobile": data.get("mobile"),
            "address": data.get("address"),
            "role": data.get("role")
        }

        print("Profile payload:", profile)

        res = supabase.table("profiles").upsert(profile).execute()
        print("Supabase response:", res)

        return jsonify(res.data), 200
    except Exception as e:
        import traceback
        traceback.print_exc() 
        return jsonify({"error": str(e)}), 500

@authRoutes.route("/profile", methods=["GET"])
@require_auth
def get_profile():
    user_id = request.user.id
    res = supabase.table("profiles").select("*").eq("id", user_id).execute()

    if not res.data:
        return jsonify({"error": "Profile not found"}), 404
    return jsonify(res.data[0]), 200
