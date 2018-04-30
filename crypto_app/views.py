from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views import generic
from .forms import BaseAuthenticationForm
from .models import Alphabed
from .tasks import create_alphabet, encoder_task, decoder_task


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
        return super(BaseIndexView, self).form_invalid(form)

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
        context = {"list": Alphabed.objects.last()}
        return context


class UserView(generic.TemplateView):
    template_name = "User/index.html"

    def get_context_data(self, **kwargs):
        _a = Alphabed.objects.last()
        if _a:
            ctx = {"alphabet": Alphabed.objects.last()}
        else:
            ctx = dict()
        return ctx

    def post(self, request, *args, **kwargs):
        encoded, decoded = "", ""
        _ctx = self.get_context_data(*args, **kwargs)
        if u'encode_form' in request.POST:
            _encode = request.POST.get("encode").upper()
            _token = request.POST.get("token").upper()
            encoded = encoder_task(text=_encode, token=_token)
            if encoded and isinstance(encoded, str):
                _ctx["encoded"] = encoded
                _ctx["encode"] = _encode
                _ctx["token"] = _token
            elif encoded and not isinstance(encoded, str) and encoded["error"]:
                if encoded["error"] == 'no-text':
                    _ctx["error"] = 'Şifrələnəcək sözü daxil edin!'
                elif encoded["error"] == 'no-token':
                    _ctx["error"] = 'Açar sözü daxil edin!'
            else:
                _ctx["error"] = "Əlifbadan kənara çıxmayın"
            return render(request, self.template_name, context=_ctx)
        elif u'decode_form' in request.POST:
            _decode = request.POST.get("decode").upper()
            _token = request.POST.get("token").upper()
            decoded = decoder_task(text=_decode, token=_token)
            if decoded and isinstance(decoded, str):
                _ctx["decoded"] = decoded
                _ctx["encoded"] = _decode
                _ctx["decode"] = _decode
                _ctx["encode"] = decoded
                _ctx["token"] = _token
            elif decoded and not isinstance(decoded, str) and decoded["error"]:
                if decoded["error"] == 'no-text':
                    _ctx["error"] = 'Deşifrələnəcək sözü daxil edin!'
                elif decoded["error"] == 'no-token':

                    _ctx["error"] = 'Açar sözü daxil edin!'
            else:
                _ctx["error"] = 'Əlifbadan kənara çıxmayın'
            return render(request, self.template_name, context=_ctx)
        return render(request, self.template_name, self.get_context_data(*args, **kwargs))
