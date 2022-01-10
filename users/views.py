from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
import datetime, jwt
from django.conf import settings
from django.http import HttpResponseRedirect

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return redirect('/api/login')

    def get(self, request):
        return render(request, 'users/register.html')
    

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password')

        payload = {
            'password':user.id,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=5),
            'iat':datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')

        response = HttpResponseRedirect('/api/user')
        response.set_cookie('jwt', token)

        return response
    
    def get(self, request):
        return render(request, 'users/login.html')
    

class UserView(APIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'users/users.html'
    def get(self, request):
        token = request.COOKIES.get('jwt')
        print(token)

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Expired Unautheticated')
        
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)

        return render(request, 'users/users.html', {'users':user})

class LogoutView(APIView):
    def post(self, request):
        return redirect('/api/login')

class DeleteView(APIView):
    def get(self, request, pk):
        response = User.objects.get(id = pk)
        response.delete()
        return redirect('/api/user')

class UpdateView(APIView):
    def post(self, request, pk):
        response = User.objects.get(id=pk)
        serializer = UserSerializer(instance = response, data=request.data, partial= True)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response("Error")
        return redirect('/api/user')

    def get(self, request, pk):
        return render(request, 'users/update.html', {'id':id})