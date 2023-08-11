from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from blog.models import Category, Post

NUM_OF_PUBLISHED = 5


def get_base_post_queryset():
    return Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )


def index(request):
    post_list = get_base_post_queryset()[:NUM_OF_PUBLISHED]
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, id):
    post = get_object_or_404(get_base_post_queryset(), pk=id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    post_list = get_base_post_queryset().filter(category=category)
    return render(
        request,
        'blog/category.html',
        {'category': category, 'post_list': post_list}
    )
