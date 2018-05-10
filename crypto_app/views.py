import random, string
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views import generic

from crypto_app.polyalphabetic import encrypt, decrypt
from .forms import BaseAuthenticationForm
from .models import Alphabed, DecodeHelper
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
        Alphabed.objects.all().delete()
        a = Alphabed(title=request.POST.get("details"))
        a.save()
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

    def generate_key(self, size=120, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def post(self, request, *args, **kwargs):
        _ctx = self.get_context_data(**kwargs)
        letter = Alphabed.objects.last().title
        if u'encode_form' in request.POST:
            _encode = request.POST.get("encode")
            _token = request.POST.get("token")
            _ctx["encode"] = _encode
            _ctx["encode_token"] = _token
            _hidden_token = self.generate_key()
            if _encode == "":
                _ctx["error"] = 'Şifrələnəcək sözü daxil edin!'
                return render(request, self.template_name, context=_ctx)
            if _token == "":
                _ctx["error"] = 'Açar sözü daxil edin!'
                return render(request, self.template_name, context=_ctx)
            error_letter = ""
            for char in _encode:
                if not char in letter:
                    error_letter += "True"
            if error_letter == "True":
                _ctx["error"] = "Əlifbadan kənara çıxmayın"
                return render(request, self.template_name, context=_ctx)
            encoded = encrypt(_encode.replace(" ","`"), _hidden_token)
            d = DecodeHelper(
                encode=encoded,
                token=_token,
                hidden_token=_hidden_token
            )
            d.save()
            if encoded and isinstance(encoded, str):
                _ctx["encoded"] = encoded
            elif encoded and not isinstance(encoded, str) and encoded["error"]:
                if encoded["error"] == 'no-text':
                    _ctx["error"] = 'Şifrələnəcək sözü daxil edin!'
                elif encoded["error"] == 'no-token':
                    _ctx["error"] = 'Açar sözü daxil edin!'
            else:
                _ctx["error"] = "Əlifbadan kənara çıxmayın"
            return render(request, self.template_name, context=_ctx)
        elif u'decode_form' in request.POST:
            _decode = request.POST.get("decode")
            _token = request.POST.get("token")
            _hidden_token = ""
            try:
                d = DecodeHelper.objects.filter(encode=_decode,token=_token)
                if d.last():
                    _hidden_token += d.last().hidden_token
                else:
                    _hidden_token += self.generate_key()
            except:
                _hidden_token += self.generate_key()
            decoded = decrypt(_decode, _hidden_token)
            decoded = decoded.replace("`"," ")
            if decoded and isinstance(decoded, str):
                _ctx["decoded"] = decoded
            elif decoded and not isinstance(decoded, str) and decoded["error"]:
                if decoded["error"] == 'no-text':
                    _ctx["error"] = 'Deşifrələnəcək sözü daxil edin!'
                elif decoded["error"] == 'no-token':
                    _ctx["error"] = 'Açar sözü daxil edin!'
            else:
                _ctx["error"] = 'Əlifbadan kənara çıxmayın'
            _ctx["encoded"] = _decode
            _ctx["decode"] = _decode
            # _ctx["encode"] = decoded
            _ctx["decode_token"] = _token
            return render(request, self.template_name, context=_ctx)
        return render(request, self.template_name, self.get_context_data(*args, **kwargs))
