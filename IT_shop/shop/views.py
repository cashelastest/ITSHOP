from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from django.http import JsonResponse


@login_required
def home(request):
 return render(request, 'shop/home.html')

class AddProduct(LoginRequiredMixin,CreateView):
	form_class = AddProduct
	template_name = 'shop/add_product.html'
	success_url = reverse_lazy('home')
	login_url = reverse_lazy('home')

	def get_context_data(self,*, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)

		if self.request.POST:
			context['images'] = AddImagesFormSet(self.request.POST, self.request.FILES)
		else:
			context['images'] = AddImagesFormSet()
		return context


	def form_valid(self, form):
		context = self.get_context_data()
		images = context['images']
		self.object = form.save()
		if images.is_valid():
			images.instance = self.object
			images.save()
		form.instance.seller = self.request.user.profile
		return super(AddProduct, self).form_valid(form)

class ShowProduct(DetailView):
	model = Product
	slug_url_kwarg = 'product_slug'
	template_name = "shop/show_product.html"
	context_object_name='product'
class ProductsList(ListView):
	model = Product
	template_name = 'shop/home.html'
	context_object_name = 'products'


	def get_queryset(self):
		return Product.objects.prefetch_related('images')




def get_cart(request):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
    return Cart.objects.filter(session_id=session_id)

def add_to_cart(request, product_id):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(product=product, session_id=session_id)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')

def cart_detail(request):
    cart_items = get_cart(request)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'shop/card_detail.html', {'cart_items': cart_items, 'total': total})

def remove_from_cart(request, product_id):
    session_id = request.session.session_key
    cart_item = get_object_or_404(Cart, product_id=product_id, session_id=session_id)
    cart_item.delete()
    return redirect('cart_detail')
