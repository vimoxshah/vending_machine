import logging

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from decorators import require_params, is_valid_role
from vending_machine.models import User, Product
from vending_machine.serializer.product_serializer import ProductSerializer
from vending_machine.views.exceptions import RequestBodyNotAcceptable, TriggerInternalServerError


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@is_valid_role('seller')
@require_params(["product_name", "cost", "amount_available"])
def create_product(request):
    payload = request.data
    product = Product.objects.create(product_name=payload['product_name'],
                                     cost = payload['cost'],
                                     amount_available=payload['amount_available'],
                                     seller_id=request.user.id)
    product = get_object_or_404(Product, pk=product.id)
    product = ProductSerializer(product)
    return Response(
        data=product.data,
        status=status.HTTP_201_CREATED,
    )



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_product(request, id):
    try:
        product = get_object_or_404(Product, pk=id)
        product = ProductSerializer(product)
        return Response(
            data=product.data,
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        logging.error(e, exc_info=True)
        raise TriggerInternalServerError(str(e))


@api_view(["DELETE"])
@is_valid_role('seller')
@permission_classes([IsAuthenticated])
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return Response(
        status=status.HTTP_200_OK,
    )


@api_view(["PUT"])
@is_valid_role('seller')
@permission_classes([IsAuthenticated])
def update_product(request, id):
    payload = request.data
    product = get_object_or_404(Product, pk=id)
    if "product_name" in payload:
        product.product_name = payload['product_name']
    if "cost" in payload:
        product.cost = payload['cost']
    if "amount_available" in payload:
        product.amount_available = payload['amount_available']
    product.save(update_fields=['product_name', 'cost', 'amount_available'])
    return Response(
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@is_valid_role('buyer')
@require_params(["product_id", "amount"])
def buy_product(request):
    payload = request.data
    product_id = payload.get("product_id")
    amount = payload.get('amount')

    product = get_object_or_404(Product, pk=product_id)

    if amount > product.amount_available:
        raise RequestBodyNotAcceptable(f'max available product amount: {product.amount_available}')

    total_amount = product.cost * amount

    user_deposited = request.user.deposit

    if total_amount > user_deposited:
        raise RequestBodyNotAcceptable('Total amount is more than you have deposited. please deposit more coins')

    request.user.deposit_amount(total_amount)
    change = product.give_change(user_deposited, total_amount, amount)

    response = {
        "change": change,
        "total_spent": total_amount,
        "product": ProductSerializer(product).data
    }

    return Response(
        data=response,
        status=status.HTTP_200_OK,
    )


