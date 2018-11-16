from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from user.forms import UserLoginForm


def login(request):
    if request.method == 'GET':
        # get请求返回页面
        return render(request, 'login.html')

    if request.method == 'POST':
        data = request.POST
        # 将请求参数丢给form表单做检验
        form = UserLoginForm(data)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data.get('username'),
                                     password=form.cleaned_data.get('password'))
            if not user:
                # 用户验证密码不通过
                return render(request, 'login.html')
            # 实现登陆，request.user等于登录系统用户对象
            auth.login(request, user)
            return HttpResponseRedirect(reverse('user:index'))
        else:
            # 验证失败，返回错误信息给页面
            errors = form.errors
            return render(request, 'login.html', {'errors': errors})


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
