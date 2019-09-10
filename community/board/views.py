from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from comuUser.models import CommuUser
from .models import post, category, comment
from django.views.generic import DetailView


def addPost(request):
    msg = {}
    if CommuUser.objects.get(id=request.session['user']) is None:
        return redirect('/')
    elif CommuUser.objects.get(id=request.session['user']).userName == "othdev95":
        msg['name'] = "othdev95"
        msg['cates'] = category.objects.all()
        if request.method == "POST":
            #  make post model
            if request.POST.get("postTitle") and request.POST.get("postContent"):
                po = post(
                    categoryId=category.objects.get(
                        categoryName=request.POST.get("categoryName")),
                    postTitle=request.POST.get("postTitle"),
                    postContent=request.POST.get("postContent"),
                    author=CommuUser.objects.get(userName=msg['name'])
                )
                po.save()

                return redirect('/posts/1')
            else:
                msg['error'] = "항목을 모두 입력하십쇼 HUMAN"
                return render(request, "addPost.html", msg)
        else:
            return render(request, 'addPost.html', msg)

    else:
        return redirect('/')


def addCategory(request):
    msg = {}
    if CommuUser.objects.get(id=request.session['user']) is None:
        return redirect('/')
    elif CommuUser.objects.get(id=request.session['user']).userName == "othdev95":
        msg['name'] = "othdev95"
        if request.method == "POST":

            categoryName = request.POST.get("categoryName")

            if(categoryName is not None):
                cate = category(
                    categoryName=categoryName
                )
                cate.save()
                return redirect('/posts/1')
            else:
                msg['error'] = "항목을 입력 하십쇼"
                return render(request, 'addCategory.html', msg)
        else:
            return render(request, 'addCategory.html', msg)
    else:
        return redirect('/')


def signOut(request):
    if request.session.get('user'):
        del(request.session['user'])
    return redirect('../')


def review(request):
    msg = {}
    if request.session.get('user'):
        msg['msg'] = request.session['user']
        user = CommuUser.objects.get(id=request.session['user'])
        msg['name'] = user.userName
    return render(request, "review.html", msg)


class postList(DetailView):
    model = category
    template_name = "getPosts.html"

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(**kwargs)
        cate = self.get_object()
        cate_list = category.objects.all()
        context["cate_list"] = cate_list
        context["posts"] = get_list_or_404(post, categoryId=cate)
        if self.request.session.get('user') is not None:
            context['msg'] = self.request.session['user']
            user = CommuUser.objects.get(id=self.request.session['user'])
            context['name'] = user.userName
        return context


def home(request):
    msg = {}
    if request.session.get('user'):
        msg['msg'] = request.session['user']
        user = CommuUser.objects.get(id=request.session['user'])
        msg['name'] = user.userName

    return render(request, "home.html", msg)


def signIn(request):
    if request.session.get('user'):
        return redirect("/home")

    if request.method == "POST":
        userName = request.POST.get('userName', None)
        userEmail = request.POST.get('userEmail', None)
        userPassword = request.POST.get('userPassword', None)
        err_msg = {}
        user = CommuUser
        if userName:
            user = get_object_or_404(CommuUser, userName=userName)
        elif userEmail:
            user = get_object_or_404(CommuUser, userEmail=userEmail)
        else:
            return render(request, 'signIn.html', err_msg)

        if check_password(userPassword, user.userPassword):
            request.session['user'] = user.id
            user = CommuUser.objects.get(id=request.session['user'])
            request.session['name'] = user.userName
            return redirect("/home")
        else:
            err_msg["error"] = "Wrong Password Dude!"
            return render(request, "signIn.html", err_msg)
    else:
        return render(request, 'signIn.html')


class postDetail(DetailView):
    model = post
    template_name = "postDetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        co_list = comment.objects.filter(
            targetPost=self.get_object())
        if self.request.session.get('user') is not None:
            context["msg"] = self.request.session['user']
            context["name"] = self.request.session['name']

        for com in co_list:
            commentAuthor = com.author
            com.name = CommuUser.objects.get(id=commentAuthor.id).userName

        context["comment_list"] = co_list
        context['cate_list'] = category.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        if self.request.POST.get("commentContent"):
            name = self.request.session['name']
            co = comment(
                commentContent=self.request.POST.get("commentContent"),
                targetPost=post.objects.get(postId=self.get_object().postId),
                author=CommuUser.objects.get(
                    userName=name)
            )
            co.save()
        return redirect(request.get_full_path())


def trolo(request):
    msg = {}
    if request.session.get('user'):
        print("!!!!!!!!!!!!!!!!!!!!!")
        msg['msg'] = request.session['user']
        user = CommuUser.objects.get(id=request.session['user'])
        msg['name'] = user.userName

    return render(request, 'trolo.html', msg)
