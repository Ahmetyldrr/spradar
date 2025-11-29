"""
🎯 Django REST Framework Serializers
"""

from rest_framework import serializers
from .models import LeagueComebackSummary, DailyMatchCommentary, ComprehensiveComebackAnalysis, MatchChatHistory


class LeagueComebackSummarySerializer(serializers.ModelSerializer):
    """League Comeback Summary için serializer"""
    
    class Meta:
        model = LeagueComebackSummary
        fields = '__all__'


class DailyMatchCommentarySerializer(serializers.ModelSerializer):
    """Daily Match Commentary için serializer"""
    
    class Meta:
        model = DailyMatchCommentary
        fields = '__all__'


class ComprehensiveComebackAnalysisSerializer(serializers.ModelSerializer):
    """Comprehensive Comeback Analysis için serializer"""
    
    class Meta:
        model = ComprehensiveComebackAnalysis
        fields = '__all__'


class MatchChatHistorySerializer(serializers.ModelSerializer):
    """Match Chat History için serializer"""
    
    class Meta:
        model = MatchChatHistory
        fields = ['id', 'match_id', 'user_message', 'ai_response', 'created_at']
        read_only_fields = ['id', 'created_at']


class ChatRequestSerializer(serializers.Serializer):
    """Chat request için serializer"""
    message = serializers.CharField(required=True, max_length=2000)
