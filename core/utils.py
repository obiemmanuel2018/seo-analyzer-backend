from .serializer import CustomTokenObtainPairSerializer
from .models import SignupCode

def get_access_token(email,password):
    data ={}
    data['email'] = email
    data['password'] = password
    auth_serialize_data = CustomTokenObtainPairSerializer().validate(data)
    return auth_serialize_data



def send_verification_mail(request,user):
    # Create and associate signup code
    ipaddr = request.META.get('REMOTE_ADDR', '0.0.0.0')
    signup_code = SignupCode.objects.create_signup_code(user, ipaddr)
    signup_code.send_signup_email()
    return True