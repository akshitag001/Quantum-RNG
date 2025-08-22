from flask import Flask, render_template, request, send_file
from qrng.generator import random_array
import pandas as pd
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    numbers = []
    error_msg = ""
    if request.method == "POST":
        try:
            # Safely get form values with defaults
            num = int(request.form.get("num") or 10)
            low = int(request.form.get("low") or 1)
            high = int(request.form.get("high") or 100)
            
            if low > high:
                raise ValueError("Minimum value cannot be greater than maximum value")
            
            # Generate quantum random numbers
            numbers = random_array(size=num, low=low, high=high)
            
            # If user wants CSV download
            if request.form.get("download") == "yes":
                df = pd.DataFrame(numbers, columns=["Quantum Random Numbers"])
                buffer = io.StringIO()
                df.to_csv(buffer, index=False)
                buffer.seek(0)
                return send_file(
                    io.BytesIO(buffer.getvalue().encode()),
                    mimetype="text/csv",
                    as_attachment=True,
                    download_name="quantum_numbers.csv"
                )
        except Exception as e:
            error_msg = f"Error: {e}"
    
    return render_template("index.html", numbers=numbers, error=error_msg)

if __name__ == "__main__":
    app.run(debug=True)


