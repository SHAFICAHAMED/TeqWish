from django.shortcuts import render
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from email.mime.image import MIMEImage
import json
import io
import zipfile
import base64
import os

from teq_wish_app.models import table


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
        table.update_one({'regNo': regNo}, {
            "$set": {
                "name": request.data.get("name"),
                "email": request.data.get("email"),
                "dob": request.data.get("dob"),
                "image": request.data.get("image")
            }
        })
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


@csrf_exempt
def send_birthday_emails(request):
    try:
        body = json.loads(request.body)
        students = body.get('students', [])
        if not students:
            return JsonResponse({'error': 'No students provided'}, status=400)

        for student in students:
            subject = "🎂 Happy Birthday from T4TEQ!"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = student['email']

            html_content = f"""
                <div style="font-family:Arial; padding:20px; border:1px solid #ddd;">
                    <h2 style="color:#007BFF;">Happy Birthday, {student['name']}!</h2>
                    <p>Wishing you all the success, happiness, and health on your special day! 🎉</p>
                    <img src="cid:poster" style="width:100%; max-width:400px; margin-top:20px;" />
                    <p style="margin-top:20px;">- T4TEQ Team</p>
                </div>
            """

            email = EmailMessage(subject, html_content, from_email, [to_email])
            email.content_subtype = 'html'

            # Use relative static image path
            image_path = os.path.join(settings.BASE_DIR, 'static', 'assests', 'image.jpeg')
            with open(image_path, 'rb') as img:
                mime_img = MIMEImage(img.read())
                mime_img.add_header('Content-ID', '<poster>')
                mime_img.add_header('Content-Disposition', 'inline', filename='image.jpeg')
                email.attach(mime_img)

            email.send()

        return JsonResponse({'message': 'Birthday wishes sent'}, status=200)

    except Exception as e:
        print(f"❌ Error sending birthday wishes: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def download_students_zip(request):
    try:
        students = json.loads(request.body)
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for student in students:
                name = student.get('name', 'unknown')
                reg_no = student.get('regNo', '')
                image_data = student.get('image', '')

                if image_data.startswith('data:image/'):
                    header, encoded = image_data.split(',', 1)
                    image_bytes = base64.b64decode(encoded)
                    ext = header.split('/')[1].split(';')[0]
                    zip_file.writestr(f"{name}_{reg_no}_image.{ext}", image_bytes)

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=students.zip'
        return response

    except Exception as e:
        print("❌ Error creating ZIP:", e)
        return HttpResponse('Failed to generate zip', status=500)
