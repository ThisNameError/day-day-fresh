from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from goods.forms import GoodsDetailForm
from goods.models import GoodsCategory, Goods


def goods_category_list(request):
    if request.method == 'GET':
        # 返回商品分类
        categorys = GoodsCategory.objects.all()
        types = GoodsCategory.CATEGORY_TYPE
        return render(request, 'goods_category_list.html', {'categorys': categorys, 'types': types})


def goods_category_detail(request, id):
    if request.method == 'GET':
        # 返回商品对象，分类枚举信息
        category = GoodsCategory.objects.filter(pk=id).first()
        types = GoodsCategory.CATEGORY_TYPE

        return render(request, 'goods_category_detail.html',
                      {'category': category, 'types': types})

    if request.method == 'POST':
        img = request.FILES.get('category_front_image')
        if img:
            category = GoodsCategory.objects.filter(pk=id).first()
            category.category_front_image = img
            category.save()
            return HttpResponseRedirect(reverse('goods:goods_category_list'))
        else:
            error = '图片必填'
            return render(request, 'goods_category_detail.html', {'error': error})


def goods_list(request):
    if request.method == 'GET':
        # 获取分页页码
        try:
            page = int(request.GET.get('page', 1))
        except Exception as e:
            page = 1
        goods = Goods.objects.all()
        types = GoodsCategory.CATEGORY_TYPE
        # 分页，使用Paginator库
        paginator = Paginator(goods, 2)
        goods = paginator.page(page)
        return render(request, 'goods_list.html', {'goods': goods, 'types': types})


def goods_add(request):
    if request.method == 'GET':
        categorys = GoodsCategory.CATEGORY_TYPE
        return render(request, 'goods_detail.html', {'categorys': categorys})

    if request.method == 'POST':
        # 表单验证
        form = GoodsDetailForm(request.POST, request.FILES)
        if form.is_valid():
            # Goods.objects.create(
            #     name=form.cleaned_data.get('name'),
            #     goods_sn=form.cleaned_data.get('goods_sn'),
            #     category_id=form.cleaned_data.get('category'),
            #     goods_num=form.cleaned_data.get('goods_num'),
            #     market_price=form.cleaned_data.get('market_price'),
            #     shop_price=form.cleaned_data.get('shop_price'),
            #     goods_brief=form.cleaned_data.get('goods_brief'),
            #     goods_front_image=form.cleaned_data.get('goods_front_image')
            # )
            # 创建
            data = form.cleaned_data
            Goods.objects.create(**data)
            return HttpResponseRedirect(reverse('goods:goods_list'))
        else:
            # 验证失败
            return render(request, 'goods_detail.html', {'errors': form.errors})


def goods_del(request, id):
    if request.method == 'POST':
        # 删除商品数据，使用Ajax
        Goods.objects.filter(pk=id).delete()
        return JsonResponse({'code': 200, 'msg': '请求成功'})


def goods_edit(request, id):
    if request.method == 'GET':
        # 编辑商品对象
        goods = Goods.objects.filter(pk=id).first()
        types = GoodsCategory.CATEGORY_TYPE
        return render(request, 'goods_detail.html', {'goods': goods, 'types': types})

    if request.method == 'POST':
        # 1.form表单校验
        form = GoodsDetailForm(request.POST, request.FILES)
        if form.is_valid():
            # 验证成功
            data = form.cleaned_data
            # 把图片从data中删掉，
            # img表示更新商品时，选择了图片，则img为图片内容
            # 如果没有选择图片，img为None
            img = data.pop('goods_front_image')
            # 更新除了图片的信息
            Goods.objects.filter(pk=id).update(**data)
            if img:
                # 更新图片的信息
                goods = Goods.objects.filter(pk=id).first()
                goods.goods_front_image = img
                goods.save()
            return HttpResponseRedirect(reverse('goods:goods_list'))
        else:
            goods = Goods.objects.filter(pk=id).first()
            types = GoodsCategory.CATEGORY_TYPE
            return render(request, 'goods_detail.html', {'errors': form.errors, 'goods': goods, 'types': types})


def goods_desc(request, id):
    if request.method == 'GET':
        # TODO: 返回商品对象，并刷新编辑内容
        goods = Goods.objects.filter(pk=id).first()

        return render(request, 'goods_desc.html', {'goods': goods})

    if request.method == 'POST':
        # 获取编辑器内容
        content = request.POST.get('content')
        # 获取修改商品对象
        goods = Goods.objects.filter(pk=id).first()
        goods.goods_desc = content
        goods.save()
        return HttpResponseRedirect(reverse('goods:goods_list'))
