from decimal import Decimal
from random import SystemRandom
from functools import reduce

from django import forms
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views import View

from website.views import PlusMemberCheck
from problem.helpers.problem_info import get_problem_list_info
from .models import Shop, ShopItem, ShopPurchaseLog


class ShopInvenView(PlusMemberCheck, View):
    def get(self, request):
        purchase_logs = ShopPurchaseLog.objects.filter(user=request.user).order_by('-purchase_time')

        return render(request, 'shop/inven.html', {
            'purchase_logs': purchase_logs
        })


class ShopProdView(PlusMemberCheck, View):
    def get(self, request, pk=None):
        if pk is None:
            shops = Shop.objects.all()
        else:
            shops = Shop.objects.filter(problem_list__pk=int(pk))
            if not shops.exists():
                raise Http404

        infos = []
        for shop in shops:
            shop_items = shop.shop_items.filter(hidden=False)
            _, user_money = get_problem_list_info(shop.problem_list, request.user)
            purchase_log = list(map(lambda x: x.item.price, ShopPurchaseLog.objects.filter(user=request.user, shop=shop)))
            if purchase_log:
                user_money -= reduce(lambda x, y: x+y, purchase_log)

            infos.append({
                'shop': shop,
                'shop_items': shop_items,
                'user_money': user_money
            })

        return render(request, 'shop/prod.html', {
            'shop_infos': infos
        })


class ShopBuyForm(forms.Form):
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

        shop_items = shop_to_visit.shop_items.all()
        shop_point_source = shop_to_visit.problem_list

        if item_to_buy not in shop_items:
            return HttpResponseBadRequest()

        response = {}
        required_point = item_to_buy.price
        required_luck = Decimal(100) - item_to_buy.chance

        _, user_money = get_problem_list_info(shop_point_source, request.user)
        purchase_log = list(map(lambda x: x.item.price, ShopPurchaseLog.objects.filter(user=request.user, shop=shop_to_visit)))
        if purchase_log:
            user_money -= reduce(lambda x, y: x+y, purchase_log)

        enough_point = (True if user_money >= required_point else False)
        enough_luck = (True if SystemRandom().uniform(0, 100) > required_luck else False)
        enough_stock = (True if item_to_buy.stock > 0 else False)

        if enough_point and enough_stock:
            succeed_purchase = enough_luck

            try:
                ShopPurchaseLog.objects.create(
                    user=request.user, shop=shop_to_visit,
                    item=item_to_buy, succeed=succeed_purchase, retrieved=False)

                response['result'] = succeed_purchase
                if enough_luck:
                    item_to_buy.stock -= 1
                    item_to_buy.save()
                else:
                    response['reason'] = 'Not enough luck!'

            except IntegrityError:
                response['result'] = False
                response['reason'] = 'Something is wrong!'

        else:
            response['result'] = False
            if not enough_point:
                response['reason'] = 'Not enough points!'
            elif not enough_stock:
                response['reason'] = 'Not enough stock!'

        return JsonResponse(response)


class ShopRetrieveView(PlusMemberCheck, View):
    def post(self, request, pk):
        try:
            log = ShopPurchaseLog.objects.get(pk=int(pk))
        except ObjectDoesNotExist:
            raise Http404

        if log.user != request.user or log.retrieved or not log.succeed:
            return HttpResponseBadRequest()

        response = {}
        try:
            log.retrieved = True
            log.save()
            response['result'] = True
        except IntegrityError:
            response['result'] = False
            response['reason'] = 'Something is wrong!'

        return JsonResponse(response)
