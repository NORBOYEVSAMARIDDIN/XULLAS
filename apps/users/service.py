import os
import environ
import threading
from pathlib import Path
from django.core.mail import EmailMessage
from .utils import code_generate
from .models import Code, User

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

EMAIL_SENDER = env.str("EMAIL_HOST_USER")


def _send_email_with_code(to_email, user):
    code_value = code_generate()


    # Create code instance
    Code.objects.create(code=code_value, user=user)

    # Prepare email
    subject = "Sizga kod jo'natildi – 30 soniya ichida foydalaning"
    recipient_list = [to_email,]

    # Render HTML template
    html_message = f"""
    <div style="font-family: Arial, sans-serif; max-width: 500px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
        <h2 style="color: #333;">Salom, <span style="color: #007BFF;">{user.username}</span>!</h2>
        <p style="font-size: 16px; color: #555;">
            Quyidagi kod siz uchun yaratildi. Bu kod faqat <strong>30 soniya</strong> davomida ishlaydi.
        </p>
        <div style="background-color: #f2f2f2; padding: 15px; text-align: center; font-size: 24px; font-weight: bold; color: #333; border-radius: 8px;">
            {code_value}
        </div>
        <p style="font-size: 14px; color: #888; margin-top: 20px;">
            Agar siz bu so‘rovni amalga oshirmagan bo‘lsangiz, hech qanday harakat qilishingiz shart emas.
        </p>
    </div>
    """


    email = EmailMessage(subject, html_message, EMAIL_SENDER, recipient_list)
    email.content_subtype = "html"
    email.send(fail_silently=False)


def send_registration_code(to_email):
    user = User.objects.filter(email=to_email).first()
    if user:
        _send_email_with_code(to_email, user)
    else:
        raise ValueError(f"No user found with email {to_email}")


def send_change_email_code(to_email, current_user):
    if current_user:
        _send_email_with_code(to_email, current_user)
    else:
        raise ValueError("Current user is required")


def send_registration_code_async(to_email):
    thread = threading.Thread(target=send_registration_code, args=(to_email,))
    thread.start()


def send_change_email_code_async(to_email, current_user):
    thread = threading.Thread(target=send_change_email_code, args=(to_email, current_user,))
    thread.start()
