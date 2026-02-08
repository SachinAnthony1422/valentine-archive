from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import ValentineDay
from django.contrib.auth.decorators import login_required
from datetime import timedelta  # 👈 1. KEEP THIS IMPORT

@login_required
def home(request):
    days = ValentineDay.objects.order_by('date_to_unlock')
    
    # 👇 2. FORCE INDIA TIME (UTC + 5:30)
    # This manually adds 5.5 hours to whatever time the server thinks it is.
    today = (timezone.now() + timedelta(hours=5, minutes=30)).date()

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
    
    # 👇 3. FORCE INDIA TIME HERE TOO
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

            # SUCCESS: Default for Rose Day, Teddy Day, etc.
            return render(request, 'love_letter.html', {'day': day})
            
        else:
            return render(request, 'quiz.html', {'day': day, 'error': "Not quite! Try again, my love. 😉"})

    return render(request, 'quiz.html', {'day': day})