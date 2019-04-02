from decimal import Decimal
from random import SystemRandom
from functools import reduce

from django import forms
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from website.views import PlusMemberCheck
from problem.models import ProblemAuthLog
from .models import Shop, ShopItem, ShopPurchaseLog
from problem.helpers.problem_info import get_problem_list_info


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
            shops = Shop.objects.get(pk=int(pk))
        
        infos = []
        for shop in shops:
            shop_items = shop.shop_items.filter(hidden=False)
            _ , user_money = get_problem_list_info(shop.problem_list, request.user)
            purchase_log = list(map(lambda x: x.item.price, ShopPurchaseLog.objects.filter(user=request.user, shop=shop)))
            if purchase_log:
                user_money -= reduce(lambda x,y: x+y, purchase_log)

            infos.append({
                'shop': shop,
                'shop_items': shop_items,
                'user_money': user_money
            })

        return render(request, 'shop/prod.html', {
            'shop_infos': infos
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

        _ , user_money = get_problem_list_info(shop.problem_list, request.user)
        user_money -= reduce(lambda x,y: x+y, map(lambda x: x.item.price, ShopPurchaseLog.objects.filter(user=request.user)))

        enough_point = \
            (True if user_money >= required_point \
            else False)
        enough_luck = \
            (True if SystemRandom().uniform(0, 100) > required_luck \
            else False)

        

        if enough_point:
            succeed_purchase = enough_point and enough_luck 

            try:
                ShopPurchaseLog.objects.create( \
                    user=request.user, shop=shop_to_visit, \
                    item=item_to_buy, succeed=succeed_purchase)

                response['result'] = succeed_purchase
                if not enough_luck:
                    response['reason'] = 'Not enough luck!'

            except IntegrityError:
                response['result'] = False
                response['reason'] = 'Something is wrong!'

        else:
            response['result'] = False
            if not enough_point:
                response['reason'] = 'Not enough point!'
        
        return JsonResponse(response)


        

        
