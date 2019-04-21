from django.shortcuts import render
from datetime import *
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.views import generic
from . import tasks
from .tasks import *
from celery.result import AsyncResult
def index(request):
    template = loader.get_template('homes/index.html')
    lastday=(date(2020,8,1)-datetime.today().date()).days
    context = {
        'li': [{"name":"control","link":"homes:"+"control"},{"name":"get","link":"homes:"+"get"}],
        "lastday":lastday,
        # "todo":["程序侧时间","硬件侧时间"][lastday%2],
        "todo": ",共"+str(int(lastday/7))+"周:"+["硬件侧时间","程序侧时间"][int(lastday/7) % 2],
    }
    return HttpResponse(template.render(context, request))

class ControlView(generic.ListView):
    template_name = 'homes/control.html'
    context_object_name = 'li'

    def get_queryset(self):
        """Return the last five published questions."""
        # return Switcher.objects.order_by('-pub_date')[:5]
        return Switcher.objects.all()





#↓开始时进行status Check，确保esp中的东西指令和database一样

from .models import *
def control(request):
    template = loader.get_template('homes/control.html')
    lastday = (date(2020, 8, 1) - datetime.today().date()).days
    li=[]
    for k in Switcher.objects.filter(active=True):
        i=[]
        i.append([k.place+":"+"Controlmod",k.place+":"+"快速模式",1,"on"])
        if k.mobile:i.append([k.place+":"+"Init","载入程序"])
        for j in k.switch_set.all():
            if j.typer=="PWM":
                i.append([k.place + ":" + j.typee, j.name,1, k.place + j.typee,1])
            else:
                i.append([k.place+":"+j.typee,j.name,1, k.place + j.typee])
        li.append(i)
    context = {
        #'li':[[位置,名字,状态]]
        #需要搞事，时间
        'li': li
            # [[主名称，],["test","测试","off"],...]
            ,
    }

    if request.POST:print(request.POST)
    return HttpResponse(template.render(context, request))

def set(request):
    q=request.POST
    fristcsrf=0
    for k in q:
        if not fristcsrf:
            fristcsrf=1
            continue
        tasks.weber.delay(k,q[k])



    return HttpResponseRedirect(reverse('homes:control'))
def get(request):
    print(request)
def change(request,pk):
    for k in request.POST:
        if k=='csrfmiddlewaretoken':continue
        if k=="fastmode":
            if (Switcher.objects.filter(pk=pk)[0].esper.keep!=0) != bool(int(request.POST[k])):
                print("done")
                EspConnection.delay(pk)
            break
        if k=="init":
            P=Switcher.objects.filter(pk=pk)[0]
            P.esper.inited=False
            P.esper.save()
            break
        else:EspConnector.delay(pk,k,request.POST[k])
    data={
        'name':'tom',
        'age':18,
    }
    return HttpResponse(json.dumps(data),content_type="application/json")