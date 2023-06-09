import logging
from django.shortcuts import render, redirect
from .models import Product, Favorite
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

def paginate(request, args, prods_per_page):
    """ Paginate function """
    paginator = Paginator(args, prods_per_page)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return page_obj

def search(request):
    """ Display product or products matching the user's request """
    query = request.GET.get('query')
    if query:
        # search by product name
        products = Product.objects.filter(
            name__icontains=query).order_by('nutriscore', 'id')

        # if nothing is found, search by brands name
        if not products.exists():
            products = Product.objects.filter(
                brands__icontains=query).order_by('nutriscore', 'id')
        # if nothing is found
        if not products.exists():
            messages.success(request,
                             "Nous n'avons trouvé aucun produit "
                             "correspondant à votre recherche")
            return redirect('index')

        context = {'page_obj': paginate(request, products, 9),
                   'query': query}

        logger.info('New search', exc_info=True, extra={
            # Optionally pass a request and we'll grab any information we can
            'request': request,
        })

        return render(request, 'core/search.html', context)

    else:
        messages.success(request, "Vous n'avez rien saisi")
        return redirect('index')

def product(request, product_id):
    """ Display the product's information """
    prod = Product.objects.get(id=product_id)
    context = {'prod': prod}
    return render(request, 'core/product.html', context)


def substitute(request, product_id):
    """ Display substitutes list """
    prod = Product.objects.get(id=product_id)
    cat = prod.categories.get()
    subs = cat.products.all().order_by('nutriscore', 'id')
    sub_list = []
    for i in subs:
        if i.nutriscore <= prod.nutriscore:
            sub_list.append(i)

    sub_list.remove(prod)
    context = {'prod': prod,
               'page_obj': paginate(request, sub_list, 9)}
    return render(request, 'substitute.html', context)

@login_required
def save(request, product_id, prod_id):
    """ Saves product and substitute """
    user = request.user
    try:
        fav = Favorite.objects.filter(user_id=user.id,
                                      sub_id=product_id,
                                      prod_id=prod_id)
        if not fav:
            Favorite.objects.create(user_id=user.id,
                                    sub_id=product_id,
                                    prod_id=prod_id)
            messages.success(request, 'Produit sauvegardé')
        else:
            messages.success(request, 'Le produit est déjà sauvegardé')

    finally:
        return redirect('index')


@login_required
def favorite(request):
    """ Display user's favorites """
    user = request.user
    favs = Favorite.objects.filter(user_id=user.id)

    context = {'page_obj': paginate(request, favs, 3)}
    return render(request, 'favorite.html', context)


@login_required
def delete(request, fav):
    """ Delete user's favorite """
    favori = Favorite.objects.filter(id=fav)
    favori.delete()
    messages.success(request, 'Le favori à bien été supprimé')
    return redirect('index')