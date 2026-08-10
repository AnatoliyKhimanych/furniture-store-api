from django.shortcuts import render, get_object_or_404
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

@api_view(['GET'])
def get_furniture_detail(request, pk):
  furniture = get_object_or_404(models.Furniture, pk=pk)

  serializer = serializers.FurnitureSerializer(furniture)

  return Response(serializer.data)