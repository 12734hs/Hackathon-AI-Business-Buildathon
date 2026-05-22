import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

USERS_FILE = os.path.join(DATA_DIR, "users.json")
PROFILES_FILE = os.path.join(DATA_DIR, "profiles.json")

#JSON file funcs

def read_json(filepath):
    """Read and return data from a JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)


def write_json(filepath, data):
    """Write data to a JSON file."""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


#User funcs

def get_all_users():
    return read_json(USERS_FILE)


def get_user_by_id(user_id):
    """Find and return a user by their id."""
    users = get_all_users()
    for user in users:
        if user["id"] == user_id:
            return user
    return None


def get_user_by_email(email):
    """Find and return a user by their email address."""
    users = get_all_users()
    for user in users:
        if user["email"].lower() == email.lower():
            return user
    return None


def save_user(user):
    """Append a new user to users.json."""
    users = get_all_users()
    users.append(user)
    write_json(USERS_FILE, users)


def update_user(user_id, updates):
    """Update a user's fields in users.json."""
    users = get_all_users()
    for user in users:
        if user["id"] == user_id:
            user.update(updates)
    write_json(USERS_FILE, users)


def next_user_id():
    """Return the next available user id."""
    users = get_all_users()
    if not users:
        return 1
    return max(u["id"] for u in users) + 1


def safe_user(user):
    """Return a user object without the passwordHash field."""
    return {
        "id": user["id"],
        "fullName": user["fullName"],
        "email": user["email"]
    }


#Password funcs
def hash_password(password):
    return generate_password_hash(password)


def verify_password(password, hashed):
    return check_password_hash(hashed, password)


#Profile funcs

def get_all_profiles():
    return read_json(PROFILES_FILE)


def get_profile_by_user_id(user_id):
    """Find and return a profile by userId."""
    profiles = get_all_profiles()
    for profile in profiles:
        if profile["userId"] == user_id:
            return profile
    return None


def save_profile(profile):
    """Append a new profile to profiles.json."""
    profiles = get_all_profiles()
    profiles.append(profile)
    write_json(PROFILES_FILE, profiles)


def update_profile(user_id, updates):
    """Update an existing profile in profiles.json."""
    profiles = get_all_profiles()
    for profile in profiles:
        if profile["userId"] == user_id:
            profile.update(updates)
    write_json(PROFILES_FILE, profiles)


def create_empty_profile(user_id):
    """Create an empty profile entry for a new user."""
    profile = {
        "userId": user_id,
        "education": "",
        "skills": [],
        "interests": [],
        "hobbies": [],
        "careerGoal": "",
        "languages": [],
        "bio": "",
        "discordUsername": "",
        "discordLink": ""
    }
    save_profile(profile)
    return profile


def ensure_list(value):
    """Make sure a value is a list. If it's a string, split by comma."""
    if isinstance(value, list):
        return [item.strip() for item in value if item.strip()]
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return []


#Match score funcs

def count_common_items(list_a, list_b):
    """Count how many items appear in both lists (case-insensitive)."""
    set_a = set(item.lower() for item in list_a)
    set_b = set(item.lower() for item in list_b)
    return len(set_a & set_b)


def overlap_score(list_a, list_b, weight):
    """
    Give a partial score based on how many items two lists share.
    If either list is empty, return 0.
    Otherwise return weight * (shared / max possible shared).
    """
    if not list_a or not list_b:
        return 0
    shared = count_common_items(list_a, list_b)
    max_possible = min(len(list_a), len(list_b))
    return round(weight * (shared / max_possible))


def word_overlap_score(text_a, text_b, weight):
    """
    Compare two text strings word by word.
    Score based on how many words they share.
    """
    if not text_a or not text_b:
        return 0
    words_a = set(text_a.lower().split())
    words_b = set(text_b.lower().split())
    shared = len(words_a & words_b)
    max_possible = min(len(words_a), len(words_b))
    if max_possible == 0:
        return 0
    return round(weight * (shared / max_possible))


def calculate_match_score(my_profile, other_profile):
    """
    Calculate a total match score (0–100) between two profiles.
    Weights: skills=30, interests=30, hobbies=10, languages=10, careerGoal=10, education=10
    """
    score = 0
    score += overlap_score(my_profile.get("skills", []), other_profile.get("skills", []), 30)
    score += overlap_score(my_profile.get("interests", []), other_profile.get("interests", []), 30)
    score += overlap_score(my_profile.get("hobbies", []), other_profile.get("hobbies", []), 10)
    score += overlap_score(my_profile.get("languages", []), other_profile.get("languages", []), 10)
    score += word_overlap_score(my_profile.get("careerGoal", ""), other_profile.get("careerGoal", ""), 10)
    score += word_overlap_score(my_profile.get("education", ""), other_profile.get("education", ""), 10)
    return min(score, 100)


def get_common_points(my_profile, other_profile):
    """
    Return a list of items that both users share across skills, interests, and hobbies.
    """
    common = []

    def shared_items(list_a, list_b):
        # compare common items between two lists
        set_a = set(item.lower() for item in list_a)
        result = []
        for item in list_b:
            if item.lower() in set_a:
                result.append(item)
        return result

    common += shared_items(my_profile.get("skills", []), other_profile.get("skills", []))
    common += shared_items(my_profile.get("interests", []), other_profile.get("interests", []))
    common += shared_items(my_profile.get("hobbies", []), other_profile.get("hobbies", []))

    # remove duplicates while keeping order
    seen = set()
    unique = []
    for item in common:
        if item.lower() not in seen:
            seen.add(item.lower())
            unique.append(item)

    return unique


def get_complementary_points(my_profile, other_profile):
    """
    Return strings describing skills/interests one user has that the other does not.
    Example: 'Backend + Frontend'
    """
    complementary = []

    my_skills = set(s.lower() for s in my_profile.get("skills", []))
    other_skills = set(s.lower() for s in other_profile.get("skills", []))

    # skills the other person has that I don't
    unique_to_other = other_skills - my_skills
    unique_to_me = my_skills - other_skills

    if unique_to_me and unique_to_other:
        # pick a short label for each side
        me_label = list(unique_to_me)[0].capitalize()
        other_label = list(unique_to_other)[0].capitalize()
        complementary.append(f"{me_label} + {other_label}")

    my_interests = set(i.lower() for i in my_profile.get("interests", []))
    other_interests = set(i.lower() for i in other_profile.get("interests", []))
    unique_interests = other_interests - my_interests

    if unique_interests:
        label = list(unique_interests)[0].capitalize()
        complementary.append(f"They know about: {label}")

    return complementary


#Seed data funcs

SEED_USERS = [
    {"fullName": "Leyla Mammadova",   "email": "leyla@example.com",   "password": "password123"},
    {"fullName": "Tural Aliyev",      "email": "tural@example.com",    "password": "password123"},
    {"fullName": "Nigar Hasanova",    "email": "nigar@example.com",    "password": "password123"},
    {"fullName": "Farid Guliyev",     "email": "farid@example.com",    "password": "password123"},
    {"fullName": "Aysel Ismayilova",  "email": "aysel@example.com",    "password": "password123"},
    {"fullName": "Kamran Jafarov",    "email": "kamran@example.com",   "password": "password123"},
    {"fullName": "Gunay Rzayeva",     "email": "gunay@example.com",    "password": "password123"},
    {"fullName": "Elvin Babayev",     "email": "elvin@example.com",    "password": "password123"},
]

SEED_PROFILES = [
    {
        "education": "Holberton School Azerbaijan",
        "skills": ["JavaScript", "React", "CSS", "HTML", "Figma"],
        "interests": ["AI Products", "Startups", "Hackathons"],
        "hobbies": ["Reading", "Gaming"],
        "careerGoal": "Frontend Developer",
        "languages": ["English", "Azerbaijani"],
        "bio": "Frontend developer who loves building clean UIs.",
        "discordUsername": "leyla.dev",
        "discordLink": "https://discord.com/users/leyla"
    },
    {
        "education": "ADA University Computer Science",
        "skills": ["Python", "Django", "PostgreSQL", "Docker", "REST APIs"],
        "interests": ["Cloud Computing", "DevOps", "Open Source"],
        "hobbies": ["Football", "Cycling"],
        "careerGoal": "Backend Developer",
        "languages": ["English", "Russian", "Azerbaijani"],
        "bio": "Backend developer focused on scalable systems.",
        "discordUsername": "tural.backend",
        "discordLink": "https://discord.com/users/tural"
    },
    {
        "education": "Baku Design Academy",
        "skills": ["Figma", "Adobe XD", "Illustrator", "Prototyping", "User Research"],
        "interests": ["UX Design", "Product Design", "Accessibility"],
        "hobbies": ["Painting", "Photography"],
        "careerGoal": "UI/UX Designer",
        "languages": ["English", "Azerbaijani"],
        "bio": "Designer who bridges user needs and beautiful interfaces.",
        "discordUsername": "nigar.design",
        "discordLink": "https://discord.com/users/nigar"
    },
    {
        "education": "UFAZ Data Science Program",
        "skills": ["Python", "TensorFlow", "PyTorch", "Machine Learning", "Data Analysis"],
        "interests": ["AI", "Deep Learning", "Hackathons", "Research"],
        "hobbies": ["Chess", "Volunteering"],
        "careerGoal": "AI Engineer",
        "languages": ["English", "French", "Azerbaijani"],
        "bio": "AI enthusiast building intelligent products.",
        "discordUsername": "farid.ai",
        "discordLink": "https://discord.com/users/farid"
    },
    {
        "education": "Baku Business University",
        "skills": ["Public Speaking", "Marketing", "Pitch Decks", "Social Media", "Copywriting"],
        "interests": ["Startups", "Entrepreneurship", "Hackathons", "Networking"],
        "hobbies": ["Volunteering", "Traveling"],
        "careerGoal": "Startup Marketing Lead",
        "languages": ["English", "Russian", "Azerbaijani"],
        "bio": "Marketing person who helps teams tell their story.",
        "discordUsername": "aysel.pitch",
        "discordLink": "https://discord.com/users/aysel"
    },
    {
        "education": "Khazar University Statistics",
        "skills": ["Python", "SQL", "Pandas", "Tableau", "Excel"],
        "interests": ["Data Science", "AI", "Finance", "Analytics"],
        "hobbies": ["Reading", "Chess"],
        "careerGoal": "Data Analyst",
        "languages": ["English", "Russian"],
        "bio": "Data analyst turning raw numbers into insights.",
        "discordUsername": "kamran.data",
        "discordLink": "https://discord.com/users/kamran"
    },
    {
        "education": "STEP IT Academy Mobile Development",
        "skills": ["Flutter", "Dart", "React Native", "Firebase", "iOS Development"],
        "interests": ["Mobile Apps", "Startups", "AI", "Hackathons"],
        "hobbies": ["Gaming", "F1"],
        "careerGoal": "Mobile Developer",
        "languages": ["English", "Russian", "Azerbaijani"],
        "bio": "Mobile developer building apps for the next billion users.",
        "discordUsername": "gunay.mobile",
        "discordLink": "https://discord.com/users/gunay"
    },
    {
        "education": "Cyber Security Academy Baku",
        "skills": ["Penetration Testing", "Linux", "Networking", "Python", "CTF"],
        "interests": ["Cybersecurity", "Ethical Hacking", "Open Source"],
        "hobbies": ["CTF Competitions", "Gaming"],
        "careerGoal": "Cybersecurity Engineer",
        "languages": ["English", "Russian"],
        "bio": "Security student breaking things to make them safer.",
        "discordUsername": "elvin.sec",
        "discordLink": "https://discord.com/users/elvin"
    },
]


def seed_demo_users():
    """
    Add demo users and profiles if they don't already exist.
    Checks by email to avoid duplicates.
    """
    added = 0
    for i, seed_user in enumerate(SEED_USERS):
        existing = get_user_by_email(seed_user["email"])
        if existing:
            continue  # already seeded, skip

        user_id = next_user_id()
        new_user = {
            "id": user_id,
            "fullName": seed_user["fullName"],
            "email": seed_user["email"],
            "passwordHash": hash_password(seed_user["password"])
        }
        save_user(new_user)

        profile = {**SEED_PROFILES[i], "userId": user_id}
        save_profile(profile)

        added += 1

    return added
