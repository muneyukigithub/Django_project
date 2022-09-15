from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import InquiryForm
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

# Create your views here.

from django.views import generic
from .forms import InquiryForm

class IndexView(generic.TemplateView):
    template_name = "index.html"

class InquiryView(generic.FormView):
    template_name = "form.html"
    form_class = InquiryForm
    success_url = reverse_lazy('diary:index')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request,'メッセージを送信しました。')
        logger.info("form_valid_check_OK")
        return super().form_valid(form)