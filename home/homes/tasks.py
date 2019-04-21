from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import *
import socket,time
import platform
# for k in EspSaver.objects.filter():
#     k.remoting=0
#     k.save()
import sys
n=socket.gethostname()
nn=platform.system()
if nn=="Windows":
    if n=="Toms2":
        sys.path.append(r"C:\Users\t\Documents\PycharmProjects\impors")
    else:sys.path.append("C:/workspace/impors")
else:sys.path.append("/home/pi/PycharmProjects/impors")
# import homecontrol.webuser as web
from homecontrol.webusssser import *

def sayerhandler(switch,state,s:Switcher):
    nsay=[]

    s.esper.refresh_from_db()
    print(s.esper.inited)
    print("didid")
    if s.esper.mobile:
        s.esper.refresh_from_db()
        if not s.esper.inited:
            defdic={'D0': 16, 'D1': 5, 'D2': 4, 'D3': 0, 'D4': 2, 'D5': 14, 'D6': 12, 'D7': 13, 'D8': 15, 'RX': 3, 'TX': 1}
            nsay = ["\x03", "from machine import *"]
            for Sw in s.switchee_set.all():
                if hasattr(Sw, "pwm"):pass
                elif hasattr(Sw, "switch"):pass
                else:
                    print(Sw)
                    import inspect
                    print(inspect.getmembers(Sw, lambda a: not (inspect.isroutine(a))))
                q=Sw.place
                if q in defdic:
                    j = defdic[q]
                    defdic.pop(q)
                else:
                    print("error,No PinDefined",end="  ")
                    q,j=defdic.popitem()
                j=str(j)
                if hasattr(Sw, "pwm"):
                    nsay.append(q + "=PWM(Pin("+j+"), freq=50)")
                elif hasattr(Sw, "switch"):
                    nsay.append(q+"=Pin("+j+",Pin.OUT)")
            s.esper.inited=True
            s.esper.save()
    if switch:
        Sw = s.switchee_set.filter(pk=switch)[0]
        if hasattr(Sw, "pwm"):
            if Sw.reverse: state = Sw.pwm.max - state
            Swit = Sw.place + ".duty(" + str(state) + ")"
        elif hasattr(Sw, "switch"):

            # Sw.state=state
            if Sw.reverse: state = 1 - state

            Swit = Sw.place + ".value(" + str(state) + ")"
        else:
            print(Sw)
            import inspect
            print(inspect.getmembers(Sw, lambda a: not (inspect.isroutine(a))))
        nsay.append(Swit)

    q=""
    for k in nsay:
        q+=k
        q+="\n"
    print("sayer:"+q)
    return q



import socket,json
@shared_task
def EspConnection(place,timeout=3,ttime=60):
    G=Switcher.objects.filter(pk=place)[0].esper
    while G.keep==1:
        if not timeout:
            G.keep=0
            G.save()
            break
        time.sleep(1)
        timeout-=1
        Esper.refresh_from_db(G)
    if G.keep:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # s.sendto(bytes(json.dumps([0]), encoding="utf-8"), ("localhost", G.keep))
        s.sendto(b"0", ("localhost", G.keep))
        s.close()
        while G.keep:
            if not timeout:
                G.keep = 0
                G.save()
                break
            time.sleep(1)
            timeout -= 1
            Esper.refresh_from_db(G)
    else:
        G.keep=8080+int(place)
        G.save()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('localhost', G.keep))
        s.settimeout(1)
        qtime=ttime
        C=espweber(G.place,1)
        while qtime:
            try:
                # recv = json.loads(str(s.recv(8192), encoding="utf-8"))[0]
                recv = str(s.recv(8192), encoding="utf-8")
                if recv=="0":break
                # webusEsp(recv[0],recv[1],recv[2])
                print("recc++:",recv,end=" ")
                C.saylines(recv)
                qtime=ttime
            except (BlockingIOError , socket.timeout):pass
            # 更新
            # C.saylines(sayerhandler("",0,Switcher.objects.filter(pk=place)[0]))
            # time.sleep(1)
            qtime-=1
        C.turnoff()
        s.close()
        G.keep=0

@shared_task
def EspConnector(place,switch,state,timeout=2):
    print(place,switch,state,end=",")
    C=Switcher.objects.filter(pk=place)[0]
    G=C.esper
    while G.keep==1:
        if not timeout:
            G.keep=0
            G.save()
            # Esper.refresh_from_db(G)
            break
        time.sleep(1)
        timeout-=1
        Esper.refresh_from_db(G)
    state=int(state)
    print("place:",place,end="")
    Swit=sayerhandler(switch,state,C)
    print("did")
    if G.keep:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # s.sendto(bytes(json.dumps([Swit]),encoding="utf-8"),("localhost",G.keep))
        s.sendto(bytes(Swit,encoding="utf-8"),("localhost",G.keep))
        s.close()
    else:
        G.keep=1
        G.save()
        # webusEsp(C.esper.place,Sw.place,state)
        print("nor++:",G.place,Swit,end=" ")
        Log = logging.getLogger()
        Log.setLevel(logging.DEBUG)
        CC=espweber(G.place,1,Log)
        CC.saylines(Swit)
        time.sleep(1)
        CC.turnoff()
        G.keep=0
        G.save()
# from celery.schedules import crontab
# from celery.decorators import periodic_task

# @shared_task
# def A():
#     EspConnector(4,6,0)

@shared_task
def Test():
    print("hihihihihihi")

