from datetime import datetime
from pathlib import Path
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from pymongo import MongoClient

# MongoDB connection
username = "anusha"
password = "anusha@43"
uri = f"mongodb+srv://{username}:{password}@cluster0.q66bcnr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
connection = MongoClient(uri)
db = connection["teq_wish_db"]                         # Use your actual DB name
table = db["student_datas"]                              # Your collection

def log(msg):
    with open("mail_log.txt", "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

def mailsend():
    today = datetime.today()
    today_str = today.strftime("%d-%m")
    img_path =" C://Users//User//Desktop//kattur pro//teq_wish//static//assests//image.jpeg"

    # Get all students and filter in Python
    birthday_data = list(table.find({}, {"_id": 0, "name": 1, "email": 1, "dob": 1}))
    
    for student in birthday_data:
        dob = student.get("dob", "")
        # Match the DD-MM part of the dob
        if dob and dob[:5] == today_str:
            name = student["name"]
            email_id = student["email"]

            subject = "🎉 Happy Birthday!"
            text_message = f"Dear {name},\nWishing you a fantastic birthday!"

            html_message = f"""
                <html>
                    <body style="font-family:Arial; background-color:#f9f9f9; padding:20px;">
                        <div style="background-color:#ffffff; border-radius:10px; padding:20px; box-shadow:0 0 10px rgba(0,0,0,0.1);">
                            <h2 style="color:#ff4081;">Happy Birthday, {name}! 🎂</h2>
                            <p>Wishing you a day charged with curiosity,<br>
                            compiled with joy, and debugged of worries. 💻✨🚀</p>
                            <img src="cid:birthday_image" alt="Birthday Image" style="max-width:100%; border-radius:8px;" />
                        </div>
                    </body>
                </html>
            """

            try:
                email = EmailMultiAlternatives(
                    subject,
                    text_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email_id]
                )
                email.attach_alternative(html_message, "text/html")

                with open(img_path, "rb") as img:
                    mime_img = MIMEImage(img.read())
                    mime_img.add_header("Content-ID", "<birthday_image>")
                    mime_img.add_header("Content-Disposition", "inline", filename="image.jpeg")
                    email.attach(mime_img)

                email.send()
                log(f"✅ Birthday email sent to {email_id}")
            except Exception as e:
                log(f"❌ Error sending to {email_id}: {e}")