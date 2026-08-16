from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework import status
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

@api_view(['GET', 'POST'])
def orders(request):
  if request.method == 'GET':
    email = request.query_params.get('email')

    if not email:
      return Response({"detail": 'Ошибка. Для полчения заказов нужно передать email клиента. Например: /?email=client@gmail.com'}, status=status.HTTP_400_BAD_REQUEST)

    orders = models.Order.objects.filter(email=email)

    serializer = serializers.OrderSerializer(orders, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

  if request.method == 'POST':
    email = request.data['email']
    goods_ids = request.data['goods']

    furniture = list(models.Furniture.objects.filter(id__in=goods_ids))

    if len(furniture) != len(goods_ids):
      return Response({'detail': 'Один или несколько товаров не существует'}, status=status.HTTP_400_BAD_REQUEST)

    total = 0

    for furniture_item in furniture:
      total += furniture_item.price

    order = models.Order.objects.create(email=email, amount=total)

    order.goods_list.set(furniture)

    serializer = serializers.OrderSerializer(order)

    return Response(serializer.data, status=status.HTTP_201_CREATED)

    