# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from accounts.serializers import UserSerializer


class UserView(APIView):
    """
    UserView handles the requests made to '/accounts/'
    """

    permission_classes = () # empty tupple means you don't need to be authenticated to access this view

    def post(self,request):
        """
        Handles the POST request made to the '/accounts/' URL.

        This view will take the 'data' property from the 'request'
        object, deserialize it into a 'User' object and store
        in the DB.
        IT WILL CREATE NEW USERS and return 201 (successfully created)
        if the user is successfully created, otherwise returns a
        400(bad request)
        """
        serializer = UserSerializer(data=request.data)

        # Check to see if the data in the `request` is valid.
        # If the cannot be deserialized into a User object then
        # a bad request response will be returned.
        # Else, save the data and return the data and a successfully
        # created status
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = serializer.data
            # Create a new user using the 'username' contained in
            # the data 'dict'
            user = User.objects.create(username=data["username"])
            # Use the 'set_password' method to create a HASHED password
            # using the password provided in the 'data' dict
            user.set_password(data["password"])
            user.save()
            return Response(data, status=status.HTTP_201_CREATED)
