import os
import csv
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__, template_folder='template2', static_folder='gambar1')

def fibonacci(n):
    fib_sequence = [1, 1]

    for i in range(2, n):
        fib_sequence.append(fib_sequence[i-1] + fib_sequence[i-2])

    return fib_sequence

@app.route("/")
def selamat_datang():
    return render_template('awal.html')


@app.route("/biodata/")
def biodata():
    return render_template('biodata.html')

@app.route("/cv/")
def cv():
    return render_template('CV.html')

@app.route("/portofolio/")
def portofolio():
    return render_template('porto.html')

@app.route("/fact/")
def fakta():
    return render_template('fact.html')

@app.route("/Media Sosial/")
def media():
    return render_template('media.html')

@app.route("/custom_fibonacci/", methods=['GET', 'POST'])
def custom_fibonacci_page():
    if request.method == 'POST':
        try:
            n = int(request.form['custom_length'])
            result = fibonacci(n)
            return render_template('fibonacci2.html', custom_length=n, result=result)
        except ValueError:
            error_message = "Masukkan angka valid."
            return render_template('fibonacci2.html', error_message=error_message)

    return render_template('fibonacci2.html')

@app.route("/csv_to_json", methods=["GET", "POST"])
def csv_to_json():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"

        file = request.files["file"]

        if file.filename == "":
            return "No selected file"

        allowed_extensions = {"csv"}
        if "." not in file.filename or file.filename.rsplit(".", 1)[1].lower() not in allowed_extensions:
            return "Invalid file type. Please upload a CSV file."

        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        json_data = convert_csv_to_json(file_path)

        return jsonify(json_data)

    return render_template("csv_to_json.html")

def convert_csv_to_json(file_path):
    with open(file_path, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        json_data = [row for row in csv_reader]

    return json_data

@app.route("/form_submit", methods=["POST"])
def form_submit():
    nama = request.form.get("nama")
    hubungan = request.form.get("hubungan")

    return redirect(url_for("halo", nama=nama, hubungan=hubungan))

@app.route("/halo")
def halo():
    nama = request.args.get("nama")
    hubungan = request.args.get("hubungan")

    return render_template('hasil.html', nama=nama, hubungan=hubungan)

if __name__ == "__main__":
    app.run(debug=True)
