from django.urls import path
from . import views
from .utils import get_csrf_token

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('verify/<str:token>/', views.verify_email, name='verify_email'),
    path('submit-problem/', views.submit_problem, name='submit_problem'),
    path('problem/<int:problem_id>/add-solution/', views.add_solution, name='add_solution'),
    path('solution/<int:solution_id>/vote/', views.vote_solution, name='vote_solution'),
    path('my-problems/', views.my_problems, name='my_problems'),
    path('problem/<int:problem_id>/', views.problem_detail, name='problem_detail'),
    path('api/csrf-token/', get_csrf_token, name='api-csrf-token'),
]

handler404 = views.handler404
