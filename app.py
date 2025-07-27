from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        total_days = int(request.form['total_days'])
        days_present = int(request.form['days_present'])

        if days_present > total_days:
            result = "Invalid Information: Days present can't be more than total days."
        else:
            percentage = (days_present / total_days) * 100
            result = f"The attendance percentage you have: {round(percentage, 2)}%"

        return render_template('result.html', title="Attendance %", result=result)

    return render_template('attendance.html')


@app.route('/required_days', methods=['GET', 'POST'])
def required_days():
    if request.method == 'POST':
        total_days = int(request.form['total_days'])
        attendance_percent = int(request.form['attendance_percentage'])

        days_75 = (75 / 100) * total_days
        days_current = (attendance_percent / 100) * total_days

        if days_current > days_75:
            result = "You already have more than 75% attendance."
        else:
            required = days_75 - days_current
            result = f"You have to attend {round(required)} more days to attain 75%."

        return render_template('result.html', title="75% Attendance Requirement", result=result)

    return render_template('required_days.html')


def convert_marks_to_grade_point(grade):
    grade_mapping = {
        "O": 10,
        "A+": 9,
        "A": 8,
        "B+": 7,
        "B": 6,
        "C": 5,
        "RA": 0,
        "SA": 0,
        "W": 0
    }
    return grade_mapping.get(grade.strip().upper())



@app.route("/gpa", methods=["GET", "POST"])
def gpa():
    if request.method == "POST":
        try:
            num_subjects = int(request.form["num_subjects"])
            credits = []
            grade_letters = []
            grade_points = []

            for i in range(1, num_subjects + 1):
                c = float(request.form[f"credits{i}"])
                grade_letter = request.form[f"marks{i}"].strip().upper()
                g = convert_marks_to_grade_point(grade_letter)

                if g is None:
                    raise ValueError(f"Invalid grade: {grade_letter}")

                credits.append(c)
                grade_letters.append(grade_letter)
                grade_points.append(g)

            total_points = sum(credits[i] * grade_points[i] for i in range(num_subjects))
            total_credits = sum(credits)
            gpa = round(total_points / total_credits, 2)

            return render_template("result.html", result=f"Your GPA is: {gpa}")
        except Exception as e:
            return render_template("result.html", result=f"Invalid input. Error: {str(e)}")

    return render_template("gpa.html")



if __name__ == '__main__':
    app.run(debug=True)
