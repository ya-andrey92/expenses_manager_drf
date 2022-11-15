from djoser.serializers import UserSerializer


class CustomUserSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        meta_data = UserSerializer.Meta
        fields = meta_data.fields + ('first_name', 'last_name', 'balance')
        read_only_fields = meta_data.read_only_fields + ('balance', )
