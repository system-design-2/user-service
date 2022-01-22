from drf_yasg import openapi

jwt_header = openapi.Parameter('Authorization', openapi.IN_HEADER, description="jwt access token for authentication",
                               format="Bearer <token>", type=openapi.TYPE_STRING, required=True)