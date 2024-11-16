from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Article
from .forms import ArticleForm

# Vista pública - no requiere autenticación
def index(request):
    """Lista todas las tareas/artículos"""
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'blog/index.html', {
        'articles': articles,
    })

@login_required
def create(request):
    """Crear nuevo artículo - requiere autenticación"""
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('blog:index')
    else:
        form = ArticleForm()
    
    return render(request, 'blog/create.html', {
        'form': form,
    })

def detail(request, article_id):
    """Ver detalle de un artículo"""
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'blog/detail.html', {
        'article': article,
    })

@login_required
def edit(request, article_id):
    """Editar artículo - requiere autenticación y ser el autor"""
    article = get_object_or_404(Article, id=article_id)
    
    # Verificar que el usuario actual sea el autor
    if article.author != request.user:
        raise PermissionDenied
        
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('blog:detail', article_id=article.id)
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'blog/edit.html', {
        'article': article,
        'form': form,
    })

@login_required
def delete(request, article_id):
    """Eliminar artículo - requiere autenticación y ser el autor"""
    article = get_object_or_404(Article, id=article_id)
    
    # Verificar que el usuario actual sea el autor
    if article.author != request.user:
        raise PermissionDenied
        
    if request.method == 'POST':
        article.delete()
        return redirect('blog:index')
        
    return render(request, 'blog/delete.html', {
        'article': article,
    })
