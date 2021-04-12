from django.shortcuts import render,redirect,get_object_or_404
from .forms import UpdateUserForm,ProfileForm,NeighbourHoodForm,BusinessForm,PostForm
from .models import Neighborhood,Profile,Post,Business
from django.http import HttpResponse,HttpResponseRedirect
from .serializer import ProfileSerializer,UserSerializer
from rest_framework.views import APIView


# Create your views here.
def index(request):
    return render(request,'index.html')

def profile(request, username):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = ProfileForm(instance=request.user.profile)
    params = {
        'user_form': user_form,
        'prof_form': prof_form,
    }
    return render(request, 'profile.html', params)

def hoods(request):
    hoods = Neighborhood.objects.all()
    form = NeighbourHoodForm(request.POST, request.FILES)
    print(form.errors)
    if form.is_valid():
        post = form.save(commit=False)
        post.admin = request.user.profile
        post.save()
        return redirect('hoods')
    else:
        form = NeighbourHoodForm(request.POST, request.FILES)

    return render(request,'all_hoods.html',{"all_hoods":hoods,"form":form})

def single_hood(request, hood_id):
    hood = Neighborhood.objects.get(id=hood_id)
    business = Business.objects.filter(neighborhood=hood)
    posts = Post.objects.filter(hood=hood)
    posts = posts[::-1]
    if request.method == 'POST':
        form = BusinessForm(request.POST,request.FILES)
        if form.is_valid():
            b_form = form.save(commit=False)
            b_form.neighborhood = hood
            b_form.user = request.user.profile
            b_form.save()
            return redirect('single_hood', hood.id)
    else:
        form = BusinessForm()
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.hood = hood
            post.user = request.user.profile
            post.save()
            return redirect('single_hood', hood.id)
    else:
        post_form = PostForm()
    params = {
        'hood': hood,
        'business': business,
        'post_form': post_form,
        'posts': posts,
        'form': form,
    }
    return render(request, 'single_hood.html', params)

def join(request, id):
    hood = get_object_or_404(Neighborhood, id=id)
    request.user.profile.neighborhood = hood
    request.user.profile.save()
    return redirect('single_hood', hood.id)


def leave(request, id):
    hood = get_object_or_404(Neighborhood, id=id)
    request.user.profile.neighborhood = None
    request.user.profile.save()
    return redirect('hoods')


def search_profile(request):
    if 'search_user' in request.GET and request.GET['search_user']:
        name = request.GET.get("search_user")
        results = Business.search_business(name)
        print(results)
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'results.html', params)
    else:
        message = "You did not make a selection"
    return render(request, 'results.html', {'message': message})

# class ProfileList(APIView):
#     def get(self, request, format=None):
#         all_profile = Profile.objects.all()
#         serializers = ProfileSerializer(all_profile, many=True)
#         return Response(serializers.data)

# class UserList(APIView):
#     def get(self, request, format=None):
#         all_user = User.objects.all()
#         serializers = UserSerializer(all_user, many=True)
#         return Response(serializers.data)