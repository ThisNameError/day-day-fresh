from django import forms

from goods.models import GoodsCategory


class GoodsDetailForm(forms.Form):
    name = forms.CharField(max_length=30, required=True,
                           error_messages={'required': '商品名必填',
                                           'max_length': '不能超过30字符'})
    goods_sn = forms.CharField(max_length=30, required=True,
                               error_messages={'max_length': '不能超过30字符',
                                               'required': '商品货号必填'})
    category = forms.CharField(required=True,
                               error_messages={
                                   'required': '商品类目必填'})
    goods_nums = forms.IntegerField(required=True,
                                    error_messages={'required': '商品库存必填'})
    market_price = forms.FloatField(required=True,
                                    error_messages={'required': '市场价格必填'})
    shop_price = forms.FloatField(required=True,
                                  error_messages={'required': '本店价格必填'})
    goods_brief = forms.CharField(max_length=500, required=True,
                                  error_messages={'max_length': '不能超过500字符',
                                                  'required': '描述必填'})
    goods_front_image = forms.ImageField(required=False)

    def clean_category(self):
        id = self.cleaned_data.get('category')
        # 获取对象
        category = GoodsCategory.objects.filter(pk=id).first()

        return category
