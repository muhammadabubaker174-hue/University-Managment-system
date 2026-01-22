
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

students = {}
marks = {}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/students")
def students_page():
    return render_template("students.html")

@app.route("/marks")
def marks_page():
    return render_template("marks.html")

@app.route("/edit")
def edit_page():
    return render_template("edit.html")

@app.route("/gpa")
def gpa_page():
    return render_template("gpa.html")

@app.route("/courses")
def course_page():
    return render_template("courses.html")

@app.route("/about")
def gpa_about():
    return render_template("about.html")

# ---------------- ADD STUDENT ----------------
@app.route("/add-student", methods=["POST"])
def add_student():
    data = request.json
    roll = data["roll"]

    students[roll] = {
        "name": data["name"],
        "department": data["department"],
        "course": data["course"],
        "section": data["section"],
        "semester": data["semester"]
    }
    return jsonify({"message": "Student Added Successfully"})
@app.route("/all-students")
def all_students():
    data = []
    for roll, s in students.items():
        data.append({
            "roll": roll,
            "name": s["name"],
            "department": s["department"],
            "course": s["course"],
            "section": s["section"],
            "semester": s["semester"]
        })
    return jsonify(data)

# ---------------- GET STUDENT ----------------
@app.route("/student/<roll>")
def get_student(roll):
    return jsonify({
        "student": students.get(roll),
        "marks": marks.get(roll)
    })

# ---------------- SAVE MARKS ----------------
@app.route("/save-marks", methods=["POST"])
def save_marks():
    data = request.json
    roll = data["roll"]

    marks[roll] = {
        "calculus": int(data["calculus"]),
        "physics": int(data["physics"]),
        "dm": int(data["dm"]),
        "aict": int(data["aict"]),
        "pf": int(data["pf"])
    }
    return jsonify({"message": "Marks Saved Successfully"})

@app.route("/edit-data")
def edit_data():
    result = []

    for roll, student in students.items():
        m = marks.get(roll, {})
        result.append({
            "roll": roll,
            "name": student["name"],
            "course": student["course"],
            "section": student.get("section", ""),
            "calculus": m.get("calculus", ""),
            "physics": m.get("physics", ""),
            "dm": m.get("dm", ""),
            "aict": m.get("aict", ""),
            "pf": m.get("pf", "")
        })

    return jsonify(result)
# ---------------- GPA ----------------
@app.route("/gpa")
def calculate_gpa(marks):
    avg = sum(marks.values()) / len(marks)
    gpa = round(avg / 25, 2)

    if gpa >= 3.5:
        grade = "A"
    elif gpa >= 3:
        grade = "B"
    elif gpa >= 2:
        grade = "C"
    else:
        grade = "F"

    return gpa, grade

    return jsonify(result)
@app.route("/gpa-data")
def gpa_data():
    result = []

    for roll, student in students.items():
        if roll in marks:
            gpa, grade = calculate_gpa(marks[roll])
        else:
            gpa, grade = "", ""

        result.append({
            "roll": roll,
            "name": student["name"],
            "course": student["course"],
            "semester": student["semester"],
            "gpa": gpa,
            "grade": grade
        })

    return jsonify(result)
if __name__ == "__main__":
    app.run(debug=True)