from rest_framework import serializers
from todo.models import Todo


"""
 Here we import the serializer module from the 
 Django Rest Framework, as well as our Todo model
"""

class TodoSerializer(serializers.ModelSerializer):
    """
        Todo Serializer.

        User to serialize the Todo model to JSON.
        The fields to be serialized are:
        -   id
        -   title
        -   description
        -   status
        -   updated

        With the META CLASS:
        we will tell the Django Rest Framework what model
        we want to serialize, as well as the fields that
        we want to be serialized
    """
    class Meta:
        model = Todo
        fields = ('id','title','description','status','updated')
