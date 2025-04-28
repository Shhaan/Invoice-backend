from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import status,permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
 

class LoginView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        user = authenticate(username=request.data.get('email'), password=request.data.get('password'))
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
             
        else:
            return Response({'error': 'Invalid credentials'}, status=401)

class LogoutView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def post(self, request):
        
        token = Token.objects.filter(user=request.user)
        if not token.exists():
            return Response({"error":True,'message':'No token found'}, status=status.HTTP_400_BAD_REQUEST)
        
        token.delete()
        return Response({"error":False,'message':'logout succesfully'}, status=status.HTTP_200_OK)

class CurrentUserView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        user = request.user 
  
            # You can customize what user data you want to return
        user_data = {
                'id': user.id,
                'email': user.email
                # Add any other fields you want to include
            }
        return Response({"error": False, "data": user_data, "message": "User is authenticated."})
         