from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from django.contrib.auth.models import Group, Permission
from rest_framework import status
from users.permissions import IsStaff
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
try:
    from globalapp.ed import encode_jwt
except:
    pass
from globalapp.views import BaseViews
from users.models import Roles, Users
from users.serializers import AllUserSerializer, CustomTokenObtainPairSerializer, GropuSerializer, PermissionSerializer, RolesSerializer, UserSerializer
# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class =CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token=response.data['access']
        payload = AccessToken(token).payload
        user_id = payload.get('user_id')
        user = Users.objects.filter(id=user_id)
        serializer = AllUserSerializer(user, many=True)
        for user_data in serializer.data:
            if 'roles' in user_data:
                for role in user_data['roles']['menu']:
                    if 'permissions' in role:
                        for permission in role['permissions']:
                            permission['submenu'] = permission['codename'].split('_')[1]
                            permission['access'] = permission['codename'].split('_')[0]
        
        serializer.instance = user
        try:
            response.data["user"] = encode_jwt({"data": serializer.data})

        except:
            response.data["user"] = {"data": serializer.data}
        return response

class RoleViewSet(BaseViews):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated,IsStaff]
    model_name = Roles
    methods=["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer

class GroupViewSet(BaseViews):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated,IsStaff]
    model_name = Group
    
    methods=["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]
    serializer_class = GropuSerializer

class PermissionViewSet(BaseViews):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated,IsStaff]
    model_name = Permission
    
    methods=["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]
    serializer_class = PermissionSerializer
    def list(self, request, *args, **kwargs):
        if "list" in self.methods:
            try:
                limit = request.GET.get('limit')
            except:
                limit = None
            if limit is None:
                # No limit parameter provided, return all data
                
                queryset = self.filter_queryset(self.get_queryset())
                # print(self.get_queryset())
                serializer = self.get_serializer(queryset, many=True)
                for data in serializer.data:
                    data['access'] = data['codename'].split('_')[0]
                    # print(data)

                token = encode_jwt({"data": serializer.data})  # Encode serialized data into JWT token
                return self.generate_response(True, status.HTTP_200_OK, "list_success", data={"token": token})
            else:
                # Pagination requested, apply pagination
                queryset = self.filter_queryset(self.get_queryset())
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    for data in serializer.data:
                        data['access'] = data['codename'].split('_')[0]
                    # print(data)
                    token = encode_jwt({"data": serializer.data})  # Encode serialized data into JWT token
                    return self.get_paginated_response({"token": token})
        else:
            return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "list_not_allowed")
        
class UserViewSet(BaseViews):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated,IsStaff]
    model_name = Users
    methods=["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['roles__name']  # Enable filtering by role name
    def get_permissions(self):
        # Allow list and create actions without authentication
        if self.action in ['list', 'create']:
            return [permissions.AllowAny()]
        if self.action in ['update_profile', 'get_own_data']:
            return [permissions.IsAuthenticated()]
        # For other actions, staff permission is required
        return super().get_permissions()
        
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def update_profile(self, request, pk=None):
        # If user is a staff member, they can update anyone's profile
        if request.user.is_staff:
            user = Users.objects.get(pk=pk)
        else:
            # Non-staff users can only update their own profile
            user = request.user
        print(request.data)
        serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
        
        
        if serializer.is_valid():
            serializer.save()
            
            token = encode_jwt({"data": serializer.data})
            return self.generate_response(True, status.HTTP_201_CREATED, "create_success", data={"token": token})
        else:
            print(f"Validation failed for phone number: {request.data.get('phone_number')}")
            print(serializer.errors)  # Log detailed errors
        return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "list_not_allowed")
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def get_own_data(self, request):
        user = request.user
        serializer = UserSerializer(user, partial=True, context={'request': request})
        token = encode_jwt({"data": serializer.data})
        return self.generate_response(
            True,
            status.HTTP_200_OK,
            "user_data_retrieved",
            data={"token": token}
        )
    
