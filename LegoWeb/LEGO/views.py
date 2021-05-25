from django.shortcuts import render, get_object_or_404, redirect
# from LEGO.models import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from LEGO.forms import *
from django.views.generic import TemplateView


# Create your views here.
def get_set_list(request):
    sets = LegoSets.objects.all().order_by('setid')

    return render(request, 'LEGO/set_list.html', {'page_title': 'LEGO Sets',
                                                  'sets': sets,
                                                  })


def get_theme_list(request):
    themes = LegoThemes.objects.all().order_by('themeid')

    return render(request, 'LEGO/theme_list.html', {'page_title': 'LEGO Themes',
                                                    'themes': themes,
                                                    })


def get_shop_list(request):
    shops = LegoShops.objects.all().order_by('shopid')

    return render(request, 'LEGO/shop_list.html', {'page_title': 'LEGO Shops',
                                                   'shops': shops,
                                                   })


def get_purchase_list(request):
    purchases = LegoPurchases.objects.all().order_by('purchaseid')

    return render(request, 'LEGO/purchase_list.html', {'page_title': 'LEGO Einkäufe',
                                                       'purchases': purchases,
                                                       })


def get_impressum(request):
    return render(request, 'LEGO/impressum.html', {'page_title': 'Kontakt',
                                                   })


def add_set(request):
    legoset = LegoSets()

    if request.method == 'POST':
        form = SetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Set saved')
            return HttpResponseRedirect(reverse_lazy('set_list'))
        else:
            messages.error(request, 'Daten falsch')
    else:
        form = SetForm(instance=legoset)

    return render(request, 'LEGO/add_set.html', {'page_title': 'Set hinzufügen',
                                                 'form': form,
                                                 })


def add_theme(request):
    legotheme = LegoThemes()

    if request.method == 'POST':
        form = ThemeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Theme saved')
            return HttpResponseRedirect(reverse_lazy('theme_list'))
        else:
            messages.error(request, 'Daten falsch')
    else:
        form = ThemeForm(instance=legotheme)

    return render(request, 'LEGO/add_theme.html', {'page_title': 'Theme hinzufügen',
                                                   'form': form,
                                                   })


def add_shop(request):
    legoshop = LegoShops()

    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Shop saved')
            return HttpResponseRedirect(reverse_lazy('shop_list'))
        else:
            messages.error(request, 'Daten falsch')
    else:
        form = ShopForm(instance=legoshop)

    return render(request, 'LEGO/add_shop.html', {'page_title': 'Shop hinzufügen',
                                                  'form': form,
                                                  })


def add_purchase(request):
    legopurchase = LegoPurchases()

    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Purchase saved')
            return HttpResponseRedirect(reverse_lazy('purchase_list'))
        else:
            messages.error(request, 'Daten falsch')
    else:
        form = PurchaseForm(instance=legopurchase)

    return render(request, 'LEGO/add_purchase.html', {'page_title': 'Einkauf hinzufügen',
                                                      'form': form,
                                                      })


def delete_set(request, pk):
    try:
        legoset = get_object_or_404(LegoSets, pk=pk)
        if request.method == 'POST':
            legoset.delete()
            return redirect('/sets')

        form = SetForm(request.POST)
        return render(request, "LEGO/set_list.html", {'page_title': 'LEGO Sets',
                                                      'form': form
                                                      })
    except:
        messages.error(request, 'Set kann nicht gelöscht werden, da es noch verwendet wird')
        return HttpResponseRedirect(reverse_lazy('set_list'))


def delete_theme(request, pk):
    try:
        legotheme = get_object_or_404(LegoThemes, pk=pk)
        if request.method == 'POST':
            legotheme.delete()
            return redirect('/themes')

        form = ThemeForm(request.POST)
        return render(request, "LEGO/theme_list.html", {'page_title': 'LEGO Themes',
                                                    'form': form
                                                    })
    except:
        messages.error(request, 'Theme kann nicht gelöscht werden, da es noch verwendet wird')
        return HttpResponseRedirect(reverse_lazy('theme_list'))


def delete_shop(request, pk):
    try:
        legoshop = get_object_or_404(LegoShops, pk=pk)
        if request.method == 'POST':
            legoshop.delete()
            return redirect('/shops')

        form = ShopForm(request.POST)
        return render(request, "LEGO/shop_list.html", {'page_title': 'LEGO Shops',
                                                       'form': form
                                                       })
    except:
        messages.error(request, 'Shop kann nicht gelöscht werden, da es noch verwendet wird')
        return HttpResponseRedirect(reverse_lazy('shop_list'))


def delete_purchase(request, pk):
    try:
        legopurchase = get_object_or_404(LegoPurchases, pk=pk)
        if request.method == 'POST':
            legopurchase.delete()
            return redirect('/purchases')

        form = PurchaseForm(request.POST)
        return render(request, "LEGO/purchase_list.html", {'page_title': 'LEGO Einkäufe',
                                                           'form': form
                                                           })
    except:
        messages.error(request, 'Einkauf kann nicht gelöscht werden, da es noch verwendet wird')
        return HttpResponseRedirect(reverse_lazy('purchase_list'))


def edit_purchase(request, pk):
    legopurchase = get_object_or_404(LegoPurchases, pk=pk)
    form = PurchaseForm(instance=legopurchase)

    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=legopurchase)
        if form.is_valid():
            form.save(commit=False)
            return redirect('/')

    return render(request, "LEGO/purchase_list.html", {'page_title': 'LEGO Einkäufe',
                                                       'form': form
                                                       })


class ThemeChartView(TemplateView):
    template_name = 'LEGO/theme_chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = LegoPurchases.objects.all()
        return context
