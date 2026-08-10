from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models
from . import serializers

def index(request):
  return render(request, 'main/index.html')

@api_view(['GET'])
def get_queryset(request):
  furniture = models.Furniture.objects.all()

  category = request.query_params.get('category')

  if category:
    furniture = furniture.filter(category=category)

  serializer = serializers.FurnitureSerializer(furniture, many=True)

  return Response(serializer.data)