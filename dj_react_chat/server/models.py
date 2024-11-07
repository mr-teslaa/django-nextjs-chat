# dj_react_chat\server\models.py

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from .validators import validate_icon_image_size, validate_image_file_extension


def category_icon_path(instance, filename):
    return f"category/{instance.name}/category_icon/{filename}"


def server_icon_path(instance, filename):
    return f"server/{instance.name}/server_icon/{filename}"


def server_banner_path(instance, filename):
    return f"server/{instance.name}/server_banner/{filename}"


class Category(models.Model):
    """
    Represents a category that servers can belong to.

    Attributes:
        name (str): The name of the category.
        icon (str): The path to the icon for this category.
        description (str): An optional description of the category.
    """

    name = models.CharField(max_length=100)
    icon = models.FileField(upload_to=category_icon_path, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    ###########################
    # Category image changes
    ###########################
    def save(self, *args, **kwargs):
        if self.id:
            # query the Category instance from the database
            existing = get_object_or_404(Category, id=self.id)

            # if the icon has changed
            if existing.icon != self.icon:
                # delete the old icon file, save=False because to avoid conflict
                existing.icon.delete(save=False)

        # finally saving the changes
        super().save(*args, **kwargs)

    ###########################
    # Category detetion
    ###########################
    # django singals to call when a Category is deleted
    @receiver(models.signals.pre_delete, sender="server.Category")
    def category_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            # Get the icon and delete it
            if field.name == "icon":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)

    # Category initialization
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
    banner = models.ImageField(
        upload_to=server_banner_path,
        blank=True,
        null=True,
        validators=[validate_image_file_extension],
    )
    icon = models.ImageField(
        upload_to=server_icon_path,
        blank=True,
        null=True,
        validators=[validate_icon_image_size, validate_image_file_extension],
    )

    ###########################
    # Category image changes
    ###########################
    def save(self, *args, **kwargs):
        # self.name = self.name.lower()
        # super(Channel, self).save(*args, **kwargs)

        if self.id:
            # query the Category instance from the database
            existing = get_object_or_404(Category, id=self.id)

            # if the icon has changed
            if existing.icon != self.icon:
                # delete the old icon file, save=False because to avoid conflict
                existing.icon.delete(save=False)

            # if the banner has changed
            if existing.banner != self.banner:
                # delete the old banner file, save=False because to avoid conflict
                existing.banner.delete(save=False)

        # finally saving the changes
        super().save(*args, **kwargs)

    ###########################
    # Category detetion
    ###########################
    # django singals to call when a Category is deleted
    @receiver(models.signals.pre_delete, sender="server.Server")
    def category_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            # Get the icon and delete it
            if field.name == "icon" or field.name == "banner":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)

    # def save(self, *args, **kwargs):
    #     # Ensure the channel name is stored in lowercase
    #     self.name = self.name.lower()
    #     super(Channel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
