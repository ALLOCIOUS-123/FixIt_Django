from rest_framework import serializers
from .models import User, Problem, Solution, Vote

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_verified', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class ProblemSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    solutions_count = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = ['id', 'user', 'title', 'description', 'photo', 'latitude', 'longitude', 
                 'date_reported', 'solutions_count']
        read_only_fields = ['id', 'user', 'date_reported']

    def get_solutions_count(self, obj):
        return obj.solutions.count()

class SolutionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    votes_count = serializers.SerializerMethodField()

    class Meta:
        model = Solution
        fields = ['id', 'problem', 'user', 'text', 'votes_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_votes_count(self, obj):
        return obj.votes.count()

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'solution', 'user', 'created_at']
        read_only_fields = ['id', 'created_at']
