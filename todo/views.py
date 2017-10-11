# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from todo.serializers import TodoSerializer     # from serializers.py
from todo.models import Todo
from django.contrib.auth.models import User


"""
    THIS VIEW WILL INHERIT FROM APIView
    IT EXPOSES AN API ENDPOINT
    Utilising a CBV - Class Based View
    which allows us to inherit functionality
    It will return a serialized response
"""
class TodoView(APIView):
    """
    TodoView used to handle the incoming requests relating
    to 'todo' items
    """

    permission_classes = (IsAuthenticated,) # add IsAuthenticated to tupple to restrict access

    #   A GET request to the server will auto invoke
    #   the "get" method
    def get(self,request, pk=None):
        """
        Handle the GET request for the `/todo/` endpoint.

        Gets `username` from the `query_params` in order to retrieve the
        `todo` items belonging to that user,

        IF primary key has been provided by the URL:
            Return the relevant object
        ELSE
            Retrieve a complete list of 'todo' items from
            the Todo model,

        Returns: the serialized 'todo' object(s)
        """
        if "username" in request.query_params:
            if pk is None:
                # Get the 'user' based on the username provided by the
                # 'query_params'
                user = User.objects.get(username=request.query_params['username'])
                # Filter the 'to-do' items based on this 'user'
                todo_items = Todo.objects.filter(user=user)
                # todo_items = Todo.objects.all()
                # Serialize the data retrieved from the DB and
                # serialize them using the 'TodoSerializer'
                # many=True informs the serializer that there's
                # multiple records to be serialized
                serializer = TodoSerializer(todo_items, many= True)
                # the serialized data 'serialized_data' is
                # stored in the .data property of the serializer
                # object
                serialized_data = serializer.data
                # return an instance of Django REST Response obj
                # containing the serialized data
                return Response(serialized_data)
            else:
                # Get the object containing the pk provided by the URL
                todo = Todo.objects.get(id=pk)
                # Serialize the 'to-do' item
                serializer = TodoSerializer(todo)
                # Store it in the serialized_data variable and return it
                serialized_data = serializer.data
                return Response(serialized_data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def post(self,request):
        """
        Handle the POST request for the '/todo/' endpoint

        This view will take the 'data' property from the 'request'
        object, deserializer it into a 'Todo' object and store it
        it in the DB.

        Returns a 201 (successfully created) if the item is successfully
        created, otherwise returns a 400 (bad request)
        """
        # Instantiate a new TodoSerializer with the data
        # contained in the request object
        # This deserializes the request data
        serializer = TodoSerializer(data=request.data)

        # Check to see if data in the 'request' is valid.
        # If (the data cannot be deserialized into a To-do object)
        #   then a bad request response will be returned containing
        #   the error.
        # Else,
        #   save the data and return the data and a successfully
        #   created status
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Get the 'user' based on the request data(not in the serializer)
            user = User.objects.get(username = request.data['username'])

            # Get the to-do item data from the serializer
            data = serializer.data

            # Create the new to-do item
            Todo.objects.create(user=user,
                                title=data["title"],
                                description=data["description"],
                                status=data["status"])

            # save data to the DB
            #serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)


    def put(self, request, pk):
        """
        Handle PUT request for the '/todo/' endpoint
        Retrieves a 'todo' instance based on the primary key contained
        in the URL.
        Then takes the 'data' property from the 'request' object to update the relevant 'todo' instance
        :return: The Updated object if the update was successful, otherwise 400 (bad request) is returned
        """

        todo = Todo.objects.get(id=pk)
        # Tell the serializer which To-do item to update and pass in the data
        serializer = TodoSerializer(todo,data=request.data)

        # Check to see if the data in the 'request' is valid.
        # If the data cannot be deserialized into a To-do object then
        # a bad request response will be returned containing the error.
        # Else, save and return the data
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            return Response(serializer.data)


    def delete(selfself,request,pk):
        """
        Handle DELETE request for the '/todo/' endpoint

        Retrieves a 'todo' instance based on the primary key
        contained in the URL and then deletes the relevant instance

        Returns a 204 (no content) status to indicate that the item
        was deleted
        """
        todo = Todo.objects.get(id=pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)