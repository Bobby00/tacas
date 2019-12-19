from django.shortcuts import render

def analysis(request):
    return render(request, 'analysis_and_opinion.html')