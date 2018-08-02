from django.shortcuts import render

# Create your views here.
#from django.views.generic import ListView
from website.models import Post
#from django.views.generic import TemplateView, View
#from django.http import HttpResponse

from .serializers import PostHtmlSerializer, PostSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def posts_by_tag(self, tag):
    return render(self, 'post_list.html', {"tag": tag})

def post(self, post_id):
    post = Post.objects.filter(id = post_id).first()
    data = PostHtmlSerializer(post).data
    return render(self, 'post.html', {"post": data})
    
def posts_view(self):
    tag = self.GET.get('tag')
    return render(self, 'post_list.html', {"tag": tag})

@api_view(['GET', 'POST'])
def posts(request):
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        
        posts = Post.objects.filter(is_raw = False).order_by('-post_date')
        tag = request.GET.get('tag')
        if not tag == 'None':
            posts = posts.filter(tags__name__exact=tag)
        page = request.GET.get('page', 1)
        paginator = Paginator(posts, 5)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = PostSerializer(data,context={'request': request} ,many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/api/posts/?page=' + str(nextPage), 'prevlink': '/api/products/?page=' + str(previousPage)})

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)