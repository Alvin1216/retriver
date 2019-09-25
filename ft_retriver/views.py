from django.shortcuts import render
from ft_retriver.parser import python_parser as ps


def hello(request):
    a = 'hello'
    return render(request, "ft_retriver/search.html", locals())
