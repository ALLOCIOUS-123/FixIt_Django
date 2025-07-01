from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from .models import User, Problem, Solution, Vote, EmailVerificationToken
from .forms import ProblemForm, SolutionForm
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404

def handler404(request, exception):
    return render(request, '404.html', status=404)

@login_required
def dashboard(request):
    # Get user's recent activity
    recent_activity = []
    
    # Get recent problems submitted by the user
    recent_problems = Problem.objects.filter(user=request.user).order_by('-date_reported')[:5]
    for problem in recent_problems:
        recent_activity.append({
            'action': 'Submitted a new problem',
            'description': f'Added "{problem.title}" to the community',
            'timestamp': problem.date_reported
        })
    
    # Get recent solutions submitted by the user
    recent_solutions = Solution.objects.filter(user=request.user).order_by('-created_at')[:5]
    for solution in recent_solutions:
        recent_activity.append({
            'action': 'Submitted a solution',
            'description': f'Added a solution to "{solution.problem.title}"',
            'timestamp': solution.created_at
        })
    
    # Sort activity by timestamp
    recent_activity.sort(key=lambda x: x['timestamp'], reverse=True)
    
    context = {
        'recent_activity': recent_activity
    }
    return render(request, 'dashboard.html', context)

def home(request):
    # Get recent problems
    recent_problems = Problem.objects.all().order_by('-date_reported')[:5]
    
    context = {
        'recent_problems': recent_problems
    }
    return render(request, 'home.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        next_url = request.GET.get('next', 'dashboard')
        
        if not email or not password:
            messages.error(request, "Please enter both email and password.")
            return redirect("login")
            
        try:
            user = User.objects.get(email=email)
            
            if not user.is_active:
                messages.error(request, "Please verify your email address first. Check your inbox for the verification link.")
                return redirect("login")
                
            if not user.check_password(password):
                messages.error(request, "Invalid password.")
                return redirect("login")
                
            login(request, user)
            messages.success(request, "Login Successful!")
            return redirect(next_url)
            
        except User.DoesNotExist:
            messages.error(request, "Account not found. Please check your email or sign up first.")
            return redirect("login")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect("login")
    
    return render(request, "registration/login.html")

def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        if not email or not password or not full_name:
            messages.error(request, "All fields are required.")
            return redirect("signup")
            
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please log in.")
            return redirect("login")
        
        if len(full_name) < 2:
            messages.error(request, "Full name must be at least 2 characters long.")
            return redirect("signup")
        
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect("signup")
        
        try:
            # Create user
            user = User.objects.create_user(
                email=email, 
                password=password,
                full_name=full_name
            )
            user.is_active = False  # Deactivate until verified
            user.save()
            
            # Generate verification token
            token = get_random_string(length=32)
            
            # Check if token already exists and delete it
            EmailVerificationToken.objects.filter(user=user).delete()
            
            # Create new token
            verification_token = EmailVerificationToken.objects.create(
                user=user,
                token=token
            )
            
            # Send verification email
            verification_url = f"{settings.FRONTEND_URL}/verify/{token}/"
            subject = "Verify Your FixItHub Account"
            
            # Load HTML template
            html_message = render_to_string('emails/verification_email.html', {
                'verification_url': verification_url,
                'full_name': full_name
            })
            
            send_mail(
                subject,
                'Please verify your email address by clicking the link in the email.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
                html_message=html_message
            )
            
            messages.success(request, "Account created! Please check your email to verify your account.")
            return redirect("login")
            
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
            return redirect("signup")
    
    return render(request, "registration/signup.html")

def verify_email(request, token):
    try:
        # Find the token
        verification = EmailVerificationToken.objects.get(token=token)
        
        # Check if token has expired
        if (timezone.now() - verification.created_at).total_seconds() > settings.EMAIL_VERIFICATION_EXPIRY:
            verification.delete()
            messages.error(request, "Verification link has expired. Please request a new verification email.")
            return redirect("login")
            
        user = verification.user
        
        # Activate the user
        user.is_active = True
        user.save()
        
        # Delete the token
        verification.delete()
        
        messages.success(request, "Email verified successfully! You can now log in.")
        return redirect(settings.EMAIL_VERIFICATION_REDIRECT_URL)
        
    except EmailVerificationToken.DoesNotExist:
        messages.error(request, "Invalid verification link.")
        return redirect("login")

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def my_problems(request):
    problems = Problem.objects.filter(user=request.user).order_by('-date_reported')
    return render(request, 'my_problems.html', {'problems': problems})

@login_required
def add_solution(request, problem_id):
    if request.method == 'POST':
        problem = Problem.objects.get(id=problem_id)
        solution_text = request.POST.get('text')
        
        if solution_text:
            Solution.objects.create(
                problem=problem,
                user=request.user,
                text=solution_text
            )
            return JsonResponse({'status': 'success'})
        
    return JsonResponse({'status': 'error', 'message': 'Solution text is required'})

@login_required
def vote_solution(request, solution_id):
    if request.method == 'POST':
        solution = Solution.objects.get(id=solution_id)
        
        # Check if user has already voted
        existing_vote = Vote.objects.filter(solution=solution, user=request.user).first()
        
        if existing_vote:
            return JsonResponse({'status': 'error', 'message': 'You have already voted for this solution'})
        
        # Create new vote
        Vote.objects.create(
            solution=solution,
            user=request.user
        )
        
        # Update solution vote count
        solution.votes = solution.vote_set.count()
        solution.save()
        
        return JsonResponse({
            'status': 'success',
            'votes': solution.votes
        })
        
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def submit_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST, request.FILES)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.user = request.user
            problem.save()
            return redirect('home')
    else:
        form = ProblemForm()
    
    return render(request, 'submit_problem.html', {'form': form})

@login_required
def problem_detail(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    solutions = Solution.objects.filter(problem=problem).order_by('-votes', '-created_at')
    
    if request.method == 'POST':
        text = request.POST.get('solution_text')
        if text:
            Solution.objects.create(
                problem=problem,
                user=request.user,
                text=text
            )
            return redirect('problem_detail', problem_id=problem_id)
    
    context = {
        'problem': problem,
        'solutions': solutions,
        'can_add_solution': problem.user != request.user
    }
    return render(request, 'problem_detail.html', context)

def home(request):
    return render(request, 'home.html')
