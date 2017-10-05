from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, logout
from django.http import HttpResponseRedirect, HttpResponse

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories' : category_list,
                    'pages': page_list}
    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False
    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            # ...прибавляем единицу к предыдущему значению cookie...
            visits = visits + 1
            # ...и обновляем cookie last visit cookie.
            reset_last_visit_time = True
    else:
        # Cookie last_visit не существует, поэтому создаём его для текущей даты/времени.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits

    response = render(request, 'rango/index.html', context_dict)

    return response


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug= category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = [pages]
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    form = CategoryForm
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit = True)
            return index(request)
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug = category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit = False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form':form, 'category':category}
    return render(request, 'rango/add_page.html', context_dict)


def about(request):
    return render(request, 'rango/about.html', {})


# def register(request):
#     reqistered = False
#     if request.method == 'POST':
#         user_form = UserForm(data = request.POST)
#         profile_form = UserProfileForm(data = request.POST)
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#             profile = profile_form.save(commit = False)
#             profile.user = user
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#             profile.save()
#             registered = True
#         else:
#             print(user_form.errors, profile_form.errors)
#     else:
#         user_form = UserForm
#         profile_form = UserProfileForm
#
#     return render(request, 'rango/register.html', {'user_form': user_form,
#                                                    'profile_form': profile_form},
#                                                   {'registered': reqistered},)


# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password = password)
#         if user:
#             if user.is_active():
#                 login(request, user)
#                 return HttpResponseRedirect('/rango/')
#             else:
#                 return HttpResponse('Your rango account is disable')
#         else:
#             print('Invalid login details: {}, {}'.format(username, password))
#             return HttpResponse('Invalid login details supplied')
#     else:
#         return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})


# @login_required
# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect('/rango/')