from django.shortcuts import get_object_or_404, render

from django.utils import timezone

from blog.models import Category, Post

POSTS_PER_PAGE = 5


def get_base_post_queryset():
    return Post.objects.select_related('category').filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )


def index(request):
    post_list = get_base_post_queryset()[:POSTS_PER_PAGE]
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, id):
    post = get_object_or_404(get_base_post_queryset(), pk=id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(Category.objects.values('title', 'description').filter(
        slug=category_slug, is_published=True
    ))

    post_list = get_base_post_queryset().filter(category__slug=category_slug)

    return render(request, 'blog/category.html', {'category': category, 'post_list': post_list})
