
from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from django.http import JsonResponse
from django.db.models import Count
from django.http import Http404
from django.core.mail import EmailMessage, send_mail

@login_required
def home(request):
    if not request.user.is_authenticated:
        return redirect("users:login")
    name = request.GET.get('name')
    filter_price_min = request.GET.get('price_min')
    filter_price_max = request.GET.get('price_max')
    category = request.GET.get('category')
    cats = Category.objects.all()
    
    profile = get_profile(request.user)
    
    # Start with all published products
    products = Product.objects.filter(is_published=True)
    
    # Apply filters
    if name:
        products = products.filter(name__icontains=name)
    if category:
        products = products.filter(category__name__icontains=category)
    if filter_price_min:
        price_min = int(filter_price_min)
        products = products.filter(price__gte=price_min)

    if filter_price_max:
        price_max = int(filter_price_max)
        products = products.filter(price__lte=price_max)

    
    # Annotate and order products
    products = products.annotate(likes_count=Count('likes'))
    products = products.annotate(dislikes_count=Count('dislikes'))
    
    # Prepare like and dislike icons for each product

    
    return render(request, 'shop/home.html', {
        'products': products,
        'profile': profile,
        'cats': cats,
    })
class AddProduct(LoginRequiredMixin,CreateView):
    form_class = AddProduct
    template_name = 'shop/add_product.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')

    def get_context_data(self,*, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['images'] = AddImagesFormSet(self.request.POST, self.request.FILES)
        else:
            context['images'] = AddImagesFormSet()

        context['profile'] = get_profile(self.request.user)
        return context


    def form_valid(self, form):
        context = self.get_context_data()
        images = context['images']
        print(any(bool(image.get('image')) for image in images.cleaned_data))
        context['is_published']=False
        try:
            price = int(form.cleaned_data['price'])
        except:
            return redirect('add_product')
        self.object = form.save()
        if images.is_valid():
            images.instance = self.object
            images.save()
        try:
            form.instance.seller = self.request.user.profile

            return super(AddProduct, self).form_valid(form)
        except:
            return redirect('users:login')          

class ShowProduct(LoginRequiredMixin,DetailView):
    model = Product
    slug_url_kwarg = 'product_slug'
    template_name = "shop/show_product.html"
    context_object_name='product'
    def get_context_data(self, object_list =None, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user:
            profile = get_profile(self.request.user)
            context['profile'] =profile
        return context

@login_required(login_url='login')
class CartDetail(DetailView):
    model = Cart
    template_name = 'shop/card_detail.html'
    context_object_name = "cart_items"

    def get_context_data(self,object_list=None, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile']=get_profile(self.request.user)
        return context

@login_required(login_url='login')
class AddToCart(ListView):
    model = Cart
    template_name = 'shop/card_detail'
    context_object_name = "cart_items"

    def get_queryset(self, *args, **kwargs): 
        context = super(AddToCart, self).get_queryset(*args, **kwargs)
        product = get_object_or_404(Product, id=product_id)
        context["product"] = Cart.objects.get_or_create(product = product)
        if not created:
            context['product'].quantity += 1
        return context


@login_required(login_url='login')
def get_cart(request):
    profile= request.user.profile
    print(profile)
    if not profile:
        return redirect('users:login')
    return Cart.objects.filter(profile=profile)

@login_required(login_url='login')
def add_to_cart(request, product_id):

    profile= request.user.profile
    if not profile:
        return redirect('users:login')
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(profile=profile,product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')

@login_required(login_url='login')
def cart_detail(request):
    cart_items = get_cart(request)
    profile= request.user.profile

    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'shop/card_detail.html', {'cart_items': cart_items, 'total':total, 'profile':profile})



@login_required(login_url='login')
def remove_from_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('users:login')

    try:
        profile = request.user.profile
        print(profile)
    except AttributeError:
        print("User profile does not exist.")
        return redirect('users:login')

    print(f"Profile: {profile}, Product ID: {product_id}")

    try:
        cart_item = Cart.objects.filter(id=product_id, profile=profile)
        print(f"Cart Item Found: {cart_item}")
        cart_item.delete()
        print("Cart item deleted.")
    except Http404:
        print("Cart item not found.")
    
    return redirect('cart_detail')

        

@login_required(login_url='login')
def moder (request):
    if request.user.is_staff:
        products = Product.objects.filter(is_published = False, is_banned =False)
        return render(request, 'shop/moder.html', {"products": products})
    else:
        return redirect('home')



def accept(request, product_id):
    product = Product.objects.get(id = product_id)
    product.is_published = True
    product.save()
    return redirect('moder')

def ban(request, product_id):
    product = Product.objects.get(id = product_id)
    product.is_banned = True
    product.save()
    return redirect("moder")


class AddLike(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        product = Product.objects.get(pk=pk)
        likes = product.likes.all()
        print(likes.count())
        is_dislike = False

        for dislike in product.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break


        if is_dislike:
            product.dislikes.remove(request.user)

        is_like = False

        for like in product.likes.all():
            if like == request.user:
                is_like = True
                break




        if is_like:
            product.likes.remove(request.user)
        else:
            product.likes.add(request.user)

        return redirect('home')



class AddDislike(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        product = Product.objects.get(pk=pk)

        is_like = False

        for like in product.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            product.likes.remove(request.user)



        is_dislike = False

        for dislike in product.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break


        if is_dislike:
            product.dislikes.remove(request.user)
        else:
            product.dislikes.add(request.user)

        return redirect('home')

def get_profile(user):
    return get_object_or_404(Profile, user=user)

class EditProduct(LoginRequiredMixin, UpdateView):
    model = Product
    #form_class = AddProduct
    fields = ['name', 'content', 'price', 'category']
    template_name = 'shop/edit_product.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        profile = get_profile(self.request.user)
        return Product.objects.filter(seller=profile.id)

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        context['profile'] = get_profile(self.request.user)
        product = self.object
        if self.request.POST:
            context['images'] = AddImagesFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['images'] = AddImagesFormSet(instance=self.object)

        #num_images = product.productimages_set.count()
        #print(num_images)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        images_formset = context['images']
        if images_formset.is_valid():
            response = super().form_valid(form)
            images_formset.instance = self.object

            num_valid_images = len([form for form in images_formset if form.cleaned_data])
            if num_valid_images>3:

                form.add_error(None, 'Количество изображений не может превышать трех.')
                return self.form_invalid(form)
            print(f'Number of valid images: {num_valid_images}')
            images_formset.save()
            return response
        else:
            print('invalid')
            return self.form_invalid(form)
    def form_invalid(self, form):
        context = self.get_context_data()
        return self.render_to_response(context)

class DeleteProduct(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'shop/confirm_delete.html'
    context_object_name = 'product'  # Make sure this matches what you use in the template
    success_url = reverse_lazy('home')
    def get_context_data(self, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_profile(self.request.user)
        return context

    def get_queryset(self):
        # Ensure the user can only delete their own products
        profile = get_profile(self.request.user)
        return Product.objects.filter(seller=profile)
class MyProducts(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'shop/home.html'
    context_object_name = 'products'
    def get_context_data(self,*,object_list =None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile']=get_profile(self.request.user)
        return context

    def get_queryset(self):
        # Ensure the user can only delete their own products
        profile = get_profile(self.request.user)
        print(profile.id)
        return Product.objects.filter(seller=profile.id)


class SellerProducts(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'shop/home.html'
    context_object_name = 'products'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_profile(self.request.user)
        return context

    def get_queryset(self):
        # Ensure the user can only delete their own products
        #profile = get_profile(self.request.user)
        profile_slug = self.kwargs['profile_slug']
        profile = get_object_or_404(Profile, slug=profile_slug)
        return Product.objects.filter(seller=profile)


@login_required
def contact(request):
    profile = get_profile(request.user) 
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        email = request.user.email
       
        if title and content:
 
            email_subject = f'Жалоба: {title}'
            email_body = f"{content}\n\n Имя пользователя: {profile}\nОписание пользователя: {profile.description}"
            email_recipient = ["trew5804@gmail.com"]
            
            email_message = EmailMessage(email_subject, email_body, email, email_recipient)
            
            # Attach the image if it was uploaded
            if image:
                email_message.attach(image.name, image.read(), image.content_type)
                print('imageIss ghhhhhhhhh')
            
            email_message.send()
            return redirect('home')
    
    return render(request, 'shop/contact.html', {'profile':profile})


class CreateCategory(LoginRequiredMixin,CreateView):
    model =Category
    form_class = CategoryForm
    template_name='shop/add_category.html'
    success_url = reverse_lazy('add_category')
    login_url = reverse_lazy('users:login')
    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_profile(self.request.user)
        return context