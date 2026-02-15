from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import ValentineDay
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import timedelta

@login_required
def home(request):
    days = ValentineDay.objects.order_by('date_to_unlock')
    
    # Force India Time (UTC + 5:30)
    today = (timezone.now() + timedelta(hours=5, minutes=30)).date()
    
    # Calculate score (days unlocked)
    score = sum(1 for d in days if d.date_to_unlock <= today)
    
    context = {
        'days': days,
        'today': today,
        'score': score,
    }
    return render(request, 'home.html', context)

@login_required
def unlock_day(request, day_id):
    day = get_object_or_404(ValentineDay, pk=day_id)
    
    # Force India Time
    today = (timezone.now() + timedelta(hours=5, minutes=30)).date()
    
    # SECURITY CHECK 1: Is it too early?
    if day.date_to_unlock > today:
        return render(request, 'locked.html', {'day': day})

    if request.method == "POST":
        user_answer = request.POST.get('answer', '').strip().lower()
        correct_answer = day.correct_answer.strip().lower()
        
        # SECURITY CHECK 2: Is the password right?
        if user_answer == correct_answer:
            
            # --- SPECIAL: PROPOSE DAY LOGIC ---
            if "Propose" in day.title:
                return render(request, 'propose.html', {'day': day})

            # --- SPECIAL: CHOCOLATE DAY LOGIC ---
            elif "Chocolate" in day.title:
                return render(request, 'chocolate.html', {'day': day})

            # --- SPECIAL: TEDDY DAY LOGIC ---
            elif "Teddy" in day.title:
                return render(request, 'teddy.html', {'day': day})

            # --- SPECIAL: PROMISE DAY LOGIC ---
            elif "Promise" in day.title:
                # We pass 'today' so the certificate date is correct
                return render(request, 'promise.html', {'day': day, 'today': today})

            # --- SPECIAL: KISS DAY LOGIC ---
            elif "Kiss" in day.title:
                # Instead of showing a page directly, we start the journey!
                return redirect('hug_reveal') 

            # --- SPECIAL: VALENTINE DAY LOGIC (GRAND FINALE) ---
            elif "Valentine" in day.title:
                # Clear any old game session data so she starts fresh
                if 'played_game' in request.session:
                    del request.session['played_game']
                return redirect('valentine_start')

            # SUCCESS: Default for Rose Day, etc.
            return render(request, 'love_letter.html', {'day': day})
            
        else:
            return render(request, 'quiz.html', {'day': day, 'error': "Not quite! Try again, my love. 😉"})
            
    return render(request, 'quiz.html', {'day': day})

# Standalone views
def teddy(request):
    return render(request, 'teddy.html')

def promise(request):
    today = (timezone.now() + timedelta(hours=5, minutes=30)).date()
    return render(request, 'promise.html', {'today': today})

# 👇 EXISTING JOURNEY VIEWS 👇

def hug_reveal(request):
    return render(request, 'hug_reveal.html')

def kiss_reveal(request):
    return render(request, 'kiss_reveal.html')

# 👇 NEW GRAND FINALE VIEWS 👇

def valentine_start(request):
    # Stage 1: The Entrance & Question
    return render(request, 'finale/1_start.html')

def valentine_game(request):
    # Stage 2: The "No" Penalty Game
    if request.method == "POST":
        # Mark that she finished the game successfully
        request.session['played_game'] = True
        return JsonResponse({'status': 'success'})
    return render(request, 'finale/2_game.html')

def valentine_quiz(request):
    # Stage 3: The KPI Quiz
    # Security: If she tried to skip the game after saying NO, send her back
    # (We check if 'said_no' was passed in GET, or rely on session logic if needed)
    return render(request, 'finale/3_quiz.html')

def valentine_doors(request):
    # Stage 4: The 3 Doors
    return render(request, 'finale/4_doors.html')

def valentine_teddy(request):
    # Stage 5: The Teddy & Heart Reveal
    return render(request, 'finale/5_teddy.html')

def valentine_gallery(request):
    # Stage 6: The Hanging Gallery
    return render(request, 'finale/6_gallery.html')

def valentine_finale(request):
    # Stage 7: The Final Memory Archive
    # We will pass ALL the days to this template so we can show every photo
    days = ValentineDay.objects.order_by('date_to_unlock')
    return render(request, 'finale/7_finale.html', {'days': days})