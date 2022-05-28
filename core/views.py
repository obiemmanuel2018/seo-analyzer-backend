from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer,SignupSerializer,LoginSerializer\
    ,LogoutSerializer,EmailChangeSerializer,EmailChangeVerifySerializer,PasswordChangeSerializer\
        ,PasswordResetSerializer,PasswordResetVerifiedSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status
from django.utils.translation import gettext as _
from .utils import get_access_token,send_verification_mail
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import SignupCode,PasswordResetCode,EmailChangeCode,send_multi_format_email
from datetime import date
from drf_yasg.utils import swagger_auto_schema
# Create your views here.





class Signup(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer
    
    @swagger_auto_schema(responses={200: SignupSerializer(many=True)}, request_body=SignupSerializer)
    def post(self, request, format=None):
        """
        Register new User
    
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
        
            name = serializer.data['name']
            email = serializer.data['email']
            password = serializer.data['password']
            
            must_validate_email = getattr(settings, "AUTH_EMAIL_VERIFICATION", True)
          
            try:
                user = get_user_model().objects.get(email=email)
               
                if user.is_verified:
                    content = {'detail': _('Email address already taken.')}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

                try:
                    # Delete old signup codes
                    signup_code = SignupCode.objects.get(user=user)
                    signup_code.delete()
                except SignupCode.DoesNotExist:
                    pass

            except get_user_model().DoesNotExist:
             
                user = get_user_model().objects.create_user(
                    email=email,
                    name=name
                    )

            # Set user fields provided
            user.set_password(password)
            if not must_validate_email:
                user.is_verified = True
                send_multi_format_email('welcome_email',
                                        {'email': user.email, },
                                        target_email=user.email)
            user.save()
            if must_validate_email:
               send_verification_mail(request,user)
            auth_data = get_access_token(email,password)
            content = {'name':name,'email': email}
            auth_data['user'] = content
            return Response(auth_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupVerify(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'core/signup_verify_message.html'
    

    def get(self, request, format=None):
        """
        Very User Email
        
        """
        code = request.GET.get('code', '')
        verified = SignupCode.objects.set_user_is_verified(code)

        if verified:
            try:
                signup_code = SignupCode.objects.get(code=code)
                signup_code.delete()
            except SignupCode.DoesNotExist:
                pass
            content = {'success': _('Email address verified.')}
            return Response(content)
        else:
            content = {'detail': _('Unable to verify user.')}
            return Response(content)

class ResendVerificationLink(APIView):
      permission_classes = (IsAuthenticated,)
      def get(self,request,format=None):
          """
          Resend User Verification Link
          """
          try:
             user = get_user_model().objects.get(email=request.user)
             send_verification_mail(request,user)
             return Response({'message':'Verification Linked Sent Successfully'},status=status.HTTP_200_OK)
          except get_user_model().DoesNotExist:
              return Response({"error":"Uaer matching query doesn't exist"})
      

class Login(APIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            try:
                user = get_user_model().objects.get(email=email)
                if user.is_active:
                        auth_data = get_access_token(email,password)
                        return Response(auth_data,
                                        status=status.HTTP_200_OK)
                else:
                    content = {'detail': _('User account not active.')}
                    return Response(content,
                                        status=status.HTTP_401_UNAUTHORIZED)

            except get_user_model().DoesNotExist:
                content = {'detail':
                           _('Unable to login with provided credentials.')}
                return Response(content, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)
  
    
    @swagger_auto_schema(responses={200: LogoutSerializer(many=True)},request_body=LogoutSerializer)
    def post(self, request,format=None):
        """
        Log User Out 
        """
       
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
           serializer.save()
           return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors)


class PasswordReset(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer
    
    @swagger_auto_schema(responses={200: PasswordResetSerializer(many=True)},request_body=PasswordResetSerializer)
    def post(self, request, format=None):
        """
        Reset User Password
        Parameters:
         email
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.data['email']

            try:
                user = get_user_model().objects.get(email=email)

                # Delete all unused password reset codes
                PasswordResetCode.objects.filter(user=user).delete()
                
                if user.is_verified and  user.is_active:
                    password_reset_code = \
                        PasswordResetCode.objects.create_password_reset_code(user)
                    password_reset_code.send_password_reset_email()
                    content = {'email': email} 
                    return Response(content)

            except get_user_model().DoesNotExist:
                pass

            # Since this is AllowAny, don't give away error.
            content = {'detail': _('Password reset not allowed.')}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class PasswordResetVerify(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'core/password_reset_form.html'
    def get(self, request, format=None):
        
        """
        Verify if user is verified 
        parameters:
          code
        
        """
        code = request.GET.get('code', '')

        try:
            password_reset_code = PasswordResetCode.objects.get(code=code)

            # Delete password reset code if older than expiry period
            delta = date.today() - password_reset_code.created_at.date()
            if delta.days > PasswordResetCode.objects.get_expiry_period():
                password_reset_code.delete()
                raise PasswordResetCode.DoesNotExist()

            content = {'success': _('Email address verified.'),'code':code}
            return Response(content)
        except PasswordResetCode.DoesNotExist:
            content = {'detail': _('Unable to verify user.')}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetVerified(APIView):
    
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetVerifiedSerializer
    @swagger_auto_schema(responses={200: PasswordResetVerifiedSerializer(many=True)},request_body=PasswordResetVerifiedSerializer)
    def post(self, request, format=None):
        """
        Confirm Reset User Password
        Parameters:
           code
           password
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            code = serializer.data['code']
            password = serializer.data['password']

            try:
                password_reset_code = PasswordResetCode.objects.get(code=code)
                password_reset_code.user.set_password(password)
                password_reset_code.user.save()

                # Delete password reset code just used
                password_reset_code.delete()

                content = {'success': _('Password reset.')}
                return Response(content, status=status.HTTP_200_OK)
            except PasswordResetCode.DoesNotExist:
                content = {'detail': _('Unable to verify user.')}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class EmailChange(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmailChangeSerializer
    @swagger_auto_schema(responses={200: EmailChangeSerializer(many=True)},request_body=EmailChangeSerializer)
    def post(self, request, format=None):
        """
        Change User Email
        
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = request.user

            # Delete all unused email change codes
            EmailChangeCode.objects.filter(user=user).delete()

            email_new = serializer.data['email']

            try:
                user_with_email = get_user_model().objects.get(email=email_new)
                if user_with_email.is_verified:
                    content = {'detail': _('Email address already taken.')}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # If the account with this email address is not verified,
                    # give this user a chance to verify and grab this email address
                    raise get_user_model().DoesNotExist

            except get_user_model().DoesNotExist:
                email_change_code = EmailChangeCode.objects.create_email_change_code(user, email_new)

                email_change_code.send_email_change_emails()

                content = {'email': email_new}
                return Response(content, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class EmailChangeVerify(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'core/email_changed_message.html'
    
    def get(self, request, format=None):
        """
        Verify Change User Email Link
        
        """
        code = request.GET.get('code', '')

        try:
            # Check if the code exists.
            email_change_code = EmailChangeCode.objects.get(code=code)

            # Check if the code has expired.
            delta = date.today() - email_change_code.created_at.date()
            if delta.days > EmailChangeCode.objects.get_expiry_period():
                email_change_code.delete()
                raise EmailChangeCode.DoesNotExist()

            # Check if the email address is being used by a verified user.
            try:
                user_with_email = get_user_model().objects.get(email=email_change_code.email)
                if user_with_email.is_verified:
                    # Delete email change code since won't be used
                    email_change_code.delete()

                    content = {'detail': _('Email address already taken.')}
                    return Response(content)
                else:
                    # If the account with this email address is not verified,
                    # delete the account (and signup code) because the email
                    # address will be used for the user who just verified.
                    user_with_email.delete()
            except get_user_model().DoesNotExist:
                pass

            # If all is well, change the email address.
            email_change_code.user.email = email_change_code.email
            email_change_code.user.save()

            # Delete email change code just used
            email_change_code.delete()

            content = {'success': _('Email address changed.')}
            return Response(content)
        except EmailChangeCode.DoesNotExist:
            content = {'detail': _('Unable to verify user.')}
            return Response(content)


class PasswordChange(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordChangeSerializer
    @swagger_auto_schema(responses={200: PasswordChangeSerializer(many=True)},request_body=PasswordChangeSerializer)
    def post(self, request, format=None):
        """
        Change Password
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = request.user

            password = serializer.data['password']
            user.set_password(password)
            user.save()

            content = {'success': _('Password changed.')}
            return Response(content, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserMe(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    @swagger_auto_schema(responses={200: UserSerializer(many=True)})
    def get(self, request, format=None):
        """
        Get Authenticated User
        
        """
        return Response(self.serializer_class(request.user).data)