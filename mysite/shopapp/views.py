from timeit import default_timer

from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.gis.feeds import Feed
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [('PC', 2000),
                    ('iPhone', 1000),
                    ('Mouse', 200), ]
        context = {
            "time_running": default_timer,
            "products": products,
        }
        return render(request, 'shopapp/shopapp-index.html', context=context)


class ProductDetailsView(DetailView):
    model = Product


class ProductListView(ListView):
    queryset = (
        Product.objects
        .filter(archived=False)
    )
    template_name = 'shopapp/products-list.html'


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'change_product'
    model = Product
    fields = 'name', 'description', 'price', 'discount'
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user.profile
        response = super().form_valid(form)

        return response


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    fields = 'name', 'price', 'description', 'discount'
    template_name = 'shopapp/product_update_form.html'
    success_url = reverse_lazy('shopapp:products_list')

    def test_func(self):
        product = self.get_object()

        if self.request.user.is_superuser:
            return True
        elif self.request.user.has_perm("shopapp.change_product") and hasattr(
                self.request.user, "profile"
        ):
            return product.created_by == self.request.user.profile

        return False


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class ProductsViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend,)
    filterset_fields = (
        'name',
        'description',
        'discount',
        'price',
        'archived',
        'created_by'
    )
    search_fields = ('name', 'description', 'price')
    ordering_fields = ('name', 'price', 'discount')


class LatestProductsFeed(Feed):
    title = "Shop products (latest)"
    description = "Updates in changes and addition shop products"
    link = reverse_lazy("shopapp:products_list")

    def items(self):
        return Product.objects.filter(archived=False).all()[:5]

    def item_title(self, item: Product) -> str:
        return item.name

    def item_description(self, item: Product) -> str:
        return item.description[:100]


class OrdersListView(ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )
    template_name = 'shopapp/orders-list.html'


class OrderDetailsView(DetailView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrderCreateView(CreateView):
    model = Order
    fields = 'delivery_address', 'promocode', 'products', 'user'
    success_url = reverse_lazy('shopapp:orders_list')


class OrderUpdateView(UpdateView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )
    fields = 'delivery_address', 'promocode', 'products'
    success_url = reverse_lazy('shopapp:orders_list')
    template_name_suffix = '_update_form'


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:orders_list')


class OrdersViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend,)
    filterset_fields = (
        'delivery_address',
        'promocode',
        'created_at',
        'user',
        'products',
    )
    search_fields = ('delivery_address', 'promocode', 'products')
    ordering_fields = ('created_at',)


class UserOrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'shopapp/user_orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        self.target_user = get_object_or_404(User, pk=user_id)

        return Order.objects.filter(user=self.target_user).prefetch_related("products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_user'] = self.target_user
        return context


class UserOrdersExportView(LoginRequiredMixin, View):

    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        user_id = self.kwargs.get('user_id')
        cache_key_value = f"user_{user_id}_orders_data"
        orders_data = cache.get(cache_key_value)

        if orders_data is None:
            target_user = get_object_or_404(User, pk=user_id)

            orders = Order.objects.filter(user=target_user).prefetch_related("products").all()

            orders_data = OrderSerializer(orders, many=True).data

            cache.set(cache_key_value, orders_data, 300)
        return JsonResponse({"orders": orders_data})


class OrdersExportView(UserPassesTestMixin, View):

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.select_related("user").prefetch_related("products").all()
        result = []
        for order in orders:
            result.append({
                "id": order.id,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user_id": order.user.pk,
                "products_ids": list(order.products.values_list("id", flat=True)),
            })

        return JsonResponse({"orders": result})
