from django.shortcuts import render

def blog(request):
    return render(request, 'blog/blog-single-sidebar.html')
