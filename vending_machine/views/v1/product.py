import logging

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from decorators import require_params
from vending_machine.models import User, Product
from vending_machine.serializer.product_serializer import ProductSerializer
from vending_machine.views.exceptions import RequestBodyNotAcceptable, TriggerInternalServerError


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@require_params(["product_name", "cost", "amount_available"])
def create_product(request):
    payload = request.data

    if request.user.role == 'seller':
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
    else:
        raise RequestBodyNotAcceptable('User is not seller')



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
@permission_classes([IsAuthenticated])
def delete_product(request, id):
    if request.user.role == 'seller':
        product = get_object_or_404(Product, pk=id)
        product.delete()
        return Response(
            status=status.HTTP_200_OK,
        )
    else:
        raise RequestBodyNotAcceptable('User is not seller of given product so he can not delete')


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_product(request, id):
    payload = request.data
    product = get_object_or_404(Product, pk=id)
    if request.user.role == 'seller':
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
    else:
        raise RequestBodyNotAcceptable('User is not seller of given product so he can not delete')


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@require_params(["product_id", "amount"])
def buy_product(request):


    payload = request.data

    if request.user.role != 'buyer':
        raise RequestBodyNotAcceptable('Only Buyer is allowed to buy the product')

    product_id = payload.get("product_id")
    amount = payload.get('amount')

    product = get_object_or_404(Product, pk=product_id)

    if amount > product.amount_available:
        raise RequestBodyNotAcceptable(f'max available product amount: {product.amount_available}')

    total_amount = product.cost * amount

    user_deposited = request.user.deposit

    if total_amount > user_deposited:
        raise RequestBodyNotAcceptable('Total amount is more than you have deposited. please deposit more coins')

    request.user.deposit -= total_amount
    request.user.save()

    op_change = []
    allowed_change = [100, 50, 20, 10, 5]

    change = 0
    if user_deposited > total_amount:
        change = user_deposited - total_amount

    for ac in allowed_change:
        op = change // ac
        if op > 0:
            op_change.append(ac)
            change -= op * ac

    product.amount_available -= amount
    product.save()
    response = {
        "change": op_change,
        "total_spent": total_amount,
        "product": ProductSerializer(product).data
    }

    return Response(
        data=response,
        status=status.HTTP_200_OK,
    )


