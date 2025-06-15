from rest_framework import serializers
from students.models import Session

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('id', 'subject', 'start_time', 'duration', 'mode', 'video_url')