

from flask import Flask, request, render_template_string

app = Flask(__name__)

PAGE = """
<!doctype html>
<html>
<head><title>Student Grade Calculator</title></head>
<body>
<h2>Student Grade Calculator</h2>
<form method="post">
<input name="marks" placeholder="e.g. 80 90 70" required>
<button type="submit">Calculate</button>
</form>
{% if error %}<p>{{ error }}</p>{% endif %}
{% if result %}
<p>Total: {{ result.total }}</p>
<p>Average: {{ result.average }}</p>
{% endif %}
</body>
</html>
"""


def parse_marks(text):
    return [float(m) for m in text.replace(",", " ").split()]


def calculate_total(marks):
    return round(sum(marks), 2)


def calculate_average(marks):
    return round(sum(marks) / len(marks), 2)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    if request.method == "POST":
        try:
            marks = parse_marks(request.form["marks"])
            if not marks or any(m < 0 or m > 100 for m in marks):
                raise ValueError
            result = {
                "total": calculate_total(marks),
                "average": calculate_average(marks),
            }
        except ValueError:
            error = "Enter valid marks between 0 and 100, separated by spaces or commas."
    return render_template_string(PAGE, result=result, error=error)


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
