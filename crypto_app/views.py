from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import generic
from .tasks import create_alphabet
from .forms import BaseAuthenticationForm
from .models import Alphabed


# Create your views here.


class BaseIndexView(generic.FormView):
    template_name = "Home/index.html"
    form_class = BaseAuthenticationForm
    success_url = "/admin-view"

    # def post(self, request, *args, **kwargs):
    #     print("post")
    #     return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.cleaned_data
        login(self.request, user)
        if user.is_staff:
            self.success_url = 'admin-view'
        else:
            self.success_url = 'user-view'
        return super(BaseIndexView, self).form_valid(form)

    def form_invalid(self, form):
        return HttpResponse(form.errors)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('/admin-view')
            else:
                return redirect('/user-view')
        else:
            if request.method == 'GET':
                return self.get(request, *args, **kwargs)
            else:
                return self.post(request, *args, **kwargs)


class AdminView(generic.TemplateView):
    template_name = "Admin/index.html"

    def post(self, request, *args, **kwargs):
        create_alphabet(request.POST.get("details").upper())
        return render(request, self.template_name, self.get_context_data(*args, **kwargs))

    def get_context_data(self, *args, **kwargs):
        context = {}
        context["list"] = Alphabed.objects.last()
        return context


class UserView(generic.TemplateView):
    template_name = "User/index.html"
