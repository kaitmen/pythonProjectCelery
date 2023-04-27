from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.core.mail import EmailMultiAlternatives
from django.views import View

from .filters import PostFilter
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from .forms import PostForm, ChooseCategoryForm
from .models import Post, Author, Category
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers
from datetime import datetime, timedelta, time

# @receiver(post_save, sender=Post)
# def notify_managers_post(sender, instance, created, **kwargs):
#     if created:
#         subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'
#     else:
#         subject = f'post changed for {instance.client_name} {instance.date.strftime("%d %m %Y")}'
#
#     mail_managers(
#         subject=subject,
#         message=instance.message,
#     )


def home(request):
    return redirect('authors:posts')

class PostsList(ListView):

    model = Post

    ordering = '-created_at'

    template_name = 'posts.html'

    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        self.filterset = PostFilter(self.request.GET, queryset)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):

    model = Post

    template_name = 'post.html'

    context_object_name = 'post'


class PostsSearch(ListView):

    model = Post

    ordering = '-created_at'

    template_name = 'search.html'

    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        self.filterset = PostFilter(self.request.GET, queryset)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['filterset'] = self.filterset
        return context




class NewsCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['categories', 'title', 'text']
    success_url = reverse_lazy('authors:posts')
    # permission_required = ('post.add_post',)
    def form_valid(self, form):
        author = Author.objects.filter(user=self.request.user.id).first()
        if not author:
            author = Author.objects.first()
            messages.error(self.request, "You not author, we get first.")
        else:
            messages.success(self.request, "The task was created successfully.")
            today = datetime.now().date()
            tomorrow = today + timedelta(1)
            today_start = datetime.combine(today, time())
            today_end = datetime.combine(tomorrow, time())

            count = author.posts.filter(created_at__lte=today_end, created_at__gte=today_start).count()
            if count == 3:
               raise ValidationError("You was create 3 post")

        form.instance.author = author
        form.instance.type = 'N'

        return super(NewsCreate, self).form_valid(form)


class ArticleCreate(PermissionRequiredMixin, LoginRequiredMixin,CreateView):
    model = Post
    fields = ['categories', 'title', 'text']
    success_url = reverse_lazy('authors:posts')
    permission_required = ('authors.ArticleCreate',)
    def form_valid(self, form):
        author = Author.objects.filter(user=self.request.user.id).first()
        if not author:
            author = Author.objects.first()
            messages.error(self.request, "You not author, we get first.")
        else:
            messages.success(self.request, "The task was created successfully.")
            today = datetime.now().date()
            tomorrow = today + timedelta(1)
            today_start = datetime.combine(today, time())
            today_end = datetime.combine(tomorrow, time())

            count = author.posts.filter(created_at__lte=today_end, created_at__gte=today_start).count()
            if count == 3:
                raise ValidationError("You was create 3 post")
        form.instance.author = author
        form.instance.type = 'A'

        return super(ArticleCreate, self).form_valid(form)

class PostFormView(PermissionRequiredMixin, LoginRequiredMixin,UpdateView):
    model = Post
    permission_required = ('authors.PostFormView',)
    fields = [
        "title",
        "text"
    ]

    success_url = reverse_lazy('authors:posts')


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post

    success_url = reverse_lazy('authors:posts')

    template_name = "authors/confirm_delete.html"


class Subscribe(View):
    def get(self, request, *args, **kwargs):
        form = ChooseCategoryForm()
        return render(request, 'make_Subscribe.html', {'form':form})
    def post(self, request, *args, **kwargs):
        form = ChooseCategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            # for c in categories:
            #     c.add_subscriber(self.request.user.emai)
            print(name)
            c = Category.objects.get(pk = name)
            c.add_subscriber(self.request.user.email)
        return redirect('authors:posts')