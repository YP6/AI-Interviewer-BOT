from rest_framework.serializers import ModelSerializer
from ..models import User
class UserSerializer(ModelSerializer):
    id = 'sadf'
    class Meta:
        model = User
        fields = '__all__'