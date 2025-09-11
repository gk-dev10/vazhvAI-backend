from flask import Blueprint, request, jsonify
from configs.database import supabase
from scripts.auth import require_auth

productRoutes = Blueprint("products", __name__)

@productRoutes.route("/create", methods=["POST"])
@require_auth
def create_product():
    user = request.user
    if user.get("role") != "farmer":
        return jsonify({"error": "Only farmers can add products"}), 403

    data = request.get_json()
    product = {
        "farmer_id": user["id"],
        "name": data.get("name"),
        "description": data.get("description"),
        "price": data.get("price"),
        "quantity": data.get("quantity"),
        "category": data.get("category")
    }

    res = supabase.table("products").insert(product).execute()
    return jsonify(res.data), 201

@productRoutes.route("/", methods=["GET"])
def get_products():
    res = supabase.table("products").select("*").execute()
    return jsonify(res.data), 200

@productRoutes.route("/<product_id>", methods=["GET"])
def get_product(product_id):
    res = supabase.table("products").select("*").eq("id", product_id).execute()
    if not res.data:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(res.data[0]), 200

@productRoutes.route("/<product_id>", methods=["PUT"])
@require_auth
def update_product(product_id):
    user = request.user
    if user.get("role") != "farmer":
        return jsonify({"error": "Only farmers can update products"}), 403

    data = request.get_json()
    res = supabase.table("products").select("*").eq("id", product_id).execute()

    if not res.data:
        return jsonify({"error": "Product not found"}), 404

    product = res.data[0]
    if product["farmer_id"] != user["id"]:
        return jsonify({"error": "You can only update your own products"}), 403

    update_fields = {
        "name": data.get("name", product["name"]),
        "description": data.get("description", product["description"]),
        "price": data.get("price", product["price"]),
        "quantity": data.get("quantity", product["quantity"]),
        "category": data.get("category", product["category"])
    }

    updated = supabase.table("products").update(update_fields).eq("id", product_id).execute()
    return jsonify(updated.data), 200

@productRoutes.route("/<product_id>", methods=["DELETE"])
@require_auth
def delete_product(product_id):
    user = request.user
    if user.get("role") != "farmer":
        return jsonify({"error": "Only farmers can delete products"}), 403

    res = supabase.table("products").select("*").eq("id", product_id).execute()
    if not res.data:
        return jsonify({"error": "Product not found"}), 404

    product = res.data[0]
    if product["farmer_id"] != user["id"]:
        return jsonify({"error": "You can only delete your own products"}), 403

    supabase.table("products").delete().eq("id", product_id).execute()
    return jsonify({"message": "Product deleted"}), 200