from django.contrib import admin
from app_fin_pessoal import models

# Register your models here.

@admin.register(models.receitas)
class receitas(admin.ModelAdmin):
    list_display = 'id', 'tipo', 'natureza', 'status', 'fornecedor', 'valor', 'previsao', 'data_pagamento'

    class Meta:
        verbose_name = "Receita"

    def __str__(self):
        return self.receitas
    
@admin.register(models.categoria)
class receitas(admin.ModelAdmin):
    list_display = 'id', 'tipo', 'categ'

    class Meta:
        verbose_name = "Categoria"

    def __str__(self):
        return self.receitas