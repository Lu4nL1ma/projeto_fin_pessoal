from django import template
import locale

register = template.Library()

#definir local global
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

@register.filter
def formata_cpf(value):
    # Lógica para formatar o CPF
    return f"{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:]}"

@register.filter
def formata_telefone(value):
    # Lógica para formatar telefone
    return (f"({value[:2]}){value[2:7]}-{value[7:]}")
@register.filter
def formata_reais(valor):
    """Formata um valor numérico para o padrão brasileiro de reais."""
    return locale.currency(valor, grouping=True)