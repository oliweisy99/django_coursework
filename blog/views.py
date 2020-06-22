from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.views.generic.edit import ModelFormMixin
from .forms import CommentForm
from .models import Blog, Comment
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import CommentForm

class BlogListView(ListView):
    model = Blog


class BlogDetailView(ModelFormMixin, DetailView):
    model = Blog
    form_class = CommentForm


    def form_valid(self, form):
        blog = get_object_or_404(Blog, pk=self.kwargs.get('pk'))
        comment = form.save(commit=False)
        comment.blog = blog
        comment.save()
        super().form_valid(form)
        return redirect('blog:post', pk=blog.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            blog = get_object_or_404(Blog, pk=self.kwargs.get('pk'))
            comment = form.save(commit=False)
            comment.blog = blog
            comment.save()
            messages.success(self.request, "Comment is waiting approval")
            return redirect('blog:post', pk=blog.pk)
        else:
            messages.warning(self.request, ("Comment Error"))


        return super().post(request, *args, **kwargs)


class BlogBioView(TemplateView):
    template_name = 'blog/blog_bio.html'

class TempUser(TemplateView):
    template_name = 'blog/temp_user.html'

class BlogCreateView(PermissionRequiredMixin, CreateView):
    model = Blog
    fields = ('title', 'description', 'content', 'blog_pic')
    permission_required = 'blog.can_make_changes'
    permission_denied_message = 'Must be a superuser to create a post'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class BlogPostUpdateView(PermissionRequiredMixin, UpdateView):
    model = Blog
    fields = ('title', 'description', 'content', 'blog_pic')
    permission_required = 'blog.can_make_changes'
    permission_denied_message = 'Must be a superuser to update a post'


class BlogDeleteView(PermissionRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:all')
    permission_required = 'blog.can_make_changes'
    permission_denied_message = 'Must be a superuser to Delete a post'

class CreateComment(SuccessMessageMixin, CreateView):
    model = Comment
    fields = ('author', 'text')
    success_message = "Your comment is waiting approval"

    def form_valid(self, form):
        blog = get_object_or_404(Blog, pk=self.kwargs.get('pk'))
        comment = form.save(commit=False)
        comment.blog = blog
        comment.save()
        super().form_valid(form)
        return redirect('blog:post', pk=blog.pk)

class CommentUpdate(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Comment
    fields = ('author', 'text')
    success_message = "The comment has been updated"
    permission_required = 'comment.can_make_decision'
    permission_denied_message = 'Must be a superuser to edit a comment'

    def form_valid(self, form):
        comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        blogcomment = form.save(commit=False)
        blogcomment.blog = comment.blog
        comment.save()
        super().form_valid(form)
        return redirect('blog:post', pk=comment.blog.pk)

class CommentApprove(PermissionRequiredMixin ,RedirectView):
    permission_required = 'comment.can_make_decision'
    permission_denied_message = 'Must be a superuser to approve a comment'

    def get_redirect_url(self, *args, **kwargs):
        return reverse("blog:post",kwargs={"pk":self.kwargs.get('pk')})

    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        try:
            comment.approve()

        except IntegrityError:
            messages.warning(self.request, ("Comment Error"))

        else:
            messages.success(self.request, "Comment approved")
        super().get(request, *args, **kwargs)
        return redirect('blog:post', pk=comment.blog.pk)

class CommentRemove(PermissionRequiredMixin ,RedirectView):
    permission_required = 'comment.can_make_decision'
    permission_denied_message = 'Must be a superuser to remove a comment'

    def get_redirect_url(self, *args, **kwargs):
        return reverse("blog:post",kwargs={"pk":self.kwargs.get('pk')})

    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        try:
            comment.delete()

        except IntegrityError:
            messages.warning(self.request, ("Comment Error"))

        else:
            messages.success(self.request, "Comment deleted")
        super().get(request, *args, **kwargs)
        return redirect('blog:post', pk=comment.blog.pk)



#
# def add_comment_to_post(request,pk):
#
#     blog = get_object_or_404(Blog,pk=pk)
#
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.blog = blog
#             comment.save()
#             return redirect('blog:post', pk=blog.pk)
#     else:
#         form = CommentForm()
#
#     return render(request, 'blog/comment_form.html', {'form':form})
#
# @login_required
# def comment_approve(request,pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     comment.approve()
#     return redirect('blog:post', pk=comment.blog.pk)
#
# @login_required
# def comment_remove(request,pk):
#     comment = get_object_or_404(Comment,pk=pk)
#     blog_pk = comment.blog.pk
#     comment.delete()
#     return redirect('blog:post', pk=blog_pk)
