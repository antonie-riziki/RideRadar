from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')


"""

Admin Views
"""

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


def admin_login(request):
    return render(request, 'admin_login.html')


def admin_register(request):
    return render(request, 'admin_register.html')


def admin_analytics(request):
    return render(request, 'admin_analytics.html')


def admin_fleet_tracking(request):
    return render(request, 'admin_fleet_tracking.html')


def admin_smart_recommendations(request):
    return render(request, 'admin_smart_recommendations.html')


"""
User Views
"""


def user_dashboard(request):
    return render(request, 'user_dashboard.html')


def user_login(request):
    return render(request, 'user_login.html')


def user_register(request):
    return render(request, 'user_register.html')


def user_live_tracking(request):
    return render(request, 'user_live_tracking.html')


def user_tickets(request):
    return render(request, 'user_tickets.html')


def user_ride_history(request):
    return render(request, 'user_trips.html')