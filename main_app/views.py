from django.shortcuts import render

def test_vew(request):
    return render(request, 'base.html', {})
