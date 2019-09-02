from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from comuUser.models import CommuUser
from .models import post, category

# Create your views here.


def postDetail(request, postId):
    msg = {}
    cate_list = category.objects.all()
    po = post.objects.get(postId=postId)

    author = po.author
    po.name = CommuUser.objects.get(id=author.id).userName

    if request.session.get('user'):
        msg['msg'] = request.session['user']
        user = CommuUser.objects.get(id=request.session['user'])
        msg['name'] = user.userName
    msg['cate_list'] = cate_list
    msg['post'] = po
    return render(request, 'postDetail.html', msg)


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

                return redirect('/study')
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
                return redirect('/study')
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

# not using anymore
# def study(request):
#     msg = {}
#     cate_list = category.objects.all()
#     if request.session.get('user'):
#         msg['msg'] = request.session['user']
#         user = CommuUser.objects.get(id=request.session['user'])
#         msg['name'] = user.userName
#     msg['cate_list'] = cate_list
#     return render(request, "study.html", msg)


def getPosts(request, key=18):
    msg = {}
    post_list = post.objects.filter(categoryId=key)
    cate_list = category.objects.all()
    if post_list:
        for posts in post_list:
            author = posts.author
            posts.name = CommuUser.objects.get(id=author.id).userName
        print(author)

        msg['posts'] = post_list
    else:
        msg['error'] = "OOPS! NO POST IN THIS CATEGORY"
        pass
    if request.session.get('user'):
        msg['msg'] = request.session['user']
        user = CommuUser.objects.get(id=request.session['user'])
        msg['name'] = user.userName
    msg['cate_list'] = cate_list
    msg['cate_key'] = key

    return render(request, "getPosts.html", msg)


def home(request):
    msg = {}
    if request.session.get('user'):
        msg['msg'] = request.session['user']
        user = CommuUser.objects.get(id=request.session['user'])
        msg['name'] = user.userName
    # else:
    #     msg['name'] = "unidentified"

    return render(request, "home.html", msg)


def signIn(request):
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
            request.session['name'] = user.userName
            return redirect("/home")
        else:
            err_msg["error"] = "Wrong Password Dude!"
            return render(request, "signIn.html", err_msg)
    else:
        return render(request, 'signIn.html')


# def error_404(request, ex):
#     data = {}
#     data['exception'] = 'exception'

#     return render(request, "404.html", data)
