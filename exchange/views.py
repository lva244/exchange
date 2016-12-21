from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
import fb
import json
from datetime import timedelta, datetime

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
                    remain_time = datetime.now() + timedelta(hours=1)

                    a = models.RegisterLike(id, access_token, name, email, remain_time)

                    if not models.RegisterLike.objects.filter(id=a.id):
                        datas = models.RegisterLike.objects.all().order_by('?')[:20]

                        for data in datas:
                            facebook = fb.graph.api(data.access_token)

                            facebook.publish(cat='likes', id=post_id)

                        a.save()
                        return HttpResponse(
                            '<h1 style="text-align: center">Thực hiện thành công, xin vui lòng đợi like về :3</h1>')
                    else:
                        person = models.RegisterLike.objects.filter(id=a.id)
                        sub_time = person[0].remain_time.replace(tzinfo=None) - datetime.now()
                        if sub_time.total_seconds() > 0:
                            return HttpResponse(
                                '<h1 style="text-align: center">Bạn phải đợi '
                                + str(round(sub_time.seconds/60)) +
                                ' phút nữa</h1>')
                        else:
                            object = facebook.get_object(cat="single", id=post_id, fields=["id"])
                            if 'error' in object:
                                return HttpResponse(
                                    '<h1 style="text-align: center">Post này chưa được cập nhật trên dữ liệu facebook</h1>')
                            else:
                                datas = models.RegisterLike.objects.all().order_by('?')[:20]

                                for data in datas:
                                    facebook = fb.graph.api(data.access_token)

                                    facebook.publish(cat='likes', id=post_id)

                                person.update(remain_time=datetime.now() + timedelta(hours=1))

                                return HttpResponse(
                                    '<h1 style="text-align: center">Thực hiện thành công, xin vui lòng đợi like về :3</h1>')
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


class GetIdPage(generic.TemplateView):
    template_name = "exchange/get_id.html"
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        kwargs['get_id_form'] = form.GetIdForm()

        return super(GetIdPage, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Kind of links
        https://www.facebook.com/photo.php?fbid=1179583762103605&set=a.102657843129541.3910.100001559768569&type=3&theater
        https://www.facebook.com/chomeolabachuthienha/videos/1087949557979859/
        """

        if 'link' in request.POST:
            link = request.POST['link']
            form_link = form.GetIdForm(request.POST)
            id = "Lỗi định mệnh, chắc link này không lấy được id =))"

            if form_link.is_valid():
                index = link.find("fbid=")
                if index > 0:
                    id = ""
                    first = index + 5
                    last = link.find("&")

                    for i in range(first, last):
                        id += link[i]

                    return HttpResponse('<h1 style="text-align: center">ID nè: ' + id + '</h1>')
                elif link.find("posts") > 0:
                    id = ""
                    index = link.find("posts")
                    first = index + 6

                    if link.find('?') > 0:
                        last = link.find('?')
                    elif link[len(link) - 1] != "/":
                        last = len(link)
                    else:
                        last = len(link) - 1

                    for i in range(first, last):
                        id += link[i]

                    return HttpResponse('<h1 style="text-align: center">ID nè: ' + id + '</h1>')

                elif link.find("videos") > 0:
                    id = ""
                    index = link.find("videos")
                    first = index + 7

                    if link.find('?') > 0:
                        last = link.find('?')
                    elif link[len(link) - 1] != "/":
                        last = len(link)
                    else:
                        last = len(link) - 1

                    for i in range(first, last):
                        id += link[i]

                    return HttpResponse('<h1 style="text-align: center">ID nè: ' + id + '</h1>')

                else:
                    return HttpResponse('<h1 style="text-align: center">' + id + '</h1>')
            else:
                return HttpResponse('<h1 style="text-align: center">Nhập link vào đi</h1>')


class BarCodePage(generic.TemplateView):
    template_name = "exchange/barcode.html"


class ListPage(generic.TemplateView):
    template_name = "exchange/list.html"
