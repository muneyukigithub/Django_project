from email import message
from django import forms
from django.core.mail import EmailMessage
import logging

logger = logging.getLogger(__name__)

class InquiryForm(forms.Form):
    name = forms.CharField(label="お名前",max_length=30)
    email = forms.EmailField(label="Email")
    title = forms.CharField(label='タイトル',max_length=30)
    message = forms.CharField(label='メッセージ',widget=forms.Textarea)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def send_email(self):
        name=self.cleaned_data['name']
        email=self.cleaned_data['email']
        title=self.cleaned_data['title']
        message=self.cleaned_data['message']

        from_email = "admin@example.com"

        # to_list = ['satou71150@icloud.com']
        to_list = []
        to_list.append(email)
        cc_list = ['']

        message = EmailMessage(subject=title,body=message,from_email=from_email,to=to_list,cc=cc_list)
        message.send()

        logger.info("send_email_OK")