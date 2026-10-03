from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Configure Jenkins", "completed": True},
    {"id": 2, "title": "Build DevOps Pipeline", "completed": False}
]


@app.route("/")
def home():
    return jsonify({
        "application": "TaskFlow API",
        "version": "1.0.0",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({"error": "Task title is required"}), 400

    task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "completed": False
    }

    tasks.append(task)
    return jsonify(task), 201


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
