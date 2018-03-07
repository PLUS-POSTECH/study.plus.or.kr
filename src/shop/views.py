from decimal import Decimal
from random import SystemRandom

from django import forms
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views import View

from website.views import PlusMemberCheck
from .models import Shop, ShopItem, ShopPurchaseLog

class ShopListView(PlusMemberCheck, View):
    def get(self, request, pk):
        shop = Shop.objects.get(pk=int(pk))
        item_list = shop.item_list

        available_points = 0

        return render(request, 'shop/list.html', {
            'item_list': item_list,
            'available_points': available_points
        })


class ShopBuyForm(PlusMemberCheck, View):
    item = forms.IntegerField()


class ShopPurchaseView(PlusMemberCheck, View):
    def post(self, request, pk):
        form = ShopBuyForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest()

        shop_item_id = form.cleaned_data['item']

        try:
            shop_to_visit = Shop.objects.get(pk=int(pk))
            item_to_buy = ShopItem.objects.get(pk=int(shop_item_id))
        except ObjectDoesNotExist:
            raise Http404

        shop_items = shop_to_visit.shop_items
        shop_point_source = shop_to_visit.problem_list

        if not item_to_buy in shop_items:
            return HttpResponseBadRequest()

        response = {}
        required_point = item_to_buy.price
        required_luck = Decimal(100) - item_to_buy.chance

        enough_point =
        enough_luck = \
            (True if SystemRandom().uniform(0, 100) > required_luck \
            else False)

        succeed_purchase = enough_point and enough_luck

        try:
            ShopPurchaseLog.objects.create( \
                user=request.user, shop=shop_to_visit, \
                item=item_to_buy, succeed=succeed_purchase)

            response['result'] = succeed_purchase
            if not enough_point:
                response['reason'] = 'Not enough point!'
            elif not enough_luck:
                response['reason'] = 'Not enough luck!'

        except IntegrityError:
            response['result'] = False
            response['reason'] = 'Something is wrong!'

        finally:
            return JsonResponse(response)
