import os
from flask import Flask, request, session, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from helpers import (get_user_by_email,get_user_by_id,save_user,update_user,next_user_id,
    safe_user,hash_password,verify_password,create_empty_profile,get_profile_by_user_id,update_profile,
    get_all_profiles,get_all_users,ensure_list,calculate_match_score,get_common_points,
    get_complementary_points,seed_demo_users)

from ai import generate_ai_analysis

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

#cookie settings
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True
#request with cookies
CORS(app, supports_credentials=True, origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://0.0.0.0:5173",
    "peermatch-ai.up.railway.app"
])

# Auth routes

@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()

    full_name = data.get("fullName", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not full_name or not email or not password:
        return jsonify({"error": "fullName, email, and password are required"}), 400

    if get_user_by_email(email):
        return jsonify({"error": "Email already in use"}), 409

    user_id = next_user_id()
    new_user = {
        "id": user_id,
        "fullName": full_name,
        "email": email,
        "passwordHash": hash_password(password)
    }
    save_user(new_user)
    create_empty_profile(user_id)

    session["user_id"] = user_id

    return jsonify({
        "message": "Registered successfully",
        "user": safe_user(new_user)
    }), 201


@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    user = get_user_by_email(email)
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    if not verify_password(password, user["passwordHash"]):
        return jsonify({"error": "Invalid email or password"}), 401

    session["user_id"] = user["id"]

    return jsonify({
        "message": "Logged in successfully",
        "user": safe_user(user)
    }), 200


@app.route("/api/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200


@app.route("/api/auth/me", methods=["GET"])
def me():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"user": None}), 200

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"user": None}), 200

    return jsonify({"user": safe_user(user)}), 200


# Profile routes

@app.route("/api/profile/me", methods=["GET"])
def get_my_profile():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    profile = get_profile_by_user_id(user_id)
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    return jsonify({
        "profile": {
            "fullName": user["fullName"],
            "education": profile.get("education", ""),
            "skills": profile.get("skills", []),
            "interests": profile.get("interests", []),
            "hobbies": profile.get("hobbies", []),
            "careerGoal": profile.get("careerGoal", ""),
            "languages": profile.get("languages", []),
            "bio": profile.get("bio", ""),
            "discordUsername": profile.get("discordUsername", ""),
            "discordLink": profile.get("discordLink", "")
        }
    }), 200


@app.route("/api/profile/me", methods=["PUT"])
def update_my_profile():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()

    # Update fullName on the user record if provided
    if "fullName" in data and data["fullName"].strip():
        update_user(user_id, {"fullName": data["fullName"].strip()})

    # Build the profile update dict
    profile_updates = {}

    if "education" in data:
        profile_updates["education"] = data["education"]
    if "skills" in data:
        profile_updates["skills"] = ensure_list(data["skills"])
    if "interests" in data:
        profile_updates["interests"] = ensure_list(data["interests"])
    if "hobbies" in data:
        profile_updates["hobbies"] = ensure_list(data["hobbies"])
    if "careerGoal" in data:
        profile_updates["careerGoal"] = data["careerGoal"]
    if "languages" in data:
        profile_updates["languages"] = ensure_list(data["languages"])
    if "bio" in data:
        profile_updates["bio"] = data["bio"]
    if "discordUsername" in data:
        profile_updates["discordUsername"] = data["discordUsername"]
    if "discordLink" in data:
        profile_updates["discordLink"] = data["discordLink"]

    update_profile(user_id, profile_updates)

    # Return the updated profile
    updated_user = get_user_by_id(user_id)
    updated_profile = get_profile_by_user_id(user_id)

    return jsonify({
        "message": "Profile updated successfully",
        "profile": {
            "fullName": updated_user["fullName"],
            "education": updated_profile.get("education", ""),
            "skills": updated_profile.get("skills", []),
            "interests": updated_profile.get("interests", []),
            "hobbies": updated_profile.get("hobbies", []),
            "careerGoal": updated_profile.get("careerGoal", ""),
            "languages": updated_profile.get("languages", []),
            "bio": updated_profile.get("bio", ""),
            "discordUsername": updated_profile.get("discordUsername", ""),
            "discordLink": updated_profile.get("discordLink", "")
        }
    }), 200


# Matches route

@app.route("/api/matches", methods=["GET"])
def get_matches():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    my_profile = get_profile_by_user_id(user_id)
    if not my_profile:
        return jsonify({"error": "Profile not found"}), 404

    all_profiles = get_all_profiles()
    all_users = get_all_users()

    # Build a quick lookup: userId -> user record
    users_by_id = {u["id"]: u for u in all_users}

    scored_matches = []

    for profile in all_profiles:
        # Skip the current user's own profile
        if profile["userId"] == user_id:
            continue

        peer_user = users_by_id.get(profile["userId"])
        if not peer_user:
            continue

        score = calculate_match_score(my_profile, profile)
        common = get_common_points(my_profile, profile)
        complementary = get_complementary_points(my_profile, profile)

        scored_matches.append({
            "profile": profile,
            "user": peer_user,
            "score": score,
            "common": common,
            "complementary": complementary
        })

    # Sort by highest score first
    scored_matches.sort(key=lambda x: x["score"], reverse=True)

    # Take top 5
    top_matches = scored_matches[:5]

    results = []
    for match in top_matches:
        profile = match["profile"]
        user = match["user"]
        common = match["common"]
        complementary = match["complementary"]

        ai_analysis = generate_ai_analysis(my_profile, profile, common, complementary)

        results.append({
            "id": user["id"],
            "name": user["fullName"],
            "education": profile.get("education", ""),
            "matchScore": match["score"],
            "commonPoints": common,
            "complementaryPoints": complementary,
            "skills": profile.get("skills", []),
            "interests": profile.get("interests", []),
            "aiAnalysis": ai_analysis,
            "discordUsername": profile.get("discordUsername", ""),
            "discordLink": profile.get("discordLink", "")
        })

    return jsonify(results), 200


# Seed route

@app.route("/api/seed", methods=["POST"])
def seed():
    added = seed_demo_users()
    return jsonify({
        "message": f"Seed complete. {added} new demo user(s) added."
    }), 200


# Health check
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
