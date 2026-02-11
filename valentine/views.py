from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import ValentineDay
from django.contrib.auth.decorators import login_required
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

            # --- SPECIAL: PROMISE DAY LOGIC (✅ ADDED THIS!) ---
            elif "Promise" in day.title:
                # We pass 'today' so the certificate date is correct
                return render(request, 'promise.html', {'day': day, 'today': today})

            # SUCCESS: Default for Rose Day, etc.
            return render(request, 'love_letter.html', {'day': day})
            
        else:
            return render(request, 'quiz.html', {'day': day, 'error': "Not quite! Try again, my love. 😉"})
            
    return render(request, 'quiz.html', {'day': day})

# Standalone views (kept as requested)
def teddy(request):
    return render(request, 'teddy.html')

def promise(request):
    today = (timezone.now() + timedelta(hours=5, minutes=30)).date() # Ensure India time consistency
    return render(request, 'promise.html', {'today': today})