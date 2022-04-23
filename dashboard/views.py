from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# from infrastructure.models import InfoNVR, PanelInfo, CCTV
# from setting.models import Branch
# from staff.models import Profile
import threading

# Create your views here.
@login_required(login_url="homepage")
def dashboard(request):
    context = {}
    return render(request, 'dashboard/dashboard.html', context)
