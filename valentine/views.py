from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import ValentineDay

def home(request):
    # Get all the days you created in Admin
    # Sort them by date so Rose Day comes before Propose Day
    days = ValentineDay.objects.order_by('date_to_unlock')
    
    today = timezone.now().date()

    # --- NEW ADDITION: CALCULATE SCORE ---
    # Count how many days have a date less than or equal to today
    score = sum(1 for d in days if d.date_to_unlock <= today)
    
    context = {
        'days': days,
        'today': today,
        'score': score, # Sending the score to your new home.html
    }
    return render(request, 'home.html', context)

def unlock_day(request, day_id):
    day = get_object_or_404(ValentineDay, pk=day_id)
    today = timezone.now().date()
    
    # SECURITY CHECK 1: Is it too early?
    if day.date_to_unlock > today:
        # You can create a 'locked_too_early.html' or just redirect home
        return render(request, 'locked.html', {'day': day}) 

    # If she submits an answer
    if request.method == "POST":
        user_answer = request.POST.get('answer', '').strip().lower()
        correct_answer = day.correct_answer.strip().lower()
        
        # SECURITY CHECK 2: Is the password right?
        if user_answer == correct_answer:
            
            # --- SPECIAL: PROPOSE DAY LOGIC (Feb 8) ---
            # If the answer is right AND it is Propose Day, show the magic screen
            if day.date_to_unlock.day == 8 and day.date_to_unlock.month == 2:
                return render(request, 'propose.html', {'day': day})

            # SUCCESS: Show the normal love letter page for other days
            return render(request, 'love_letter.html', {'day': day})
            
        else:
            # FAILURE: Show error message
            return render(request, 'quiz.html', {'day': day, 'error': "Not quite! Try again, my love. 😉"})

    # Default: Show the Question Page
    return render(request, 'quiz.html', {'day': day})