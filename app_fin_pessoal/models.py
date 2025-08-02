from django.db import models

# Create your models here.

class receitas(models.Model):
    tipo = models.CharField(max_length=255, verbose_name="Tipo")
    natureza = models.CharField(null=True, blank=True, max_length=255, verbose_name="Natureza")
    status = models.CharField(max_length=255, verbose_name="Status")
    fornecedor = models.CharField(max_length=255, verbose_name="Fornecedor")
    parcela = models.CharField(null=True, blank=True, verbose_name="Parcela")
    categoria = models.CharField(null=True, blank=True, verbose_name="Categoria")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor (R$)")
    previsao = models.DateField(null=True, blank=True, verbose_name="Previsão")
    data_pagamento = models.DateField(null=True, blank=True, verbose_name="Data de Pagamento")

class categoria(models.Model):
    tipo = models.CharField(max_length=255, verbose_name="Tipo")
    categ = models.CharField(max_length=255, verbose_name="Categoria")
