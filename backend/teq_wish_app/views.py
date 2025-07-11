from django.shortcuts import render
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from teq_wish_app.models import *
from datetime import date
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from datetime import date
from email.mime.image import MIMEImage
import os
import json
import io
import zipfile
import base64


class Student(APIView):
    def post(self, request):
        di = {
            "name": request.data.get("name"),
            "regNo": request.data.get("regNo"),
            "email": request.data.get("email"),
            "dob": request.data.get("dob"),
            "image": request.data.get("image"),
            "created_at": datetime.now()
        }
        table.insert_one(di)
        return Response("data inserted")

    def get(self, request, *args, **kwargs):
        data = list(table.find({}, {"_id": 0}))
        return Response(data)

    def put(self, request, *args, **kwargs):
        regNo = kwargs.get("regNo")
        table.update_one(
            {'regNo': regNo},
            {
                "$set": {
                    "name": request.data.get("name"),
                    "email": request.data.get("email"),
                    "dob": request.data.get("dob"),
                    "image": request.data.get("image")
                }
            }
        )
        return Response("updated successfully")

    def delete(self, request, *args, **kwargs):
        regNo = kwargs.get("regNo")
        table.delete_one({"regNo": regNo})
        return Response("data deleted")


class student_update(APIView):
    def get(self, request, *args, **kwargs):
        regNo = kwargs.get("regNo")
        data = list(table.find({"regNo": regNo}, {"_id": 0}))
        return Response(data[0] if data else {})


# @csrf_exempt
# def send_birthday_emails(request):
#     if request.method != 'POST':
#         return JsonResponse({'error': 'Only POST method allowed'}, status=405)

#     try:
#         body_unicode = request.body.decode('utf-8')
#         if not body_unicode:
#             return JsonResponse({'error': 'Empty request body'}, status=400)

#         body = json.loads(body_unicode)
#         students = body.get('students', [])

#         if not students:
#             return JsonResponse({'error': 'No students provided'}, status=400)

#         for student in students:
#             name = student.get('name', 'Student')
#             email_address = student.get('email')

#             if not email_address:
#                 continue  # Skip if no email

#             subject = "🎂 Happy Birthday from T4TEQ!"
#             from_email = settings.DEFAULT_FROM_EMAIL
#             to_email = email_address

#             html_content = f"""
#                 <div style="font-family:Arial; padding:20px; border:1px solid #ddd;">
#                     <h2 style="color:#007BFF;">Happy Birthday, {name}!</h2>
#                     <p>Wishing you all the success, happiness, and health on your special day! 🎉</p>
#                     <img src="cid:poster" style="width:100%; max-width:400px; margin-top:20px;" />
#                     <p style="margin-top:20px;">- T4TEQ Team</p>
#                 </div>
#             """

#             email = EmailMessage(subject, html_content, from_email, [to_email])
#             email.content_subtype = 'html'

#             # Attach inline birthday image
#             image_path = os.path.join(settings.BASE_DIR, 'static', 'assests', 'image.jpeg')
#             if os.path.exists(image_path):
#                 with open(image_path, 'rb') as img:
#                     mime_img = MIMEImage(img.read())
#                     mime_img.add_header('Content-ID', '<poster>')
#                     mime_img.add_header('Content-Disposition', 'inline', filename='image.jpeg')
#                     email.attach(mime_img)

#             print(f"✅ Email sent to: {email_address}")
#             print(f"Sending birthday email to: {email_address}")
#             email.send()

#         return JsonResponse({'message': 'Birthday wishes sent successfully'}, status=200)

#     except json.JSONDecodeError:
#         return JsonResponse({'error': 'Invalid JSON format'}, status=400)
#     except Exception as e:
#         print("Email error:", str(e))
#         return JsonResponse({'error': 'Failed to send birthday emails'}, status=500)

####second version
@csrf_exempt
def send_birthday_emails(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    try:
        body_unicode = request.body.decode('utf-8').strip()

        # 🎯 Case 1: Empty body — Auto mode (for GitHub Actions)
        if not body_unicode:
            print("🌀 Auto mode triggered: No request body found.")
            today = date.today().strftime('%Y-%m-%d')
            students = list(table.find({"dob": today}, {"_id": 0}))
        else:
            # 🎯 Case 2: Manual mode (Postman)
            body = json.loads(body_unicode)
            students = body.get('students', [])

        if not students:
            return JsonResponse({'message': 'No students to wish today'}, status=200)

        for student in students:
            name = student.get('name', 'Student')
            email_address = student.get('email')

            if not email_address:
                continue  # Skip if no email

            subject = "🎂 Happy Birthday from T4TEQ!"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = email_address

            html_content = f"""
                <div style="font-family:Arial; padding:20px; border:1px solid #ddd;">
                    <h2 style="color:#007BFF;">Happy Birthday, {name}!</h2>
                    <p>Wishing you all the success, happiness, and health on your special day! 🎉</p>
                    <img src="cid:poster" style="width:100%; max-width:400px; margin-top:20px;" />
                    <p style="margin-top:20px;">- T4TEQ Team</p>
                </div>
            """

            email = EmailMessage(subject, html_content, from_email, [to_email])
            email.content_subtype = 'html'

            # Attach inline birthday image
            image_path = os.path.join(settings.BASE_DIR, 'static', 'assests', 'image.jpeg')
            if os.path.exists(image_path):
                with open(image_path, 'rb') as img:
                    mime_img = MIMEImage(img.read())
                    mime_img.add_header('Content-ID', '<poster>')
                    mime_img.add_header('Content-Disposition', 'inline', filename='image.jpeg')
                    email.attach(mime_img)

            print(f"✅ Email sent to: {email_address}")
            email.send()

        return JsonResponse({'message': 'Birthday wishes sent successfully'}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        print("💥 Email error:", str(e))
        return JsonResponse({'error': 'Failed to send birthday emails'}, status=500)


###third version
# from bson.regex import Regex  # Required for Regex query

# @csrf_exempt
# def send_birthday_emails(request):
#     if request.method != 'POST':
#         return JsonResponse({'error': 'Only POST method allowed'}, status=405)

#     try:
#         print("🎯 send_birthday_emails endpoint HIT", flush=True)

#         body_unicode = request.body.decode('utf-8').strip()

#         # 🎯 Auto mode — GitHub or UptimeRobot
#         if not body_unicode:
#             print("🌀 Auto mode triggered: No request body found.", flush=True)
#             today_md = date.today().strftime("-%m-%d")  # -MM-DD
#             students = list(table.find({"dob": Regex(f"{today_md}$")}, {"_id": 0}))
#             print(f"📦 Auto-mode students: {students}", flush=True)
#         else:
#             # 🎯 Manual mode
#             body = json.loads(body_unicode)
#             students = body.get('students', [])
#             print(f"🧪 Manual students: {students}", flush=True)

#         if not students:
#             print("📭 No students found to wish today.", flush=True)
#             return JsonResponse({'message': 'No students to wish today'}, status=200)

#         for student in students:
#             name = student.get('name', 'Student')
#             email_address = student.get('email')
#             if not email_address:
#                 print("⚠️ Skipping student with no email.", flush=True)
#                 continue

#             subject = "🎂 Happy Birthday from T4TEQ!"
#             from_email = settings.DEFAULT_FROM_EMAIL
#             to_email = email_address

#             html_content = f"""
#                 <div style="font-family:Arial; padding:20px; border:1px solid #ddd;">
#                     <h2 style="color:#007BFF;">Happy Birthday, {name}!</h2>
#                     <p>Wishing you all the success, happiness, and health on your special day! 🎉</p>
#                     <img src="cid:poster" style="width:100%; max-width:400px; margin-top:20px;" />
#                     <p style="margin-top:20px;">- T4TEQ Team</p>
#                 </div>
#             """

#             email = EmailMessage(subject, html_content, from_email, [to_email])
#             email.content_subtype = 'html'

#             # 🎁 Attach image
#             image_path = os.path.join(settings.BASE_DIR, 'static', 'assests', 'image.jpeg')
#             if os.path.exists(image_path):
#                 with open(image_path, 'rb') as img:
#                     mime_img = MIMEImage(img.read())
#                     mime_img.add_header('Content-ID', '<poster>')
#                     mime_img.add_header('Content-Disposition', 'inline', filename='image.jpeg')
#                     email.attach(mime_img)

#             print(f"✅ Email sent to: {email_address}", flush=True)
#             email.send()

#         return JsonResponse({'message': 'Birthday wishes sent successfully'}, status=200)

#     except json.JSONDecodeError:
#         print("❌ Invalid JSON format", flush=True)
#         return JsonResponse({'error': 'Invalid JSON format'}, status=400)
#     except Exception as e:
#         print("💥 Email error:", str(e), flush=True)
#         return JsonResponse({'error': 'Failed to send birthday emails'}, status=500)



@csrf_exempt
def download_students_zip(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    try:
        body_unicode = request.body.decode('utf-8')
        if not body_unicode:
            return JsonResponse({'error': 'Empty request body'}, status=400)

        students = json.loads(body_unicode)

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for student in students:
                name = student.get('name', 'unknown')
                reg_no = student.get('regNo', '')
                image_data = student.get('image', '')

                if image_data.startswith('data:image/'):
                    header, encoded = image_data.split(',', 1)
                    image_bytes = base64.b64decode(encoded)
                    ext = header.split('/')[1].split(';')[0]  # jpeg/png/etc.
                    filename = f"{name}_{reg_no}_image.{ext}"
                    zip_file.writestr(filename, image_bytes)

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=students.zip'
        return response

    except Exception as e:
        print("Download ZIP error:", str(e))
        return JsonResponse({'error': 'Failed to generate zip'}, status=500)
