from django.shortcuts import render
from django.views import View
from pirates.models import Tesouro
from django.db.models import F,ExpressionWrapper,DecimalField
from django import forms
from django.http import HttpResponseRedirect,  HttpResponseNotFound
from django.urls import reverse

class ListaTesourosView(View):
    def get(self, request):
        campo_calculado = DecimalField(max_digits=10, decimal_places=2, blank=True)
        valor_total_tesouro = ExpressionWrapper(F('preco')*F('quantidade'), output_field=campo_calculado)
        nova_coluna = Tesouro.objects.annotate(valor_total = valor_total_tesouro)

        total = 0
        for tesouro in nova_coluna:
            total+=tesouro.valor_total
        
        return render(request, "lista_tesouros.html", {"lista_tesouros": nova_coluna,"total_geral":total} )

class ListaTesourosViewForm(forms.ModelForm):
    class Meta:
        model = Tesouro
        fields = ['nome', 'preco', 'quantidade', 'img_tesouro']
        labels = {"img_tesouro": "Imagem"}

class SalvarTesouro(View):
    def get(self, request, id=None):
        if id != None:
            atualizar_tesouro = Tesouro.objects.get(id=id)
        else:
            atualizar_tesouro = None
            
        return render(request, "salvar_tesouro.html", {"tesouro_novo": ListaTesourosViewForm(instance=atualizar_tesouro)})
    
    def post(self, request, id=None):
        if id != None:
            atualizar_tesouro = Tesouro.objects.get(id=id)
        else:
            atualizar_tesouro = None
        
        form = ListaTesourosViewForm(request.POST,request.FILES, instance=atualizar_tesouro)
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tesouro'))
        else:
            return render(request,"salvar_tesouro.html", {"tesouro_novo": form})

class DeletarTesouro(View):
    def get(self, request, id):
        try:
            Tesouro.objects.get(id=id).delete()
        except:
            return HttpResponseNotFound('<h1>Page not found</h1>')

        return HttpResponseRedirect(reverse('tesouro'))

        




