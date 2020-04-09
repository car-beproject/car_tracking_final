from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib import messages
from django.template import RequestContext
from .models import *
import cv2
import socket
import base64
import threading
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import os

# Create your views here.
global l_query,u_name_query, u_role_query

l_query = New_location_db.objects.all()


def login(request):
    return render(request, "login.html",{'u_name':request.session.get('u_name')})

def login_action(request):
    u_name_query= request.POST.get('u_name')
    p_word_query= request.POST.get('p_word')
    s_query = Vehicle.objects.all()
    u_query = AuthUser_db.objects.all().filter(u_name = u_name_query).filter(p_word = p_word_query)

    if u_query:
        for u in u_query:
            request.session['role']=(u.u_role)
        request.session['u_name']=u_name_query

        return render(request,"index.html", {'s_query': s_query, 'l_query':l_query, 'u_role':request.session.get('role') ,'u_name':request.session.get('u_name')})
    else :
        fail="login failed"
        return render(request,"login.html",{'fail':fail})

def logout(request):
    del request.session['u_name']
    del request.session['role']
    return render(request, 'login.html')

def index(request):
    if request.session.get('u_name'):
        s_query = Vehicle.objects.all()
        return render(request,"index.html",{'s_query':s_query, 'l_query':l_query, 'u_role':request.session.get('role') ,'u_name':request.session.get('u_name')})
    else:
        return render(request,"login.html")

def search(request):
    if request.session.get('u_name'):
        s_query = Vehicle.objects.all()
        l_query = New_location_db.objects.all()
        license_query = request.GET.get("license_plate")
        if(license_query is not None):
            license_query=license_query.replace(" ", "").upper()
        location_query = request.GET.get("location")
        start_date_query = request.GET.get("start_date")
        end_date_query = request.GET.get("end_date")
        
        if location_query=="All":location_query=""
        if start_date_query=="":start_date_query="1980-01-01"
        if end_date_query=="":end_date_query="2200-01-01"
        if start_date_query > end_date_query:
            info ='Date should be in proper order!!!'
            return render(request,"index.html",{'l_query':l_query,'info':info})
        if license_query or location_query or start_date_query or end_date_query:
            s_query = s_query.filter(license_number__icontains = license_query).filter(location__icontains = location_query).filter(date__range = (start_date_query, end_date_query))    
            if s_query:
                return render(request, "index.html",{'s_query': s_query,'l_query':l_query, 'u_role':request.session.get('role') ,'u_name':request.session.get('u_name')})
            else:
                return render(request, "index.html", {'s_query': s_query,'l_query':l_query, 'u_role':request.session.get('role') ,'u_name':request.session.get('u_name')})
        return render(request, "index.html",{'l_query':l_query, 'u_role':request.session.get('role') ,'u_name':request.session.get('u_name')})
    else:
        return render(request,"login.html")

def vehicle_details(request, id):
    if request.session.get('u_name'):
        s_query = Vehicle.objects.all()
        s_query = s_query.filter(id__icontains = id)
        return render(request, "vehicle_details.html",{'s_query': s_query, 'u_role':request.session.get('role') ,'u_name':request.session.get('u_name')})
    else:
        return render(request,"login.html")
        
def camera_details(request):
    if request.session.get('u_name'):
        c_query = CameraDb.objects.all()
        new_location_query= New_location_db.objects.all()
        new_camera_type_query= New_camera_type_db.objects.all()

        return render(request, "camera_details.html",{'c_query': c_query, 'u_role':request.session.get('role') ,'u_name':request.session.get('u_name'), 'new_location': new_location_query, 'new_camera_type':new_camera_type_query })
    else:
        return render(request,"login.html")
        
def search_camera(request):
    if request.session.get('u_name'):
        ip_address_query=request.GET.get("ip_add")
        location_query=request.GET.get("location")
        if location_query=="All":
            location_query=""
        camera_type_query=request.GET.get("camera_type")
        new_location_query= New_location_db.objects.all()
        new_camera_type_query= New_camera_type_db.objects.all()

        c_query= CameraDb.objects.all()
        c_query = c_query.filter(ip_address__icontains=ip_address_query).filter(camera_type__icontains=camera_type_query).filter(location__icontains=location_query)
        return render(request, "camera_details.html",{'u_role':request.session.get('role') ,'u_name':request.session.get('u_name') ,'c_query': c_query, 'location': location_query, 'camera_type':camera_type_query , 'new_location': new_location_query, 'new_camera_type':new_camera_type_query})
    else:
        return render(request,"login.html")
        
## camera add
def add_cam(request):
    if request.session.get('u_name'):
        new_location_query= New_location_db.objects.all()
        new_camera_type_query= New_camera_type_db.objects.all()

        return render(request,'add_cam.html', {'u_role':request.session.get('role') ,'u_name':request.session.get('u_name'), 'new_location': new_location_query, 'new_camera_type':new_camera_type_query })
    else:
        return render(request,"login.html")
        
def add_cam_action(request):
    if request.session.get('u_name'):
        new_location_query= New_location_db.objects.all()
        new_camera_type_query= New_camera_type_db.objects.all()
        c_query = CameraDb.objects.all()

        ip_address_query = request.GET.get("ip_address")
        location_query = request.GET.get("location").upper()
        camera_type_query = request.GET.get("camera_type")
        q=CameraDb.objects.all().filter(ip_address__exact=ip_address_query)
        
        if q:
            error="Camera IP is already in use!!!"
            return render(request,'add_cam.html',{'u_role':request.session.get('role') , 'u_name':request.session.get('u_name'), 'new_location': new_location_query, 'new_camera_type':new_camera_type_query,'error':error })
        if ip_address_query is not None and camera_type_query is not None and location_query is not None:
            new_camera = CameraDb(ip_address=ip_address_query, location=location_query, camera_type=camera_type_query)
            new_camera.save()
        
        return render(request, 'camera_details.html', {'c_query':c_query,'u_role':request.session.get('role') , 'u_name':request.session.get('u_name')})
    else:
        return render(request,"login.html")
        
def new_details(request):
    if request.session.get('u_name'):
        return render(request,"new_details.html", {'u_role':request.session.get('role') ,'u_name':request.session.get('u_name')})
    else:
        return render(request,"login.html")
        
def new_details_action(request):
    if request.session.get('u_name'):
        new_location_query = request.GET.get("new_location").upper()
        new_camera_type_query = request.GET.get("new_camera_type").upper()
        if new_location_query is not None :
            new_location = New_location_db(location=new_location_query)
            new_location.save()
        if new_camera_type_query is not None:
            new_camera_type = New_camera_type_db(camera_type=new_camera_type_query)
            new_camera_type.save()
        return render(request, 'index.html', {'u_role':request.session.get('role') ,'u_name':request.session.get('u_name')})
    else:
        return render(request,"login.html")

class VideoCamera(object):
    def __init__(self):

        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
        print(1)
        self.video = cv2.VideoCapture(0)
        print(2)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()



def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


global s

@gzip.gzip_page
def livefe(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera()),content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:
        print("aborted")

def stream(request):
    s = socket.socket()
    port = 1789
    s.connect(('127.0.0.1', port))
    msg="Hi".encode()
    s.send(msg)
    s.close()
    return render(request,"stream.html")

def stream_end(request):
    s = socket.socket()
    port = 1789
    s.connect(('127.0.0.1', port))
    print("Socket closed")
    msg="Closing Connection".encode()
    s.send(msg)
    s.close()
    return render(request,"index.html")


def path(request):
        if request.session.get('u_name'):
            return render(request,"path.html", {'u_role':request.session.get('role') ,'u_name':request.session.get('u_name')})
        else:
            return render(request,"login.html")

def path_generator(request):
    if request.session.get('u_name'):
        s_query = Vehicle.objects.all()
        l_query = New_location_db.objects.all()
        license_query = request.GET.get("license_plate")

        s_query = Vehicle.objects.raw('SELECT * FROM search_vehicle where license_number ~ %s order by date, time', [license_query])
            
        return render(request, "path.html",{'s_query':s_query, 'u_role':request.session.get('role') ,'u_name':request.session.get('u_name')})
    else:
        return render(request,"login.html")

def choose_camera(request):
    if request.session.get('u_name'):
        s_query = CameraDb.objects.all()
            
        return render(request, "choose_camera.html",{'s_query':s_query, 'u_role':request.session.get('role') ,'u_name':request.session.get('u_name')})
    else:
        return render(request,"login.html")