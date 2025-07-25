
from django.core.mail import send_mail, EmailMessage
import threading
from .utils import code_generate
from .models import Code, User

import os
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

def send_simple_email(to):
    code_value = code_generate()
    user = User.objects.filter(email=to).first()
    code = Code.objects.create(code=code_value, user=user)

    subject = "Sizga kod jo'natildi – 30 soniya ichida foydalaning"
    from_email = env.str("EMAIL_HOST_USER")
    recipient_list = [to]

    html_message = f"""
    <div style="font-family: Arial, sans-serif; max-width: 500px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
        <h2 style="color: #333;">Salom, <span style="color: #007BFF;">{user.username}</span>!</h2>
        <p style="font-size: 16px; color: #555;">
            Quyidagi kod siz uchun yaratildi. Bu kod faqat <strong>30 soniya</strong> davomida ishlaydi.
        </p>
        <div style="background-color: #f2f2f2; padding: 15px; text-align: center; font-size: 24px; font-weight: bold; color: #333; border-radius: 8px;">
            {code.code}
        </div>
        <p style="font-size: 14px; color: #888; margin-top: 20px;">
            Agar siz bu so‘rovni amalga oshirmagan bo‘lsangiz, hech qanday harakat qilishingiz shart emas.
        </p>
    </div>
    """

    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = "html"  # Set content to HTML
    email.send(fail_silently=False)

def send_email_in_thread(to):
    thread = threading.Thread(target=send_simple_email, args=(to,))
    thread.start()
