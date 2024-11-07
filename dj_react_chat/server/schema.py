from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .serializer import ServerSerializer, ChannelSerializer

server_list_docs = extend_schema(
    responses=ServerSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name="category",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Filter servers by the specified category name",
        ),
        OpenApiParameter(
            name="qty",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Limit the number of servers returned to this quantity",
        ),
        OpenApiParameter(
            name="by_user",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="If set to 'true', filters servers where the current user is a member",
        ),
        OpenApiParameter(
            name="by_server_id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Retrieve a specific server by its ID",
        ),
        OpenApiParameter(
            name="with_num_members",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="If set to 'true', includes the number of members in each server",
        ),
    ],
)
