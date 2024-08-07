from django.shortcuts import render,redirect
from django.views import View
from .forms import RegisterForm

# Create your views here.
class CustomerRegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        form = RegisterForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role='customer'
            user.save()
            return redirect('accounts:add_address', id=user.id)
        return render(request, 'register.html', {'form': form})