from django.http.response import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.db.models import Q
from django.views.generic import ListView, DetailView, UpdateView

from poem.forms import CommentForm, PoemForm

from .models import Poem


class LoginPermissionMixin(LoginRequiredMixin):
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class PoemsView(LoginPermissionMixin, ListView):
    model = Poem
    paginate_by = 1
    
    def get_queryset(self):
        search = self.request.GET.get('search', '')
        search_filter = []
        if search:
            search_filter.append(
                Q(name__icontains=search) |
                Q(author__first_name__icontains=search) |
                Q(author__last_name__icontains=search)
            )

        ordering = self.get_ordering()
        return Poem.objects.filter(*search_filter).order_by(*ordering)

    def get_ordering(self):
        sort_by_author = self.request.GET.get('sort_by_author', 'asc')
        sort_by_name = self.request.GET.get('sort_by_name', 'asc')
        sorting = (
            'author__last_name' if sort_by_author == 'asc' else '-author__last_name',
            'name' if sort_by_name == 'asc' else '-name'
        )
        return sorting

    def get_context_data(self, **kwargs):
        context = super().get_context_data(*kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['sort_by_author'] = self.request.GET.get('sort_by_author', '')
        context['sort_by_name'] = self.request.GET.get('sort_by_name', '')
        return context


class PoemDetailView(LoginPermissionMixin, DetailView):
    model = Poem

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['comment_form'] = CommentForm()
        return context


class PoemUpdateView(PermissionRequiredMixin, LoginPermissionMixin, UpdateView):
    model = Poem

    permission_required = 'poem.change_poem'

    fields = ['name', 'text', 'author']
    success_url = '/poems/'
    template_name = 'poem/poem_update.html'


@login_required(login_url='/accounts/login')
def like_poem(request, poem_id):
    poem = Poem.objects.filter(id=poem_id).first()
    if poem:
        try:
            poem.like_set.create(user=request.user)
        except IntegrityError:
            return HttpResponse('This poem is already liked')
        return HttpResponse('Liked successfully')
    return render(request, '404.html')


@login_required(login_url='/accounts/login')
def dislike_poem(request, poem_id):
    poem = Poem.objects.filter(id=poem_id).first()
    if poem:
        try:
            poem.dislike_set.create(user=request.user)
        except IntegrityError:
            return HttpResponse('This poem is already disliked')
        return HttpResponse('Disliked successfully')
    return render(request, '404.html')


@login_required(login_url='/accounts/login')
def comment_poem(request, poem_id):
    poem = Poem.objects.filter(id=poem_id).first()
    if poem:
        form = CommentForm(data=request.POST)
        if form.is_valid():
            poem.comment_set.create(user=request.user, text=form.cleaned_data['comment'])
            return redirect('retrieve_poem', poem_id=poem_id)
    return render(request, '404.html')
