from django.utils import timezone
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, \
    get_object_or_404
from core.models import Product, Order, OrderProduct, Category, SubCategory, DeliveryMan, Payment, Refund, Client, \
    AdditionalItem, ShippingAddress
from .serializers import ProductSerializer, OrderProductSerializer, OrderSerializer, SubCategorySerializer, \
    CategorySerializer, RefundSerializer, AdditionalItemSerializer, ClientSerializer, UserSerializer
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from django.shortcuts import redirect
import random
import string
from django.utils import timezone
import datetime
from datetime import timedelta
from django.contrib.auth.models import User
import json
from rest_framework.authtoken.models import Token


class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product instances.
    """
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class OrderProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing OrderProduct instances.
    """
    serializer_class = OrderProductSerializer
    queryset = OrderProduct.objects.all()


class OrderViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing  Order instances.
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class SubCategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing SubCategory instances.
    """
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Category instances.
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class RefundViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Refund instances.
    """
    serializer_class = RefundSerializer
    queryset = Refund.objects.all()


class AdditionalItemViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing AdditionalItem instances.
    """
    serializer_class = AdditionalItemSerializer
    queryset = AdditionalItem.objects.all()


class ClientViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Client instances.
    """
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

#
# @api_view()
# @login_required
# def add_to_cart(request, pk):
#     # find the product
#     product = get_object_or_404(Product, pk=pk)
#     order_product, created = OrderProduct.objects.get_or_create(
#         product=product, user=request.user, ordered=False)
#     # find the orders of current user that has not benn ordered (payed)
#     orders = Order.objects.filter(user=request.user, ordered=False)
#
#     if orders.exists():
#         order = orders[0]
#         # check product already exist in order product increase quantity
#         if order.products.filter(product__slug=product.slug).exists():
#             order_product.quantity += 1
#             order_product.save()
#         else:
#             order.products.add(order_product)
#     else:
#         order = Order.objects.create(user=request.user)
#         order.products.add(order_product)
#     return Response(
#         {'message': 'product ' + product.title + ' has been added to ' + request.user.username + ' cart successfully'})


class AddToCart(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        pk = int(request.data.get('pk', None))
        add_item = request.data.get('add_item', None)
        user = User.objects.get(pk=int(request.data.get('user', None)))

        # find the product
        product = get_object_or_404(Product, pk=pk)

        # Check if add_item is valid
        if not product.additional_items.filter(pk=add_item).exists():
            add_item = None
        add_item_obj = AdditionalItem.objects.filter(pk=add_item)
        order_product = OrderProduct.objects.filter(product=product, user=user, ordered=False,
                                                    additional_items=add_item)
        # get
        if order_product.exists():
            order_product = order_product[0]

        # Create
        else:
            order_product = OrderProduct.objects.create(
                product=product, user=user, ordered=False)
            if add_item_obj.exists():
                add_item_obj = AdditionalItem.objects.get(pk=add_item)
                order_product.additional_items.add(add_item_obj)

        # find the orders of current user that has not benn ordered (payed)
        orders = Order.objects.filter(user=user, ordered=False)

        if orders.exists():
            order = orders[0]

            # check product already exist in order product increase quantity
            if order.products.filter(product__slug=product.slug, additional_items=add_item).exists():
                order_product.quantity += 1
                order_product.save()
            else:
                order.products.add(order_product)
        else:
            order = Order.objects.create(user=user)
            order.products.add(order_product)
        return Response(
            {'message': 'Le produit ' + product.title + ' a été ajouter au panier du' + user.username + ' avec succès'})


# @api_view()
# @login_required
# def remove_from_cart(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     order_qs = Order.objects.filter(
#         user=request.user,
#         ordered=False
#     )
#     if order_qs.exists():
#         order = order_qs[0]
#         # check if the order item is in the order
#         if order.user == request.user:
#             if order.products.filter(product__slug=product.slug).exists():
#                 order_product = OrderProduct.objects.filter(
#                     product=product,
#                     user=request.user,
#                     ordered=False
#                 )[0]
#                 order.products.remove(order_product)
#                 order_product.delete()
#                 return Response({'message': 'This item was removed from your cart.'})
#             else:
#                 return Response({'message': 'This item was not in your cart'})
#         else:
#             return Response({'message': "you don't own this order"})
#     else:
#         return Response({'message': 'You do not have an active order'})


class RemoveFromCart(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        pk = int(request.data.get('pk', None))
        user = User.objects.get(pk=int(request.data.get('user', None)))
        product = get_object_or_404(Product, pk=pk)
        order_qs = Order.objects.filter(
            user=user,
            ordered=False
        )
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.user == user:
                if order.products.filter(product__slug=product.slug).exists():
                    order_product = OrderProduct.objects.filter(
                        product=product,
                        user=user,
                        ordered=False
                    )[0]
                    order.products.remove(order_product)
                    order_product.delete()
                    return Response({'message': 'Cet article a été supprimé de votre panier'})
                else:
                    return Response({'message': "ce produit n'existe pas dans le panier"})
            else:
                return Response({'message': "vous ne possédez pas cette commande"})
        else:
            return Response({'message': "vous n'avez pas de commande active"})


# @api_view()
# @login_required
# def remove_single_product_from_cart(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     order_qs = Order.objects.filter(
#         user=request.user,
#         ordered=False
#     )
#     if order_qs.exists():
#         order = order_qs[0]
#         # check if the order item is in the order
#         if order.products.filter(product__slug=product.slug).exists():
#             order_product = OrderProduct.objects.filter(
#                 product=product,
#                 user=request.user,
#                 ordered=False
#             )[0]
#             if order_product.quantity == 1:
#                 return redirect("core:api:remove_from_cart", pk=pk)
#             else:
#                 order_product.quantity -= 1
#             order_product.save()
#             return Response({'message': 'This item was removed from your cart.'})
#         else:
#             return Response({'message': 'This item was not in your cart'})
#     else:
#         return Response({'message': 'You do not have an active order'})


class RemoveSingleProductFromCart(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        pk = int(request.data.get('pk', None))
        user = User.objects.get(pk=int(request.data.get('user', None)))
        product = get_object_or_404(Product, pk=pk)
        order_qs = Order.objects.filter(
            user=user,
            ordered=False
        )
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.products.filter(product__slug=product.slug).exists():
                order_product = OrderProduct.objects.filter(
                    product=product,
                    user=user,
                    ordered=False
                )[0]
                if order_product.quantity == 1:
                    order.products.remove(order_product)
                    order_product.delete()
                    if order.products.count() == 0:
                        order.delete()
                    return Response({'message': 'Cet article a été complètement supprimé de votre panier'})
                else:
                    order_product.quantity -= 1
                order_product.save()
                return Response({'message': 'Cet article a été supprimé de votre panier'})
            else:
                return Response({'message': "Cet article n'était pas dans votre panier"})
        else:
            return Response({'message': "Vous n'avez pas de commande active"})


@api_view()
def cart_item_count(request):
    user = User.objects.get(pk=int(request.data.get('user', None)))
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return Response({'message': qs[0].products.count()})
        else:
            return Response({'message': 'panier vide'})


def get_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


class PaymentHandler(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        pk = request.data.get('pk')
        user = request.data.get('user')
        order = Order.objects.get(pk=pk)
        user = User.objects.get(pk=user)
        if order.ordered:
            return Response({'message': "cette commande est déjà commandée"})
        else:
            # TODO :payment = Payment() , update to post class
            client = Client.objects.get(user=user)
            if client.amount >= order.total_price:
                client.amount -= order.total_price
                client.save()
                payment_obj = Payment.objects.create(user=user, payment_type='S', amount=order.total_price,
                                                     payment_date=timezone.now())
                order.ordered = True
                order.ordered_date = timezone.now()
                order.shipping_address = ShippingAddress.objects.get(user=client, default=True)
                order.payment = payment_obj
                order_products = Order.objects.filter(pk=pk)[0].products.all()
                for order_product in order_products:
                    order_product.ordered = True
                    order_product.save()
                order.ref_code = get_ref_code()
                order.save()
                mans = DeliveryMan.objects.order_by('orders_delivered')
                for man in mans:
                    if man.available:
                        man.orders.add(order)
                        man.orders_delivered += 1
                        man.save()
                        order.status = 'W'
                        order_products = Order.objects.filter(pk=pk)[0].products.all()
                        return Response({'message': 'la commande est payé'})
                if order.status != 'W':
                    order.status = 'Q'
                    order.save()
                    return Response({
                        'message': "la commande a été payée et mise dans la file d'attente en raison de l'indisponibilité du livreur"
                    })
            else:
                return Response({'message': "tu n'as pas assez d'argent"})


@api_view()
@login_required()
def total(request):
    # ToDo fix that count more than one item in orders
    order_products = OrderProduct.objects.filter(ordered=True)
    orders = [product.product.title for product in OrderProduct.objects.filter(ordered=True)]
    total_money = 0
    total_quantity: int = 0
    for order_product in order_products:
        total_money += order_product.quantity * order_product.product.price
        total_quantity += order_product.quantity
        # {'money': total_money, 'quantity': total_quantity}
    return Response({'argent': total_money, 'quantité': total_quantity, 'produit': orders})


class RefundHandler(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        option = request.data.get('option', None)
        pk = request.data.get('pk', None)
        if pk is not None:
            order_qs = Order.objects.filter(pk=pk)
            if order_qs.exists() and order_qs[0].ordered:
                order = order_qs[0]
                if option == "request":
                    print(0)
                    if not order.refund_requested:
                        reason = request.data.get('reason', None)
                        Refund.objects.create(reason=reason, accepted=False, in_queue=True, order=order)
                        order.refund_requested = True
                        order.save()
                        return Response({'message': 'refend a été demandé'})
                    else:
                        return Response({'error': 'le remboursement est déjà demandé'})
                if option == "grant":
                    if order.refund_requested and not order.refund_granted:
                        order.refund_granted = True
                        refund_qs = Refund.objects.filter(order=order)
                        refund = refund_qs[0]
                        refund.accepted = True
                        refund.in_queue = False
                        client = Client.objects.get(user=order.user)
                        client.amount += order.total_price
                        refund.save()
                        order.save()
                        client.save()
                        return Response({'message': 'remboursement accordé'})
                    else:
                        return Response({'error': 'le remboursement est déjà accordé ou non demandé sur cette commande'})
                if option == "deny":
                    if order.refund_requested and not order.refund_granted:
                        refund_qs = Refund.objects.filter(order=order)
                        if refund_qs.exists():
                            if not refund_qs[0].accepted and refund_qs[0].in_queue:
                                refund = refund_qs[0]
                                refund.accepted = False
                                refund.in_queue = False
                                refund.save()
                                return Response({'message': 'remboursement refusé'})
                            else:
                                return Response({'error': 'le remboursement est déjà refusé' + str(refund_qs[0].accepted) + str(
                                    refund_qs[0].in_queue)})
                        else:
                            return Response({'error': 'remboursement non trouvé'})

                    else:
                        return Response(
                            {'error': 'le remboursement est accordé et ne peut être ni refusé ni demandé sur cette commande'})
            else:
                return Response({'error': 'commande non trouvée ou non commandée'})
        else:
            return Response({'error': 'veuillez saisir un pk'})


class OrderByDate(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        start_date = request.data.get('star_date', None)
        end_date = request.data.get('end_date', None)
        ordered = request.data.get('ordered', None)
        if start_date is not None and end_date is not None and ordered is not None:
            order = Order.objects.filter(ordered_date__range=[start_date, end_date], ordered=ordered)
            serializer = OrderSerializer(order, many=True)
            return Response(serializer.data)
        else:
            if ordered is None and end_date:
                order = Order.objects.filter(ordered_date__range=[start_date, end_date])
                serializer = OrderSerializer(order, many=True)
                return Response(serializer.data)
            if end_date is None:
                order = Order.objects.filter(ordered_date__range=[start_date, timezone.now()])
                serializer = OrderSerializer(order, many=True)
                return Response(serializer.data)
            else:
                return Response({'error': 'argument manquant'})


class ProfitView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        star_date = request.data.get('star_date')
        end_date = request.data.get('end_date')
        orders = Order.objects.filter(ordered_date__range=[star_date, end_date], ordered=True)
        profit = 0
        for order in orders:
            profit += order.total_price

        return Response({"profit": profit})


# merged_dict = {key: value for (key, value) in (dictA.items() + dictB.items())}


class OrderGraph(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        time_range = int(request.data.get('range'))
        star_date = datetime.datetime.strptime(request.data.get('star_date'), '%Y-%m-%d')
        by = request.data.get('by')
        # counter = {i: i for (i,order) in (range(time_range)+)}
        counter = {}
        for i in range(time_range):
            # counter += [Order.objects.filter(ordered_date__range=[star_date, star_date + timedelta(minutes=1439,
            # seconds=59)]).count()]
            # counter.update({str(star_date.date()): Order.objects.filter(
            # ordered_date__range=[star_date, star_date + timedelta(minutes=1439, seconds=59)]).count()})
            if by == 'days':
                counter.update({str(star_date.date()): Order.objects.filter(
                    ordered_date__range=[star_date, star_date + timedelta(minutes=1439, seconds=59)]).count()})
                star_date += timedelta(days=1)
            if by == 'years':
                counter.update({str(star_date.date()): Order.objects.filter(
                    ordered_date__range=[star_date,
                                         star_date + timedelta(minutes=1439, seconds=59, days=365)]).count()})
                star_date += timedelta(days=365)
            if by == 'months':
                counter.update({str(star_date.date()): Order.objects.filter(
                    ordered_date__range=[star_date, star_date + timedelta(minutes=1439, seconds=59, days=30)]).count()})
                star_date += timedelta(days=30)
        # res = {i: val for (i, val) in (range(time_range), counter)}
        return Response(counter)


class OrderView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        orders = Order.objects.filter(ordered=True)
        products = Product.objects.all()
        ordered = request.data.get('ordered', "False")
        if request.data.get('pk') is not None:
            user = User.objects.get(pk=request.data.get('pk'))
            if ordered is not None and ordered == "True":
                ordered = True
            else:
                if ordered is not None and ordered == "False":
                    ordered = False
                else:
                    ordered = False

            refunded = request.data.get('refunded', None)
            if refunded is not None and refunded == "True":
                refunded = True
            else:
                if refunded is not None and refunded == "False":
                    refunded = False
                else:
                    refunded = None

            print(ordered, refunded)
            if refunded is not None:
                if refunded:
                    orders = Order.objects.filter(user=user, ordered=True, refund_granted=refunded)
                else:
                    orders = Order.objects.filter(user=user, ordered=True, refund_requested=True, refund_granted=refunded)
            else:
                orders = Order.objects.filter(user=user, ordered=ordered)
        data = [{'id': order.pk,
                 'ordered_date': order.ordered_date,
                 'ordered': order.ordered,
                 'ref_code': order.ref_code,
                 'received': order.received,
                 'refund_requested': order.refund_requested,
                 'refund_granted': order.refund_granted,
                 'price': order.total_price,
                 'refund': ([{'id': Refund.objects.get(order=order).id,
                              'reason': Refund.objects.get(order=order).reason,
                              'accepted': str(Refund.objects.get(order=order).accepted),
                              'in_queue': str(Refund.objects.get(order=order).in_queue),
                              }
                             if Refund.objects.filter(order=order).exists() else 'none']),
                 'user': order.user.id,
                 'user_name': str(User.objects.get(pk=order.user.id).username),
                 'product': ([{'id': Product.objects.get(pk=order.products.all()[i].product.id).id,
                               'title': Product.objects.get(pk=order.products.all()[i].product.id).title,
                               'price': Product.objects.get(pk=order.products.all()[i].product.id).price,
                               'discount_price':
                                   Product.objects.get(pk=order.products.all()[i].product.id).discount_price,
                               'slug': Product.objects.get(pk=order.products.all()[i].product.id).slug,
                               'photo': "http://127.0.0.1:8000/media/" + str(
                                   Product.objects.get(pk=order.products.all()[i].product.id).photo),
                               'description': Product.objects.get(pk=order.products.all()[i].product.id).description,
                               'category': Product.objects.get(pk=order.products.all()[i].product.id).category,
                               'subcategory': Product.objects.get(pk=order.products.all()[i].product.id).subcategory,
                               'quantity': order.products.all()[i].quantity,
                               'additional_items': ([{'id': order.products.all()[i].additional_items.all()[j].id,
                                                      'title': order.products.all()[i].additional_items.all()[j].title,
                                                      'price': order.products.all()[i].additional_items.all()[j].price
                                                      }
                                                     for j in
                                                     range(order.products.all()[i].additional_items.all().count())])
                               }
                              for i in range(order.products.count())])
                 }
                for order in orders]
        if request.data.get('pk') is not None and not ordered:
            return Response(data[0])
        return Response(data)


######################


class ProductView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        products = Product.objects.all()

        print(kwargs.get('pk'))
        if kwargs.get('pk') is not None:
            pk = kwargs.get('pk')
            product = Product.objects.get(pk=pk)
            data = {
                'id': product.id,
                'title': product.title,
                'price': product.price,
                'discount_price': product.discount_price,
                'slug': product.slug,
                'photo': "http://127.0.0.1:8000/media/" + str(product.photo),
                'description': product.description,
                'category': product.category,
                'subcategory': product.subcategory,
                'additional_items': ([{'id': product.additional_items.all()[j].id,
                                       'title': product.additional_items.all()[j].title,
                                       'price': product.additional_items.all()[j].price
                                       }
                                      for j in
                                      range(product.additional_items.all().count())])
            }
        else:
            data = [{
                'id': product.id,
                'title': product.title,
                'price': product.price,
                'discount_price': product.discount_price,
                'slug': product.slug,
                'photo': "http://127.0.0.1:8000/media/" + str(product.photo),
                'description': product.description,
                'category': product.category,
                'subcategory': product.subcategory,
                'additional_items': ([{'id': product.additional_items.all()[j].id,
                                       'title': product.additional_items.all()[j].title,
                                       'price': product.additional_items.all()[j].price
                                       }
                                      for j in
                                      range(product.additional_items.all().count())])
            }
                for product in products]
        return Response(data)


class ClientView(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        clients = Client.objects.all()
        data = [{
            "id": client.id,
            "address": client.address,
            "tel": client.tel,
            "city": client.city,
            "postal_code": client.postal_code,
            "amount": client.amount,
            "user": client.user_id,
            'user_name': str(User.objects.get(pk=client.user_id).username),
        }
            for client in clients]
        return Response(data)


class CreateAuth(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        serialized = UserSerializer(data=request.data)
        address = request.data.get('address', None)
        tel = request.data.get('tel', None)
        city = request.data.get('city', None)
        postal_code = request.data.get('postal_code', None)
        if serialized.is_valid():
            if tel is not None and city is not None and postal_code is not None and address is not None:
                user = User.objects.create_user(
                    request.data.get('username'),
                    request.data.get('email'),
                    request.data.get('password'),
                )
                client = Client.objects.create(amount=0, address=request.data.get('address'),
                                               tel=tel,
                                               city=city,
                                               postal_code=postal_code, user=user)
                token = Token.objects.create(user=user)
                ShippingAddress.objects.create(user=client, address=address, postal_code=postal_code, default=True)
                return Response({"key": token.key}, status=status.HTTP_201_CREATED)
            else:
                return Response({"errrr": "missing arg"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        token = request.data.get('token')
        f_token = Token.objects.get(key=token)
        user = User.objects.get(pk=f_token.user_id)
        client_qs = Client.objects.filter(user=user)
        if client_qs.exists():
            client = client_qs[0]
            data = {
                "id": client.id,
                "address": client.address,
                "tel": client.tel,
                "city": client.city,
                "postal_code": client.postal_code,
                "amount": client.amount,
                "photo": "http://127.0.0.1:8000/media/" + str(client.photo),
                "user": client.user_id,
                'user_name': str(User.objects.get(pk=client.user_id).username),
                'is_admin': user.is_superuser
            }
        else:
            data = {
                "id": user.id,
                "address": None,
                "tel": None,
                "city": None,
                "postal_code": None,
                "amount": None,
                'user_name': str(user.username),
                'is_admin': user.is_superuser
            }
        return Response(data)

