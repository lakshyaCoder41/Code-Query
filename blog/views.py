from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post,Comment
import operator
from django.db.models import Q
from functools import reduce

#We are going to function home, this function will handle the traffic
def home(request):
    context={
        'posts':Post.objects.all()
    }
    return render(request,'blog/home.html',context)

class SearchListView(ListView):
    model=Post
    paginate_by=5
    context_object_name='posts'
    template_name='blog/search_post.html'
    def get_queryset(self):
        result=super(SearchListView,self).get_queryset()
        search=self.request.GET.get('q')
        if search:
            search_list=search.split()
            result=result.filter(
                reduce(operator.and_,
                        (Q(title__icontains=q) for q in search_list))|
                        reduce(operator.and_,
                                (Q(content__icontains=q) for q in search_list)))

        return result

class PostListView(ListView):
    model=Post

    template_name='blog/home.html' #<app>/<model>_<viewtype>.html
    context_object_name='posts'
    ordering=['-date_posted'] # ordering is an attribute of ListView if set date_posted as -date_posted it will latest post
    paginate_by=5


class UserPostListView(ListView):
    model=Post

    template_name='blog/user_posts.html' #<app>/<model>_<viewtype>.html
    context_object_name='posts'
    paginate_by=5

    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model=Post

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['comments']=Comment.objects.filter(post=self.object)
        context['users']=User.objects.filter(username=self.request.user)
        return context
    #def get_queryset(self):
    #    user=get_object_or_404(Comment,user=self.kwargs.get('user'))
    #    return Comment.objects.filter(author=user).order_by('-date_posted')
    #return render(request,post_detail.html,{'comments':Comment})

class CommentCreateView(LoginRequiredMixin,CreateView):
    model=Comment
    fields=['image','content']
#    template_name='blog/comment_form.html'


    def form_valid(self,form):
        post=get_object_or_404(Post,id=self.kwargs['pk'])
        form.instance.author=self.request.user
        form.instance.post=post
        return super().form_valid(form)



class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title','content','image']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form) # overriding the parent class method form_valid for checking whether current user is valid to create post

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=Post
    fields=['title','content','image']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)


    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False
        #here checkin if any user trying to update annother users post


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model=Post
    success_url='/' # success_url is also an object that is overrided  here to home page
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False
        #here checkin if any user trying to delete another users post

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=Comment
    fields=['image','content']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)


    def test_func(self):
        comment=self.get_object()
        if self.request.user==comment.author:
            return True
        return False
        #here checkin if any user trying to update annother users post

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model=Comment
    success_url='/'
    template_name='blog/comment_confirm_delete.html'

    def test_func(self):
        comment=self.get_object()
        if self.request.user==comment.author:
            return True
        return False

    def get_success_url(self):
        post=self.object.post
        return reverse_lazy('post-detail',kwargs={'pk':post.pk})



def about(request):
    return render(request,'blog/about.html',{'title':'About'})
# urls.py file is created in which each views or functions are mapped.
