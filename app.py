from flask import Flask, request, render_template, send_file
import qrcode
from barcode import Code128
from barcode.writer import ImageWriter
import os

# Initialize Flask app
app = Flask(__name__)

# Folder to store generated files
UPLOAD_FOLDER = "./codes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route for the main page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get the form data
        data = request.form.get("data")
        code_type = request.form.get("code_type")

        # Validate the data length
        if len(data) > 6:
            return render_template("index.html", error="Data exceeds 6 characters. Please try again.")

        # Generate file path for saving the code
        output_file = os.path.join(UPLOAD_FOLDER, f"{code_type}_{data}.png")

        # Generate QR code or barcode based on user selection
        if code_type == "qr":
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill="black", back_color="white")
            img.save(output_file)
        elif code_type == "barcode":
            barcode = Code128(data, writer=ImageWriter())
            barcode.save(os.path.splitext(output_file)[0])

        # Serve the generated file for download
        return send_file(output_file, as_attachment=True)

    return render_template("index.html", error=None)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
