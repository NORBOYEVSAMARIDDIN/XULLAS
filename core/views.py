import os
from django.views.static import serve
from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import render

def static_html(request, filename):
    html_dir = os.path.join(settings.BASE_DIR, 'static', 'html')
    return serve(request, filename + '.html', document_root=html_dir)

def render_html(request, filename):
    return render(request, f'{filename}.html')

def redirect_to_home(request):
    return redirect('users:login')