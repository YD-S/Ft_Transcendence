from chat.models import Message, Room
from utils.modelserializer import ModelSerializer


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'content',
            'sender',
            'sender_id',
            'room',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ('sender', 'sender_id', 'room', 'created_at', 'updated_at')

    def serialize_sender(self, obj):
        return obj.username


class RoomSerializer(ModelSerializer):

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    class Meta:
        model = Room
        fields = [
            'id',
            'name',
            'members',
            'messages',
            'created_at',
            'updated_at',
            'code',
            'is_direct'
        ]
        read_only_fields = ('members', 'messages', 'created_at', 'updated_at', 'is_direct', 'code')

    def serialize_name(self, obj):
        if self.user:
            return self.instance.get_name(self.user)
        return self.instance.name

    def serialize_members(self, obj):
        return [member.username for member in obj.all()]

    def serialize_messages(self, obj):
        return [MessageSerializer(instance=message).data for message in obj.all()]
