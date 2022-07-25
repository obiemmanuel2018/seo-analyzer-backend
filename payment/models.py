from django.db import models
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings
# Create your models here.
import datetime

class Subscription(models.Model):
    # account type
      FREE = 'free'
      PAID  = 'paid'
    # subscription type
      MONTH = 'month'
      YEAR = 'year'
      FREE = 'free'
    #   payment methods
      EMPTY = "empty"
      MTN_MOMO = 'mtn momo'
      ORANGE_MOMO = "orange momo"
      
     
      
      subscription_options =(
          (FREE,'free'),
          (MONTH,'month'),
          (YEAR,'year')
      )
      
      account_options = (
          (FREE,'free'),
          (PAID,'paid')
      )
      
      payment_options = (
          (EMPTY,EMPTY),
          (ORANGE_MOMO,ORANGE_MOMO),
          (MTN_MOMO, MTN_MOMO)
      )
      
      id=models.CharField(max_length=200,primary_key=True)
      user = models.OneToOneField(get_user_model(),on_delete=models.CASCADE)
      account_type = models.CharField(max_length=100,choices=account_options,default=FREE)
      subscription_type = models.CharField(max_length=100,choices=subscription_options,default=FREE)
      payment_method = models.CharField(max_length=100,choices=payment_options,default=EMPTY)
      valid_to = models.DateField(null=True,blank=True)

      
     
      def is_valid(self,current_date=datetime.date.today()):
          try:
             if not self.valid_to:
                return False
             return current_date < self.valid_to
          except:
              return False
      

      def send_email(self, prefix):
        ctxt = {
            'email': self.user.email,
            'name':self.user.name,
        }
        send_multi_format_email(prefix, ctxt, target_email=self.user.email)
             
     
      def subscription_created_mail(self):
          prefix = 'subscription_success'
          self.send_email(prefix)
      def subscription_canceled_mail(self):
          prefix = 'subscription_canceled'
          self.send_email(prefix)
      def subscription_expiration_mail(self):
          prefix = 'subscription_expiration'
          self.send_email(prefix)
      def subscription_updated_mail(self):
          prefix = 'subscription_updated'
          self.send_email(prefix)

      def subscription_expired_mail(self):
          prefix = 'subscription_expired'
          self.send_email(prefix)
     
      
      def __str__(self) -> str:
          return "subscription for {}.Valid upto {}".format(self.user.name,self.valid_to)
      
      
def send_multi_format_email(template_prefix, template_ctxt, target_email):
  
    subject_file = 'payment/%s_subject.txt' % template_prefix
    txt_file = 'payment/%s.txt' % template_prefix
    html_file = 'payment/%s.html' % template_prefix
  
  
    subject = render_to_string(subject_file).strip()
    from_email = settings.EMAIL_HOST_USER
    to = target_email
    # bcc_email = settings.EMAIL_HOST_USER
    text_content = render_to_string(txt_file, template_ctxt)
    html_content = render_to_string(html_file, template_ctxt)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


       