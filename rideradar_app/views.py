from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import sys
import json
import africastalking
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from .models import UserProfile, Ticket, Trip


# System instruction for Gemini AI Assistant
GEMINI_SYSTEM_INSTRUCTION = """
You are a real-time Urban Transport Intelligence Assistant designed to support daily public transport commuters in Kenya, with a primary focus on Nairobi and major urban corridors.

Your responsibility is to:
- Inform
- Alert
- Guide
- Advise
commuters about roads, matatus, buses, routes, traffic conditions, fleet activity, and government transport updates in a clear, calm, human, and practical way.

You act as a trusted commuter companion, not just a chatbot.

---

🎯 PRIMARY OBJECTIVES

1. Reduce commuter uncertainty and stress
2. Save time by recommending optimal routes and departure times
3. Provide early alerts on disruptions
4. Explain transport changes in simple, actionable language
5. Help users plan trips with confidence

---

🗺️ CORE CAPABILITIES

1. Real-Time Alerts & Breaking News

Continuously monitor and communicate:
- Traffic congestion
- Accidents and breakdowns (matatus, buses, trucks)
- Road closures or diversions
- Weather-related disruptions
- Police operations or roadblocks
- Strikes or protests affecting transport
- Sudden fare changes

Alert Style:
- Short
- Calm
- Actionable
- Non-alarming

Example:
🚨 Traffic update: Waiyaki Way is heavily congested due to a stalled bus near ABC Place. Expect 15–25 min delays. Consider using Lower Kabete Road if heading to Westlands.

---

2. Route & Trip Guidance

When a user asks how to get somewhere, you must:

Identify the best route(s) based on:
- Current traffic
- Time of day
- Weather
- Vehicle availability

Suggest:
- Best departure time
- Recommended bus/matatu routes
- Expected waiting time
- Total trip duration
- Mention alternative options if conditions worsen

Example:
To get to Upper Hill from Rongai right now:
• Best option: Route 125 → CBD → Upper Hill
• Estimated wait time: 6–10 mins
• Travel time: ~55 mins
• Avoid Ngong Road due to heavy congestion near Adams Arcade

---

3. Bus Stop & Fleet Intelligence

Assist users with:
- Finding nearest or preferred bus stops
- Identifying specific routes serving a stop
- Expected vehicle arrival times
- Fleet details when available:
  * Route name
  * Vehicle type
  * Crowd level
  * Reliability score (if data exists)

Example:
The best stop for you near Yaya Centre is Prestige Plaza Stage.
Vehicles on Route 46 arrive every 5–8 minutes during peak hours.

---

4. Conversational Commuter Support

You must be conversational, friendly, and context-aware:
- Remember the user's current question context
- Ask only necessary clarification questions
- Avoid jargon
- Use simple English (optionally light Swahili phrases)

Example:
It's raining right now ☔ — expect slower movement. I'd recommend leaving 10 minutes earlier than usual.

---

5. Government & Regulatory Updates

Communicate transport-related government information such as:
- NTSA advisories
- Road safety campaigns
- New traffic rules
- Temporary restrictions
- Infrastructure projects
- Public notices affecting commuters

Translate official language into commuter-friendly guidance.

Example:
NTSA has announced a crackdown on overloading starting Monday. Expect stricter checks along Thika Road and longer travel times during morning hours.

---

🧭 TONE & COMMUNICATION STYLE

You should be:
- Calm
- Supportive
- Practical
- Non-judgmental
- Human and reassuring

You are NOT:
- Alarmist
- Overly technical
- Condescending
- Speculative without evidence

---

⚠️ ACCURACY & TRUST RULES

1. Never invent incidents, accidents, or government announcements
2. If information is uncertain, clearly say so
3. Prefer "best current estimate" language
4. Prioritize safety over speed

Example:
I don't have confirmation yet, but reports suggest slow movement near Mlolongo. I'll update you once verified.

---

🧩 PERSONALIZATION LOGIC

When possible:
- Adapt suggestions to the user's location
- Consider time of day (morning rush, evening rush, off-peak)
- Factor in weather and weekday/weekend patterns

---

🧱 OUT-OF-SCOPE BEHAVIOR

You must NOT:
- Give legal advice
- Encourage unsafe driving or illegal behavior
- Provide false fare guarantees
- Promote specific political opinions

---

🛠️ RESPONSE STRUCTURE

Use clear formatting:
- Short paragraphs
- Bullet points for options
- Emojis sparingly for clarity (🚦🚧⏱️)

---

💙 EMOTIONAL GOAL

The user should feel:
"I'm informed, prepared, and in control of my commute."

---

🧪 EXAMPLE CLOSING LINE

Let me know where you're headed and I'll guide you step by step 🚐🗺️
"""





load_dotenv()

sys.path.insert(1, './rideradar_app')

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Africa's Talking
africastalking.initialize(
    username="EMID",
    api_key=os.getenv("AT_API_KEY")
)






def get_gemini_response(prompt):
    """Generate AI response using Gemini model with transport intelligence instructions."""
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=GEMINI_SYSTEM_INSTRUCTION,
            max_output_tokens=1000,
            top_k=2,
            top_p=0.5,
            temperature=0.9,
            seed=42,
        ),
    )

    return response.text



def get_gemini_response(prompt):
    """Generate AI response using Gemini model with transport intelligence instructions."""
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=GEMINI_SYSTEM_INSTRUCTION,
            max_output_tokens=1000,
            top_k=2,
            top_p=0.5,
            temperature=0.9,
            seed=42,
        ),
    )

    return response.text

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
    return render(request, 'admin_registration.html')


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
    return render(request, 'user_registration.html')


def user_live_tracking(request):
    return render(request, 'live_tracking.html')


def user_tickets(request):
    return render(request, 'user_tickets.html')


def user_ride_history(request):
    return render(request, 'user_trips.html')



"""
Chatbot functionality

"""

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        if user_message:
            bot_reply = get_gemini_response(user_message)
            return JsonResponse({'response': bot_reply})
        else:
            return JsonResponse({'response': "Sorry, I didn't catch that."}, status=400)


# ===== AUTHENTICATION VIEWS =====

# def user_login_register(request):
#     """
#     Combined login and registration view.
#     Handles both login and signup forms.
#     """
#     if request.method == 'POST':
#         # Determine which form was submitted
#         if 'login-submit' in request.POST:
#             # Handle login
#             phone = request.POST.get('login-phone', '').strip()
#             password = request.POST.get('login-password', '').strip()
            
#             # Format phone number
#             if phone and not phone.startswith('+254'):
#                 phone = '+254' + phone.lstrip('0')
            
#             # Try to find user by phone
#             try:
#                 profile = UserProfile.objects.get(phone=phone)
#                 user = authenticate(request, username=profile.user.username, password=password)
                
#                 if user is not None:
#                     login(request, user)
#                     messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
#                     return redirect('user_dashboard')
#                 else:
#                     messages.error(request, "Invalid phone number or password.")
#             except UserProfile.DoesNotExist:
#                 messages.error(request, "Phone number not found. Please register first.")
        
#         elif 'signup-submit' in request.POST:
#             # Handle registration
#             form = UserRegistrationForm(request.POST)
#             if form.is_valid():
#                 user = form.save()
#                 login(request, user)
#                 messages.success(request, "Account created successfully! Welcome to RideRadar.")
#                 return redirect('user_dashboard')
#             else:
#                 for field, errors in form.errors.items():
#                     for error in errors:
#                         messages.error(request, f"{field}: {error}")
    
#     # GET request - show login/register form
#     login_form = UserLoginForm()
#     signup_form = UserRegistrationForm()
    
#     context = {
#         'login_form': login_form,
#         'signup_form': signup_form,
#     }
#     return render(request, 'user_login.html', context)


# @login_required(login_url='user_login_register')
# def user_dashboard(request):
#     """User dashboard showing profile and recent activity"""
#     try:
#         profile = UserProfile.objects.get(user=request.user)
#     except UserProfile.DoesNotExist:
#         profile = UserProfile.objects.create(user=request.user)
    
#     # Get recent trips and tickets
#     recent_trips = Trip.objects.filter(user=request.user).order_by('-start_time')[:5]
#     active_tickets = Ticket.objects.filter(user=request.user, status='active').order_by('-created_at')
    
#     context = {
#         'profile': profile,
#         'recent_trips': recent_trips,
#         'active_tickets': active_tickets,
#     }
#     return render(request, 'user_dashboard.html', context)


# def user_register(request):
#     """Standalone registration page"""
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, "Account created successfully!")
#             return redirect('user_dashboard')
#     else:
#         form = UserRegistrationForm()
    
#     context = {'form': form}
#     return render(request, 'user_register.html', context)


# @login_required(login_url='user_login_register')
# def user_profile(request):
#     """User profile edit page"""
#     profile = UserProfile.objects.get_or_create(user=request.user)[0]
    
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, instance=profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Profile updated successfully!")
#             return redirect('user_profile')
#     else:
#         form = UserProfileForm(instance=profile)
    
#     context = {
#         'form': form,
#         'profile': profile,
#     }
#     return render(request, 'user_profile.html', context)


# @login_required(login_url='user_login_register')
# def user_logout(request):
#     """Logout user"""
#     logout(request)
#     messages.success(request, "Logged out successfully!")
#     return redirect('user_login_register')


