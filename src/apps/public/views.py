from apps.product.models import ProductModel
from apps.public.models import AboutUsModel, ArticleModel, BannerModel
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views import View


class HomeView(View):
    def get(self, request):

        banners = BannerModel.objects.filter(is_active=True).order_by("-created_at")[:3]

        products = ProductModel.objects.filter(status="available").order_by(
            "-created_at"
        )[:4]

        articles = ArticleModel.objects.filter(is_published=True).order_by(
            "-created_at"
        )[:2]

        return render(
            request,
            "public/index.html",
            {
                "banners": banners,
                "products": products,
                "articles": articles,
            },
        )


class AboutUsView(View):
    def get(self, request):
        about = AboutUsModel.objects.order_by("-updated_at").first()
        return render(request, "public/about.html", {"about": about})


class ArticleListView(View):
    def get(self, request):
        articles = ArticleModel.objects.filter(is_published=True).order_by(
            "-created_at"
        )

        paginator = Paginator(articles, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "public/article_list.html", {"page_obj": page_obj})


class ArticleDetailView(View):
    def get(self, request, id, slug):
        article = get_object_or_404(ArticleModel, id=id, slug=slug, is_published=True)
        return render(request, "public/article_detail.html", {"article": article})
