from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.core.mail import send_mail
from furnitureStore import settings

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models
from . import serializers


def index(request):
    return render(request, "main/index.html")


@api_view(["GET"])
def get_queryset(request):
    furniture = models.Furniture.objects.all()

    category = request.query_params.get("category")

    if category:
        furniture = furniture.filter(category=category)

    serializer = serializers.FurnitureSerializer(furniture, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_furniture_detail(request, pk):
    furniture = get_object_or_404(models.Furniture, pk=pk)

    serializer = serializers.FurnitureSerializer(furniture)

    return Response(serializer.data)


@api_view(["GET", "POST"])
def orders(request):
    if request.method == "GET":
        email = request.query_params.get("email")

        if not email:
            return Response(
                {
                    "detail": "Ошибка. Для полчения заказов нужно передать email клиента. Например: /?email=client@gmail.com"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        orders = models.Order.objects.filter(email=email).prefetch_related("goods_list")

        serializer = serializers.OrderSerializer(orders, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "POST":

        email = request.data.get("email")
        goods_ids = request.data.get("goods")

        err = validate_order_data(email, goods_ids)
        if err:
            return Response({"detail": f"{err}"}, status=status.HTTP_400_BAD_REQUEST)

        furniture = list(models.Furniture.objects.filter(id__in=goods_ids))

        found_ids = {item.id for item in furniture}

        missing_ids = set(goods_ids) - found_ids

        if missing_ids:
            return Response(
                {"detail": f"ID товаров {missing_ids} не существуют"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        total = 0

        for furniture_item in furniture:
            total += furniture_item.price

        order = models.Order.objects.create(email=email, amount=total)

        order.goods_list.set(furniture)

        send_email(order)

        serializer = serializers.OrderSerializer(order)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


def validate_order_data(email, goods_ids):
    validator = EmailValidator()

    if email is None:
        return "Поле email обязательно"

    if goods_ids is None:
        return "Поле goods обязательно"

    try:
        validator(email)

    except ValidationError:
        return "Введите правильный адрес электронной почты."

    if not isinstance(goods_ids, list):
        return "goods должен быть списком"

    if len(goods_ids) == 0:
        return "Список товаров не должен быть пустым"

    if not all(type(goods_ids) is int and goods_ids > 0 for goods_ids in goods_ids):
        return "Все ID товаров в goods должны быть положительными числами"

    if len(goods_ids) != len(set(goods_ids)):
        return "ID не должны повторяться"


def send_email(order):
    items = order.goods_list.all()

    item_names = "\n".join([f"• {item.name} - ${item.price}" for item in items])

    subject = "Ваш заказ успешно создан"
    message = (
        f"Ваш заказ с email: {order.email} успешно создан!\n"
        f"Товары в заказе:\n{item_names}\n"
        f"Общая сумма: {order.amount}"
    )
    from_email = settings.EMAIL_HOST_USER
    to_email = settings.EMAIL_HOST_USER

    send_mail(
        subject,
        message,
        from_email,
        [to_email],
        fail_silently=False,
    )
