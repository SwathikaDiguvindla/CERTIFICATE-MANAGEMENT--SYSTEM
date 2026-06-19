from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import sqlite3
import os
import uuid
import qrcode
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

# ---------- CONFIG ----------
CERT_FOLDER = "certificates"
QR_FOLDER = "qrcodes"
UPLOAD_FOLDER = "uploads"
DB_PATH = "certificates.db"

os.makedirs(CERT_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unique_id TEXT UNIQUE,
            name TEXT,
            email TEXT,
            phone TEXT,
            domain TEXT,
            start_date TEXT,
            end_date TEXT,
            pdf_path TEXT,
            qr_path TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_certificate_record(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO certificates 
        (unique_id, name, email, phone, domain, start_date, end_date, pdf_path, qr_path, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['unique_id'], data['name'], data['email'], data['phone'],
        data['domain'], data['start_date'], data['end_date'],
        data['pdf_path'], data['qr_path'], datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()


# ---------- CERTIFICATE GENERATION ----------
def generate_unique_id():
    return "CERT-" + uuid.uuid4().hex[:8].upper()


def generate_qr_code(unique_id):
    verify_url = f"http://127.0.0.1:5000/verify/{unique_id}"
    qr_img = qrcode.make(verify_url)
    qr_path = os.path.join(QR_FOLDER, f"{unique_id}.png")
    qr_img.save(qr_path)
    return qr_path


def generate_certificate_pdf(name, domain, start_date, end_date, unique_id, qr_path):
    pdf_path = os.path.join(CERT_FOLDER, f"{unique_id}.pdf")
    c = canvas.Canvas(pdf_path, pagesize=landscape(A4))
    width, height = landscape(A4)

    # Border
    c.setStrokeColor(colors.HexColor("#2c3e50"))
    c.setLineWidth(4)
    c.rect(20, 20, width - 40, height - 40)

    # Title
    c.setFont("Helvetica-Bold", 32)
    c.setFillColor(colors.HexColor("#2c3e50"))
    c.drawCentredString(width / 2, height - 100, "CERTIFICATE OF COMPLETION")

    # Subtitle
    c.setFont("Helvetica", 16)
    c.drawCentredString(width / 2, height - 150, "This certificate is proudly presented to")

    # Name
    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(colors.HexColor("#e74c3c"))
    c.drawCentredString(width / 2, height - 200, name)

    # Description
    c.setFont("Helvetica", 14)
    c.setFillColor(colors.black)
    c.drawCentredString(
        width / 2, height - 240,
        f"for successfully completing the {domain} program"
    )
    c.drawCentredString(
        width / 2, height - 265,
        f"from {start_date} to {end_date}"
    )

    # Unique ID
    c.setFont("Helvetica", 10)
    c.drawString(60, 60, f"Certificate ID: {unique_id}")

    # QR Code
    c.drawImage(qr_path, width - 160, 40, width=100, height=100)

    c.save()
    return pdf_path


# ---------- ROUTES ----------
@app.route('/')
def home():
    return redirect(url_for('admin_form'))


@app.route('/admin', methods=['GET', 'POST'])
def admin_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        domain = request.form['domain']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        unique_id = generate_unique_id()
        qr_path = generate_qr_code(unique_id)
        pdf_path = generate_certificate_pdf(name, domain, start_date, end_date, unique_id, qr_path)

        save_certificate_record({
            'unique_id': unique_id,
            'name': name,
            'email': email,
            'phone': phone,
            'domain': domain,
            'start_date': start_date,
            'end_date': end_date,
            'pdf_path': pdf_path,
            'qr_path': qr_path
        })

        flash(f"Certificate generated for {name}! ID: {unique_id}")
        return redirect(url_for('admin_form'))

    return render_template('admin_form.html')


@app.route('/admin/bulk', methods=['GET', 'POST'])
def bulk_upload():
    if request.method == 'POST':
        file = request.files.get('excel_file')
        if not file:
            flash("No file selected!")
            return redirect(url_for('bulk_upload'))

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        df = pd.read_excel(filepath)

        success_count = 0
        failed_count = 0
        failed_rows = []

        for index, row in df.iterrows():
            try:
                name = str(row['Name'])
                email = str(row['Email'])
                phone = str(row['Phone'])
                domain = str(row['Domain'])
                start_date = str(row['Start'])
                end_date = str(row['End'])

                unique_id = generate_unique_id()
                qr_path = generate_qr_code(unique_id)
                pdf_path = generate_certificate_pdf(name, domain, start_date, end_date, unique_id, qr_path)

                save_certificate_record({
                    'unique_id': unique_id,
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'domain': domain,
                    'start_date': start_date,
                    'end_date': end_date,
                    'pdf_path': pdf_path,
                    'qr_path': qr_path
                })
                success_count += 1
            except Exception as e:
                failed_count += 1
                failed_rows.append(f"Row {index + 2}: {str(e)}")

        flash(f"Bulk upload complete! Success: {success_count} | Failed: {failed_count}")
        if failed_rows:
            flash("Failed rows: " + "; ".join(failed_rows))

        return redirect(url_for('bulk_upload'))

    return render_template('bulk_upload.html')


@app.route('/download/<unique_id>')
def download_certificate(unique_id):
    return send_from_directory(CERT_FOLDER, f"{unique_id}.pdf", as_attachment=True)


@app.route('/verify/<unique_id>')
def verify_certificate(unique_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM certificates WHERE unique_id=?", (unique_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return f"<h2>✅ Valid Certificate</h2><p>Name: {row[2]}</p><p>Domain: {row[5]}</p>"
    return "<h2>❌ Certificate Not Found</h2>"


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
