from flask import Flask, render_template, request, send_file
import qrcode
from reportlab.pdfgen import canvas
from io import BytesIO
import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        airline = request.form["airline"]
        flight = request.form["flight"]
        from_loc = request.form["from"]
        to_loc = request.form["to"]
        date = request.form["date"]
        time = request.form["time"]
        seat = request.form["seat"]
        gate = request.form["gate"]
        ticket_id = "TK" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        data = {
            "Name": name,
            "Email": email,
            "Airline": airline,
            "Flight": flight,
            "From": from_loc,
            "To": to_loc,
            "Date": date,
            "Time": time,
            "Seat": seat,
            "Gate": gate,
            "Ticket No": ticket_id
        }

        # Create QR Code
        qr_data = "\n".join([f"{k}: {v}" for k, v in data.items()])
        qr_img = qrcode.make(qr_data)
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer)
        qr_buffer.seek(0)

        # Generate PDF
        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer)
        y = 800
        for key, val in data.items():
            c.drawString(50, y, f"{key}: {val}")
            y -= 30
        c.drawInlineImage(qr_buffer, 400, 600, width=150, height=150)
        c.save()
        pdf_buffer.seek(0)

        return send_file(pdf_buffer, download_name="flight_ticket.pdf", as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
