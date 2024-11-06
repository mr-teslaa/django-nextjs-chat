# dj_react_chat\server\views.py

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from .models import Server
from .serializer import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):
    """
    ViewSet for listing all servers.

    This ViewSet will be used to list all servers in the database.
    You can filter the servers by category by passing the category name as a query parameter.
    """

    # This is the queryset that will be used to retrieve the servers.
    # It is a queryset of all servers in the database.
    queryset = Server.objects.all()

    def list(self, request):
        """
        List all servers.

        This function will be called when the user makes a GET request to the view.
        It will return a list of all servers in the database, filtered by category if the user provided a category name as a query parameter.
        """

        # Get the category name and quantity from the query parameters.
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = (
            request.query_params.get("by_user") == "true"
        )  # Convert the "by_user" query parameter to a boolean; comparison with "true" checks if the parameter is explicitly set to "true"
        by_server_id = request.query_params.get("by_server_id")

        # check if user is authenticated
        if by_user or by_server_id and not request.user.is_authenticated:
            raise AuthenticationFailed()

        # If the user provided a category name, filter the queryset to only include servers in that category.

        # Filter the queryset to only include servers in the specified category.
        # __name means that we are filtering by the name of the category table as we have relation with category and server table.
        if category:
            self.queryset = self.queryset.filter(category__name=category)

        # Filter the queryset to only include servers by the current user if the 'by_user' query parameter is set to 'true'.
        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(
                members=user_id
            )  # only query servers what have the current user as a member

        # The user provided a quantity, so we need to limit the queryset to the specified number of items.
        # We use list slicing to achieve this.
        # The syntax is: queryset[start:stop]
        # Where start is the index of the first item we want to include, and stop is the index of the last item we want to include + 1.
        # Since we want to include the first 'qty' items, we start at index 0, and stop at index 'qty'.
        # We use int(qty) to convert the string 'qty' to an integer, because list slicing requires integer indices.
        # The queryset will now only contain the first 'qty' items of the original queryset.
        if qty:
            self.queryset = self.queryset[: int(qty)]

        if by_server_id:
            try:
                self.queryset = self.queryset.filter(id=by_server_id)
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"Server with id {by_server_id} not found"
                    )
            except ValueError:
                raise ValidationError("Server value error")

        # Serialize the queryset into a JSON response.
        serializer = ServerSerializer(self.queryset, many=True)

        # Return the serialized queryset as the response.
        return Response(serializer.data)
