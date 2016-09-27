from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
import fb
import json

from . import form

from . import models


# Create your views here.
class ExchangePage(generic.TemplateView):
    template_name = 'exchange/exchange_like.html'
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        kwargs['register_form'] = form.RegisterLikeForm()

        return super(ExchangePage, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'access_token' in request.POST:
            form_regis = form.RegisterLikeForm(request.POST)
            if form_regis.is_valid():
                access_token = request.POST['access_token']
                post_id = request.POST['post_id']

                facebook = fb.graph.api(access_token)

                object_profile = facebook.get_object(cat='single', id='me', fields=['name', 'email'])

                if 'error' not in object_profile:
                    email = object_profile['email']
                    name = object_profile['name']
                    id = object_profile['id']

                    a = models.RegisterLike(id, access_token, name, email)

                    if not models.RegisterLike.objects.filter(id=a.id):
                        datas = models.RegisterLike.objects.all()

                        for data in datas:
                            facebook = fb.graph.api(data.access_token)

                            facebook.publish(cat='likes', id=post_id)

                        a.save()
                        return HttpResponse('<h1 style="text-align: center">Thực hiện thành công, xin vui lòng đợi like về :3</h1>')
                    else:
                        return HttpResponse('<h1 style="text-align: center">Tài khoản đã tồn tại</h1>')

                else:
                    return HttpResponse('<h1 style="text-align: center">Dữ liệu nhập vào sai</h1>')
            else:
                return HttpResponse('<h1 style="text-align: center">Dữ liệu nhập vào sai</h1>')
        else:
            return HttpResponse('<h1 style="text-align: center">Bạn chưa nhập dữ liệu</h1>')


class ImportPage(generic.TemplateView):
    template_name = "exchange/import.html"
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        kwargs['import_form'] = form.ImportForm()

        return super(ImportPage, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'list_token' in request.POST:
            form_import = form.ImportForm(request.POST)
            if form_import.is_valid():
                arr = request.POST['list_token'].split('\r\n')

                for ele in arr:
                    facebook = fb.graph.api(ele)
                    object_profile = facebook.get_object(cat='single', id='me', fields=['name', 'email'])

                    if 'error' not in object_profile:
                        email = object_profile['email']
                        name = object_profile['name']
                        id = object_profile['id']

                        a = models.RegisterLike(id, ele, name, email)

                        if not models.RegisterLike.objects.filter(id=a.id):
                            a.save()

                return HttpResponse(
                    '<h1 style="text-align: center">Thực hiện thành công :3</h1>')

            else:
                return HttpResponse("Error")

        else:
            return HttpResponse("Error")
