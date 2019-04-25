import socket

import jwt
from django.conf import settings
from django.contrib.auth import authenticate, login, user_logged_in
from django.forms import forms
from django.http import HttpResponse, HttpResponseRedirect, Http404, response
from django.shortcuts import render, redirect
from datetime import datetime

from rest_framework.decorators import permission_classes, api_view, action
# from  import settings
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.serializers import jwt_payload_handler

from .serializers import FollowingUsersSerializer, ProfileSerializer
from .models import *
from .forms import UserRegisterForm, UserLoginForm, WishListForm
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, HomeDataSerializer, ProductSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView


@api_view(['POST'])
def index(request):
    # if request.POST:
    #     name=request.GET['firstname']
    #     print(name)
    # else:
    #     return HttpResponse('invalid')
    pn = "9848023455"
    print("this is test")
    profile_name = profile.objects.all()
    for i in profile_name:
        print(i.firstname, i.lastname, i.birthday, i.bloodgroup, i.phonenumber)
        if i.phonenumber == pn:
            print("match")
    return HttpResponse('good')


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email = userObj['email']
            password = userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
    else:
        form = UserRegisterForm()
    return render(request, "chahana/nav.html", {'form': form})


# def user_register(request):
#     print(request.POST)
#     if request.method == "POST":
#         form=UserRegisterForm(request.POST)
#         print(form)
#         if form.is_valid():
#             userObj = form.cl
# eaned_data
#             username = userObj['username']
#             email =  userObj['email']
#             if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
#                 form.save()
#     else:
#         form=UserRegisterForm()
#     context ={
#         'form': form,
#     }
#     return render(request, 'chahana/nav.html', context)

def user_profile(request):
    print(request.POST)
    if request.method == "POST":
        firstname = request.POST.getlist('first')
        secondname = request.POST.getlist('last')
        birthday = request.POST.getlist('birthday')
        blood = request.POST.getlist('blood')
        photo = request.POST.getlist('photo')
        phonenumber = request.POST.getlist('phonenumber')

        print(firstname, secondname, birthday, blood)
        date = datetime.strptime(birthday[0], '%Y-%m-%d')
        p = profile(firstname=firstname[0], lastname=secondname[0], birthday=date, bloodgroup=blood[0], photo=photo[0],
                    phonenumber=phonenumber[0])
        p.save()
    else:
        pass
    return render(request, 'chahana/profile.html')


# class LoginView(APIView):
#    def post(self, request, *args, **kwargs):
#         if not request.data:
#             return Response({'Error': "Please provide username/password"}, status="400")
#
#         username = request.data['username']
#         password = request.data['password']
#         try:
#             user = Register.objects.get(username=username, password=password)
#         except Register.DoesNotExist:
#             return Response({'Error': "Invalid username/password"}, status="400")
#         if user:
#             payload = {
#                 'id': user.id,
#                 'email': user.email,
#             }
#             jwt_token = {'token': jwt.encode(payload, "SECRET_KEY")}
#
#             return HttpResponse(
#             json.dumps(jwt_token),
#             status=200,
#             content_type="application/json"
#         )
#         else:
#             return Response(
#             json.dumps({'Error': "Invalid credentials"}),
#             status=400,
#             content_type="application/json"
#         )

def user_login(request):
    if request.method == 'POST':
        print(request.POST)
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                # User.objects.create_user(username, password)
                login(request, user)
                data = ["A+", "B+", "O+", "AB+", "A-", "B-", "O-"]
                use = User.objects.all()
                arr = []
                for i in use:
                    name = i.username
                    namesId = i.id
                    arr.append({
                        'names': name,
                        'id': namesId
                    })
                    # form=WishListForm()

                return render(request, 'chahana/following.html', {'data': data, 'use': arr, 'username': username})

            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
    else:
        print("External else is called")
        form = UserLoginForm()
        followers = FollowingUsers.objects.all()
        user = User.objects.all()
        context = {
            'form': form,
            'followers': followers,
            'user': user,
        }
        return render(request, "chahana/login.html", context)


class CreateUserAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request):
        print(request.POST)
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes((AllowAny,))
def authenticate_user(request, format=None):
    print(request.data)
    try:
        print("jsnvsj")
        # user_obj=None
        email = request.data['email']
        # email = "Bbb@gmail.com"
        # print(email)
        password = request.data['password']
        # password = "1234"
        user_detail = User.objects.filter(email=email)
        if user_detail.exists():
            user = authenticate(username=user_detail.first().username, password=password)
            # print(user)
            # login(request, user)
        else:
            res = {'error': 'email doesnot exists'}
            return Response(res)
        if user:
            try:
                print("hi")
                user_details = {}
                payload = jwt_payload_handler(user_detail.first())
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details['username'] = "%s " % (
                    user_detail.first().username)
                user_details['token'] = token
                # prof = profile.objects.all()
                # for i in prof:
                #
                #     if user_detail.first().id==int(i.user_id_id):
                #
                #         print(user_detail.first().id)
                #         user_details['firstname'] = "%s" % (i.firstname)
                #         user_details['lastname'] = "%s" % (i.lastname)
                #         user_details['birthday'] = "%s" % (i.birthday)
                #         user_details['bloodgroup']= "%s" %(i.bloodgroup)
                #         user_details['phonenumber'] = "%s" % (i.phonenumber)
                print(user_details)

                # user_logged_in.send(sender=user.__class__,
                #                     request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)

                # user_logged_in.send(sender=user.__class__,
                #                     request=request, user=user)
                # return Response(user_details, status=status.HTTP_200_OK)

            except Exception as e:
                raise e


        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response(res)


# class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
#     # Allow only authenticated users to access this url
#     permission_classes = (IsAuthenticated,)
#     serializer_class = UserSerializer
#
#     def get(self, request, *args, **kwargs):
#         # serializer to handle turning our `User` object into something that
#         # can be JSONified and sent to the client.
#         serializer = self.serializer_class(request.user)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, *args, **kwargs):
#         serializer_data = request.data.get('user', {})
#
#         serializer = UserSerializer(
#             request.user, data=serializer_data, partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class CreateProfileAPIView(APIView):
    serializer_class = ProfileSerializer
    queryset = profile.objects.all()
    # permission_classes([IsAuthenticated, ])
    permission_classes = (IsAuthenticated,)

    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    # permission_classes = (IsAuthenticated,)
    # permission_classes([IsAuthenticated, ])

    def post(self, request):
        print(request.data)
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')
        birthday = request.data.get("birthday")
        bloodgroup = request.data.get("bloodgroup")
        phonenumber = request.data.get("phonenumber")
        print(user_id_id)

        probj = profile(
            firstname=firstname,
            lastname=lastname,
            birthday=birthday,
            bloodgroup=bloodgroup,
            phonenumber=phonenumber,
            user_id=user_id_id,
        )
        probj.save()

        return Response({"sucess": "Profile created successfully"})

    def get(self, request, format=None):
        print(request.data)
        user_id = request.user.id
        # external=[]
        # user_id_ = request.POST.get("user_id")
        is_profile_exists = profile.objects.filter(user_id_id=user_id).order_by("-id")
        if is_profile_exists.exists():
            prof = is_profile_exists.first()
            # for i in prof:
            data = {
                'firstname': prof.firstname,
                'lastname': prof.lastname,
                'birthday': prof.birthday,
                'bloodgroup': prof.bloodgroup,
                'phonenumber': prof.phonenumber
            }

            # serializeData = ProfileSerializer([data], many=True)
            return Response(data)
        else:
            return Response({"error": "Profile not found."})

        # if hasattr(request.user, 'profile'):
        #     profile_obj = request.user.profile
        # else:
        #     return Response({"error" : "Profile not found."})

        # print(request.POST)

        # host = request.META.get('HTTP_X_FORWARDED_FOR')

        # external = []
        # prof = profile.objecs.filter()
        # # user=User.objects.all()host = socket.gethostname()
        #
        # for i in prof:
        #
        #     if username_obj.exists():
        #         external.append({
        #             'firstname': i.firstname,
        #             'lastname': i.lastname,
        #             'birthday': i.birthday,
        #             'bloodgroup': i.bloodgroup,
        #             'phonenumber': i.phonenumber
        #         })
        # val = {}
        # val["value"] = external
        #
        # serializeData = ProfileDataSerializer([val], many=True)
        # return Response(serializeData.data)

        # print(request.POST)
        # user = request.data
        # serializer = ProfileSerializer(data=user)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def post(self,request):
    #         print(request.POST)
    #         user_id_id = User.objects.get(id=request.user.id)
    #         firstname = request.POST.get('firstname')
    #         print(firstname)
    #         lastname = request.POST.get('lastname')
    #         birthday = request.POST.get('birthday')
    #         phonenumber= request.POST.get('phonenumber')
    #
    #         serializer = ProfileSerializer(
    #             firstname=firstname,
    #             lastname=lastname,
    #             birthday=birthday,
    #             phonenumber=phonenumber,
    #             user_id_id=user_id_id,
    #
    #         )
    #
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
 # def create(self, validated_data):
    #
    #     create_user=User.objects.create(
    #     mobile=validated_data['mobile'],
    #     full_name=validated_data['full_name'],
    #     user_type=validated_data['user_type'],
    #     )
    #
    #     create_user.set_password(validated_data['password'])
    #     create_user.set_password(validated_data['confirm_password'])
    #     create_user.save()
    #     return create_user

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def search(request):
    if request.method == 'POST':
        print(request.POST)
        # host = request.get_host()
        username = request.data.get('username')
        detail = User.objects.filter(username=username)


        for i in detail:
            a=i.username
            # a=i.user_id.username
            print(a)
            user_in_follow = FollowingUsers.objects.filter(user=a).filter(
                user_id=request.user).count()
            print(user_in_follow)
            following = True
            if user_in_follow == 0:
                following = False
            data = {
                # 'photo': '',

                'firstname':i.firstname,
                'follwing':following

            }
            print(data)

            return Response(data)
        else:
            return Response({"error": "not found"})


@api_view(['POST'])
def follow(request):
    if request.method=='POST':
        print(request.data)
        username=request.data['following_name']
        useruser=request.data['user']
        print(useruser)
        # a = FollowingUsers(following_name=username,user_id= useruser)
        user = User.objects.filter(username=useruser)
        if not user.exists():
            return Response({'message':'failed'})
        # print(user.id)
        # print(user.id)
        a = FollowingUsers.objects.create(following_name=username,user_id= user.first().id)
        # a.save()
        # if a:
        if a:
            return Response({'message':'success'})

def followinguserss(request, id):
        user = User.objects.get(id=id)
        foll = FollowingUsers.objects.all()
        return render(request, 'chahana/followinguserss.html', {'user': user, 'foll': foll})

def deleteUsers(request, id):
        foll = FollowingUsers.objects.get(id=id).delete()
        return HttpResponse('succesfully unfollowed')

def completeUser(request, id):
        foll = FollowingUsers.objects.get(id=id)
        return render(request, 'chahana/complete.html', {'user': foll})

def create1(request, id):
        user = User.objects.get(id=id)
        if request.POST:
            # item_name = request.POST.get('item_name')
            # img_name=request.POST.get('img_name')
            # print()
            # a = Wish_list(item_name=item_name,img_name=img_name)
            # a.save()
            # if a:
            #     return HttpResponse('success')
            # else:
            #     return HttpResponse('failed')

            form = WishListForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return HttpResponse('success')
            else:
                return HttpResponse('form error')
        else:
            form = WishListForm()

            return render(request, 'chahana/index1.html', {'form': form, 'user': user})

class HomePageView(APIView):
        serializer_class = HomeDataSerializer
        permission_classes = (AllowAny,)

        # @action(detail=True, methods=['post'])

        def get(self, request, format=None):
            # print(request.POST)

            # host = request.META.get('HTTP_X_FORWARDED_FOR')
            host = request.get_host()
            external = []
            wish = Wish_list.objects.all()
            # user=User.objects.all()host = socket.gethostname()

            for i in wish:
                username_obj = User.objects.filter(id=int(i.user_id_id))
                username = " "
                if username_obj.exists():
                    username = username_obj.first().username

                # print(i.item_name, i.img_name, i.user_id)
                # external.append([i.item_name,request.get_host()+str(i.img_name),str(i.user_id)])
                external.append({
                    'item_name': i.item_name,
                    'img_name': str(request.scheme) + '://' + host + '/media' + '/' + str(i.img_name),
                    'user_name': username
                })
            val = {}
            val["value"] = external

            serializeData = HomeDataSerializer([val], many=True)
            return Response(serializeData.data)

        def post(self, request):
            # print(request.data, request.FILES)
            item_name = request.data.get('item_name')
            img_nae = request.FILES['img_name']
            user = request.data.get("user_name")
            user_id = request.user

            wishlistObj = Wish_list(
                item_name=item_name,
                img_name=request.FILES['img_nae'],
                user_name=user,
                user_id=user_id
            )
            wishlistObj.save()

            return Response({"sucess": "done"})
        def delete(self,request):
            id=request.user.id
            give1=Wish_list.objects.filter(user_id=id)
            give1.delete()
            return Response({'message':'Deleted Successfully'})


class productClass(ModelViewSet):
        # queryset = Product.objects.all()
        serializer_class = ProductSerializer

        @action(detail=True, methods=['get'])
        def get_queryset(self):
            print(self.kwargs)
            return Product.objects.filter(subcat_id=self.kwargs.get('id'))

class Foll(APIView):
        serializer_class = FollowingUsersSerializer

        # queryset = FollowingUsers.objects.all()
        # @action(detail=True, methods=['post'])

        def get(self, request, format=None):
            # print(request.POST)

            host = socket.gethostbyname(socket.gethostname())
            external = []
            foll = FollowingUsers.objects.all()

            for i in foll:
                print(i.user_id)
                # foll_obj = FollowingUsers.objects.filter(id=int(i.user_id))
                # print(foll_obj)
                # username = ""
                # if foll_obj.exists():
                #     print("pass")
                #     username = i.user
                # username = foll_obj.first().user
                a = i.user_id
                user = User.objects.get(id=a)
                username = user.username
                external.append({
                    'following_name': i.following_name,
                    'user': username
                })
            val = {}
            val["value"] = external

            serializeData = FollowingUsersSerializer([val], many=True)
            return Response(serializeData.data)

        def post(self, request):
            print(request.POST)
            following_name = request.POST.get('following_name')
            user = request.POST.get("user")
            user_id = User.objects.get(username=user)

            foll = FollowingUsers(
                following_name=following_name,
                user=user,
                user_id=user_id
            )
            foll.save()

            return Response({"sucess": "done"})
