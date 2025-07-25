import random

def code_generate():
    code = random.randint(1000, 9999)
    return code

def current_user(request):
    return request.user