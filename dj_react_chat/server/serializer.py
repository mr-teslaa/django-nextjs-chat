from rest_framework import serializers
from .models import Server, Channel


class ChannelSerializer(serializers.ModelSerializer):
    """Serializer for Channel model.

    This serializer handles the serialization and deserialization of the Channel model.

    Attributes:
        Meta.model: The model class that this serializer is associated with.
        Meta.fields: Specifies which fields of the model should be included in the serialization.
    """

    class Meta:
        model = Channel
        fields = "__all__"


class ServerSerializer(serializers.ModelSerializer):
    """Serializer for Server model.

    This serializer handles the serialization and deserialization of the Server model, including nested serialization for related channels and a method field for the number of members.

    Attributes:
        num_members: A method field that provides the number of members in the server.
        channel_server: A nested serializer for related channels.

    Methods:
        get_num_members: Returns the number of members if available.
        to_representation: Custom representation to conditionally include the number of members.

    """

    num_members = serializers.SerializerMethodField()
    channel_server = ChannelSerializer(many=True)

    class Meta:
        model = Server
        fields = "__all__"

    def get_num_members(self, obj):
        """Retrieve the number of members in the server if available.

        Args:
            obj (Server): The server instance being serialized.

        Returns:
            int or None: The number of members or None if not available.
        """
        if hasattr(obj, "num_members"):
            return obj.num_members
        return None

    def to_representation(self, instance):
        """Customize the serialized representation.

        This method modifies the serialized data to conditionally include the number of members
        based on the context.

        Args:
            instance (Server): The server instance being serialized.

        Returns:
            dict: The serialized data for the server.
        """
        data = super().to_representation(instance)
        num_members = self.context.get("num_members")
        if not num_members:
            data.pop("num_members", None)
        return data
