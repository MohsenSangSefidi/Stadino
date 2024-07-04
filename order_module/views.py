import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string

# Create your views here.
from django.views import View

from order_module.models import OrderModel, OrderDetailModel, DiscountCodeModel
from django.utils.decorators import method_decorator
from product_module.models import ProductModel
from user_module.models import AddressModel
from .forms import DeliveryForm, DeliveryIdForm, DiscountCodeForm

@login_required
def add_to_order(request: HttpRequest):
    product_id = request.GET.get('productId')
    count = int(request.GET.get('count'))
    product = ProductModel.objects.filter(id=product_id).first()

    if request.user.is_authenticated:
        if count < 1:
            return JsonResponse({
                'status': 'count_error'
            })
        else:
            if product is not None:
                if count > product.count:
                    return JsonResponse({
                        'status': 'count_biger_error'
                    })
                else:
                    current_order, created = OrderModel.objects.get_or_create(is_pay=False, user_id=request.user.id)
                    current_product = current_order.orderdetailmodel_set.filter(product_id=product_id).first()
                    if current_product is not None:
                        current_product.count += count
                        product.count = product.count - count
                        product.save()
                        current_product.final_price = current_product.count * product.price
                        current_product.save()
                    else:
                        final_price = count * product.disCount()
                        new_product = OrderDetailModel(product_id=product_id, order_id=current_order.id, count=count, final_price=final_price)
                        product.count = product.count - count
                        product.save()
                        new_product.save()
                    return JsonResponse({
                        'status': 'success'
                    })
            else:
                return JsonResponse({
                    'status': 'count_error'
                })
    else:
        return JsonResponse({
            'status': 'not_login'
        })

@method_decorator(login_required, name='dispatch')
class UserBasket(View):
    def get(self, request:HttpRequest):
        order = OrderModel.objects.filter(user_id=request.user.id, is_pay=False).first()
        if order is not None:
            order_product = OrderDetailModel.objects.filter(order_id=order.id)
            delivery = DeliveryForm()
            discount = DiscountCodeForm()
            if order_product.count() >= 1:
                return render(request, 'order.html', {
                    'products' : order_product,
                    'order' : order,
                    'delivery' : delivery,
                    'discount' : discount
                })
            else:
                return render(request, 'empty_order.html')
        else:
            return render(request, 'empty_order.html')

    def post(self, request:HttpRequest):
        order = OrderModel.objects.filter(user_id=request.user.id, is_pay=False).first()
        delivery = DeliveryForm(request.POST)
        discount = DiscountCodeForm(request.POST)

        if discount.is_valid():
            order_product = OrderDetailModel.objects.filter(order_id=order.id)
            code = discount.cleaned_data.get('DiscountCode')
            get_code = DiscountCodeModel.objects.filter(code=code, is_active=True).first()
            if get_code is not None:
                order.discount_code = get_code
                order.save()
                return render(request, 'order.html', {
                    'products': order_product,
                    'order': order,
                    'delivery': delivery,
                    'discount' : discount
                })

            else:
                discount.add_error('DiscountCode', 'کد وارد شده معتبر نیست.')
                return render(request, 'order.html', {
                    'products': order_product,
                    'order': order,
                    'delivery': delivery,
                    'discount' : discount
                })

        if delivery.is_valid():
            delivery_type = delivery.cleaned_data.get('delivery_type')
            order.delivery_type = delivery_type
            if delivery_type == 'normal':
                order.delivery_price = 10000
            else:
                order.delivery_price = 50000
            order.save()
            return redirect(reverse('checkout'))



def remove_product(request:HttpRequest):
    product_id = request.GET.get('product_id')
    order = OrderModel.objects.filter(user_id=request.user.id, is_pay=False).first()
    product_in_order = OrderDetailModel.objects.filter(order_id=order.id, product_id=product_id).first()
    product = ProductModel.objects.filter(id=product_id).first()
    if product_id is None:
        return JsonResponse({
            'status' : 'id_isnt_valid'
        })
    if product is not None:
        product.count += product_in_order.count
        product.save()
        product_in_order.delete()
        return JsonResponse({
            'status' : 'success'
        })

def change_count(request:HttpRequest):
    product_id = request.GET.get('product_id')
    state = request.GET.get('state')
    if product_id is None or state is None:
        return JsonResponse({
            'status' : 'Not_Found'
        })
    order = OrderModel.objects.filter(user_id=request.user.id, is_pay=False).first()
    if order is None :
        return JsonResponse({
            'status': 'Not_Found'
        })
    product_in_order = OrderDetailModel.objects.filter(order_id=order.id, product_id=product_id).first()
    product = ProductModel.objects.filter(id=product_id).first()
    if state == 'add':
        if product.count >= 1:
            product_in_order.count += 1
            product.count -= 1
            product_in_order.save()
            product.save()
        else:
            return JsonResponse({
                'status': 'Count_Not_Valid'
            })
        delivery = DeliveryForm()
        order_product = OrderDetailModel.objects.filter(order_id=order.id)
        total_price = 0
        for item in order_product:
            total_price += item.finalPrice()
        return JsonResponse({
            'status' : 'Success',
            'body' : render_to_string('basket.html', {
                'products' : order_product,
                'order' : order,
                'delivery' : delivery
            }),
            'totalPrice' : order.total_price(),
            'totlaDiscount' : order.total_discount(),
            'totalWithDelivery': order.total_with_delivery()
        })
    if state == 'mines':
        if product_in_order.count > 1 :
            product_in_order.count -= 1
            product.count += 1
            product_in_order.save()
            product.save()
        else:
            return JsonResponse({
                'status': 'Minimom_Count'
            })
        delivery = DeliveryForm()
        order_product = OrderDetailModel.objects.filter(order_id=order.id)
        total_price = 0
        for item in order_product:
            total_price += item.finalPrice()
        return JsonResponse({
            'status' : 'Success',
            'body' : render_to_string('basket.html', {
                'products' : order_product,
                'order' : order,
                'delivery' : delivery
            }),
            'totalPrice': order.total_price(),
            'totlaDiscount': order.total_discount(),
            'totalWithDelivery' : order.total_with_delivery()
        })

@method_decorator(login_required, name='dispatch')
class CheckOutView(View):
    def get(self, request:HttpRequest):
        order = OrderModel.objects.filter(user_id=request.user.id, is_pay=False).first()
        if order is not None:
            order_product = OrderDetailModel.objects.filter(order_id=order.id)
            address = AddressModel.objects.filter(user_id=request.user.id, is_active=True)
            form = DeliveryIdForm()
            return render(request, 'checkout.html', {
                'order' : order,
                'order_product' : order_product,
                'address' : address,
                'form' : form
            })
        else:
            return redirect(reverse('basket'))

    def post(self, request:HttpRequest):
        order = OrderModel.objects.filter(user_id=request.user.id, is_pay=False).first()
        order_product = OrderDetailModel.objects.filter(order_id=order.id)
        address = AddressModel.objects.filter(user_id=request.user.id)
        form = DeliveryIdForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data.get('delivery_Id')
            print(id)
            order.address_id = id
            order.is_pay = True
            order.pay_datetime = datetime.datetime.now()
            order.save()
            return redirect(reverse('success-pay'))
        else:
            return render(request, 'checkout.html', {
                'order': order,
                'order_product': order_product,
                'address': address,
                'form': form
            })

class SuccessPayment(View):
    def get(self, request):
        return render(request, 'success-payment.html')