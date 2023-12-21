from flask import Flask, jsonify

app = Flask(__name__)

# Sample user data
users = [
    {
        "id": 1,
        "name": "Meet",
        "hobbies": ["Music", "Chess", "Drawing"]
    },
    {
        "id": 2,
        "name": "Pari Singh",
        "hobbies": ["Music", "Cooking", "Reading"]
    },
    {
        "id": 3,
        "name": "Naina Patel",
        "hobbies": ["Music", "Chess", "Dance"]
    },
    {
        "id": 4,
        "name": "Amy Bhatt",
        "hobbies": ["Cooking"]
    }
]

@app.route('/match/<int:user_id>', methods=['GET'])
def get_potential_matches(user_id):
    user = next((user for user in users if user["id"] == user_id), None)
    if not user:
        return jsonify(message="User not found"), 404

    matches = []
    for other_user in users:
        if other_user["id"] != user_id:
            common_hobbies = set(user["hobbies"]).intersection(other_user["hobbies"])
            matches.append({"id": other_user["id"], "name": other_user["name"], "hobbies": list(common_hobbies)})

    sorted_matches = sorted(matches, key=lambda match: len(match["hobbies"]), reverse=True)
    return jsonify(sorted_matches)

if __name__ == '__main__':
    app.run(debug=True)

