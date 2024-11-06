# dj_react_chat\server\models.py

from django.db import models
from django.conf import settings


class Category(models.Model):
    """
    Represents a category that servers can belong to.

    Attributes:
        name (str): The name of the category.
        description (str): An optional description of the category.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Server(models.Model):
    """
    Represents a server which can have multiple members and belong to a category.

    Attributes:
        name (str): The name of the server.
        owner (User): The owner of the server.
        category (Category): The category the server belongs to.
        description (str): An optional description of the server.
        members (User[]): The members of the server.

    Query Parameters:
        - category (str): The name of the category to filter by.
        - by_user (bool): Whether to filter by the current user.
        - by_server_id (str): The ID of the server to filter by.
        - with_num_members (bool): Whether to include the number of members in the response.
    """

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="server_owner"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="server_category"
    )
    description = models.CharField(max_length=500, blank=True, null=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="server_members"
    )

    def __str__(self):
        return f"Name: {self.name} | Id: {self.id}"


class Channel(models.Model):
    """
    Represents a communication channel within a server.

    Attributes:
        name (str): The name of the channel.
        owner (User): The owner of the channel.
        topic (str): The topic of the channel.
        server (Server): The server the channel belongs to.
    """

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="channel_owner"
    )
    topic = models.CharField(max_length=500)
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name="channel_server"
    )

    def save(self, *args, **kwargs):
        # Ensure the channel name is stored in lowercase
        self.name = self.name.lower()
        super(Channel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
