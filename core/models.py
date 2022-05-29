from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin )
from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from django.utils.translation import gettext_lazy as _
import binascii
import os
from django.conf import settings
# Create your models here.
# Make part of the model eventually, so it can be edited
EXPIRY_PERIOD = 3    # days


def _generate_code():
    return binascii.hexlify(os.urandom(20)).decode('utf-8')


class UserManager(BaseUserManager):
     
      def create_user(self,email,name=None,password=None,**extra_fields):
          """Create and Save User"""
          if not email:
              raise ValueError('User email is required')
          user = self.model(
              name=name,
              email=self.normalize_email(email)
          )
          
          user.set_password(password)
          user.save()
          return user
      def create_superuser(self,email,password):
          """Create superuser"""
          user = self.create_user(
              email=email,
              password=password
          )
          
          user.is_staff = True
          user.is_superuser = True
          user.is_verified = True
          user.save()
          return user
          
      
      
      


class User(AbstractBaseUser,PermissionsMixin):
      name = models.CharField(max_length=200,null=True,blank=True)
      email = models.EmailField(max_length=200,unique=True)
      is_staff = models.BooleanField(default=False)
      is_active = models.BooleanField(default=True)
      is_superuser = models.BooleanField(default=False)
      is_verified = models.BooleanField(default=False)
      
      USERNAME_FIELD = 'email'
      objects = UserManager()      
      
      def __str__(self):
          return str(self.email)

   

class SignupCodeManager(models.Manager):
    def create_signup_code(self, user, ipaddr):
        code = _generate_code()
        signup_code = self.create(user=user, code=code, ipaddr=ipaddr)

        return signup_code

    def set_user_is_verified(self, code):
        try:
            signup_code = SignupCode.objects.get(code=code)
            signup_code.user.is_verified = True
            signup_code.user.save()
            return True
        except SignupCode.DoesNotExist:
            pass

        return False


class PasswordResetCodeManager(models.Manager):
    def create_password_reset_code(self, user):
        code = _generate_code()
        password_reset_code = self.create(user=user, code=code)

        return password_reset_code

    def get_expiry_period(self):
        return EXPIRY_PERIOD


class EmailChangeCodeManager(models.Manager):
    def create_email_change_code(self, user, email):
        code = _generate_code()
        email_change_code = self.create(user=user, code=code, email=email)

        return email_change_code

    def get_expiry_period(self):
        return EXPIRY_PERIOD


def send_multi_format_email(template_prefix, template_ctxt, target_email):
  
    subject_file = 'core/%s_subject.txt' % template_prefix
    txt_file = 'core/%s.txt' % template_prefix
    html_file = 'core/%s.html' % template_prefix
  
  
    subject = render_to_string(subject_file).strip()
    from_email = settings.EMAIL_HOST_USER
    to = target_email
    # bcc_email = settings.EMAIL_HOST_USER
    text_content = render_to_string(txt_file, template_ctxt)
    html_content = render_to_string(html_file, template_ctxt)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


class AbstractBaseCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(_('code'), max_length=40, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    site_url = settings.SITE_URL
    class Meta:
        abstract = True

    def send_email(self, prefix):
        ctxt = {
            'email': self.user.email,
            'name':self.user.name,
            'code': self.code,
            'site_url':self.site_url
        }
        send_multi_format_email(prefix, ctxt, target_email=self.user.email)

    def __str__(self):
        return self.code


class SignupCode(AbstractBaseCode):
    ipaddr = models.GenericIPAddressField(_('ip address'))

    objects = SignupCodeManager()

    def send_signup_email(self):
        prefix = 'signup_email'
        self.send_email(prefix)


class PasswordResetCode(AbstractBaseCode):
    objects = PasswordResetCodeManager()

    def send_password_reset_email(self):
        prefix = 'password_reset_email'
        self.send_email(prefix)


class EmailChangeCode(AbstractBaseCode):
    email = models.EmailField(_('email address'), max_length=255)

    objects = EmailChangeCodeManager()

    def send_email_change_emails(self):
        prefix = 'email_change_notify_previous_email'
        self.send_email(prefix)

        prefix = 'email_change_confirm_new_email'
        ctxt = {
            'email': self.email,
            'code': self.code
        }

        send_multi_format_email(prefix, ctxt, target_email=self.email)