# dj_react_chat\server\views.py

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.db.models import Count
from .models import Server
from .schema import server_list_docs
from .serializer import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):
    """
    **ServerListViewSet**

    A Django REST Framework ViewSet for retrieving and filtering servers based on multiple criteria.

    ### Attributes:
    - **queryset (QuerySet)**: The default queryset used to retrieve all servers from the database.

    ### Methods:
    - `list(request)`: Retrieves and filters a list of servers based on the provided query parameters.
    """

    # This is the queryset that will be used to retrieve the servers.
    # It is a queryset of all servers in the database.
    queryset = Server.objects.all()

    @server_list_docs
    def get_queryset(self, request):
        """
        **Lists and filters servers based on query parameters.**

        This method applies optional filters to the server list, based on parameters
        like category, user membership, specific server ID, and whether to include
        the number of members for each server.

        ### Args:
        - **request (Request)**: The HTTP request object containing query parameters.

        ### Query Parameters:
        - `category` **(str, optional)**: Filter servers by the specified category name.
        - `qty` **(str, optional)**: Limit the number of servers returned to this quantity.
        - `by_user` **(str, optional)**: If set to `"true"`, filters servers where the current user is a member.
        - `by_server_id` **(str, optional)**: Retrieve a specific server by its ID.
        - `with_num_members` **(str, optional)**: If set to `"true"`, includes the number of members in each server.

        ### Raises:
        - **AuthenticationFailed**: Raised if the user is not authenticated when using `by_user` or `by_server_id`.
        - **ValidationError**: Raised for invalid `by_server_id` values or if no server is found for the provided ID.

        ### Returns:
        - **Response**: A `Response` object containing the serialized data of the filtered server list.

        ### Example Usage:
        ```python
        GET /servers/?category=gaming&qty=10
        Returns the first 10 servers in the "gaming" category

        GET /servers/?by_user=true
        Returns servers where the current user is a member

        GET /servers/?by_server_id=123
        Returns the server with the ID 123
        ```
        """
        ################################
        # Get the query parameters
        ################################
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = (
            request.query_params.get("by_user") == "true"
        )  # Convert the "by_user" query parameter to a boolean; comparison with "true" checks if the parameter is explicitly set to "true"
        by_server_id = request.query_params.get("by_server_id")
        with_num_members = request.query_params.get("with_num_members") == "true"

        # Filter the queryset to only include servers in the specified category.
        # __name means that we are filtering by the name of the category table as we have relation with category and server table.
        if category:
            self.queryset = self.queryset.filter(category__name=category)

        # Filter the queryset to only include servers by the current user if the 'by_user' query parameter is set to 'true'.
        if by_user:
            if not request.user.is_authenticated:
                raise AuthenticationFailed()
            user_id = request.user.id
            self.queryset = self.queryset.filter(
                members=user_id
            )  # only query servers what have the current user as a member

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("members"))

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
            if not request.user.is_authenticated:
                raise AuthenticationFailed()

            try:
                self.queryset = self.queryset.filter(id=by_server_id)
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"Server with id {by_server_id} not found"
                    )
            except ValueError:
                raise ValidationError("Server value error")

        # Serialize the queryset into a JSON response.
        serializer = ServerSerializer(
            self.queryset, many=True, context={"num_members": with_num_members}
        )

        # Return the serialized queryset as the response.
        return Response(serializer.data)
