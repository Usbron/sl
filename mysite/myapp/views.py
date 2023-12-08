from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Product

def index(request):
    items = Product.objects.all()
    context = {
        'items':items
    }
    return render(request, "myapp/index.html", context)

def indexItem(request, my_id):
    item = Product.objects.get(id=my_id)
    context = {
        'item': item
    }
    return render(request, "myapp/detail.html", context)
def add_item(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.FILES["upload"]
        item = Product(
            name=name, price=price, description=description, image=image
        )
        item.save()
    return render(request, "myapp/additem.html")

def update_item(request, my_id):
    item = Product.objects.get(id=my_id)
    if request.method == "POST":
        item.name = request.POST.get("name")
        item.price = request.POST.get("price")
        item.description = request.POST.get("description")
        item.image = request.FILES.get("upload", item.image)
        item.save()
        return redirect("/myapp/")
    context = {"item": item}
    return render(request, "myapp/updateitem.html", context)

def delete_item(request, my_id):
    item = Product.objects.get(id=my_id)
    if request.method == "POST":
        item.delete()
        return redirect("/myapp/")
    context = {"item": item}
    return render(request, "myapp/deleteitem.html", context)

def register(request):
    if request.method == 'POST': #POST - это один из HTTP-методов, используемых для отправки данных на сервер
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None: #проверяет, успешно ли прошла аутентификация пользователя.
                login(request, user) #выполняет вход пользователя в систему
                return render(request, 'myapp/profile.html')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})

def profile_view(request):
    return render(request, 'myapp/profile.html')
