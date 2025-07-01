from django.contrib import admin
from .models import User, Problem, Solution, Vote, EmailVerificationToken

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'is_verified', 'date_joined', 'is_staff')
    list_filter = ('is_verified', 'is_staff', 'is_superuser')
    search_fields = ('email', 'full_name')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login')

@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at', 'is_expired')
    list_filter = ('expired', 'created_at')
    search_fields = ('user__email', 'token')
    readonly_fields = ('created_at',)

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date_reported', 'solutions_count')
    list_filter = ('date_reported',)
    search_fields = ('title', 'description')
    ordering = ('-date_reported',)
    readonly_fields = ('date_reported',)

    def solutions_count(self, obj):
        return obj.solutions.count()
    solutions_count.short_description = 'Solutions'

@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('problem', 'user', 'created_at', 'votes_count')
    list_filter = ('created_at',)
    search_fields = ('text', 'problem__title')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    def votes_count(self, obj):
        return obj.votes.count()
    votes_count.short_description = 'Votes'

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('solution', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'solution__text')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
