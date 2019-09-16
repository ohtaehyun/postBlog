from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.hashers import check_password
from comuUser.models import CommuUser
from .models import post, category, comment, troloCard, troloList
from django.views.generic import DetailView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json


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
            context['name'] = self.request.session['name']
        return context


def home(request):
    msg = {}
    if request.session.get('user'):
        msg['msg'] = request.session['user']
        msg['name'] = request.session['name']

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


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def troloTest(request):
    msg = {}
    if request.session.get('user'):
        user = CommuUser.objects.get(id=request.session['user'])

        if request.method == 'GET':
            msg['msg'] = user.userName
            msg['name'] = user.id
            if request.GET.get('action') is not None:
                action = request.GET['action']
                if action == "getCard":
                    card = troloCard.objects.get(id=request.GET['cardId'])
                    data = {
                        'cardTitle': card.cardTitle,
                        'cardDescription': card.cardDescription,
                        'listTitle': card.targetList.listTitle
                    }
                    return HttpResponse(json.dumps(data))
            tList = troloList.objects.filter(author=user)
            if tList.count() > 0:
                msg['tList'] = tList
                cList = []
                for t in tList:
                    cards = troloCard.objects.filter(targetList=t)
                    data = {
                        "listTitle": t.listTitle,
                        "cards": cards,
                        "id": t.id
                    }
                    cList.append(data)
                msg['cList'] = cList
            return render(request, 'troloTest.html', msg)
        elif request.method == 'POST':
            action = request.POST['action']
            if action == "addList":
                newList = troloList(
                    listTitle="something",
                    author=user
                )
                newList.save()
                return HttpResponse(newList.id)
            elif action == "addCard":
                listId = request.POST['listId']
                newCard = troloCard(
                    cardTitle="something to do",
                    cardDescription="Description here",
                    targetList=troloList.objects.get(id=listId)
                )
                newCard.save()
                return HttpResponse(newCard.id)
            # msg['cList'] = troloList.objects.filter(author=user)
            return redirect("/troloTest")
            # return render(request, 'troloTest.html', msg)
        elif request.method == "PUT":
            action = request.data['action']
            if action == "cardTitleUpdate":
                print(request.data['cardId'])
                card = get_object_or_404(troloCard, id=request.data['cardId'])
                if request.data['data'] is None:
                    return render(request, 'troloTest.html', msg)
                card.cardTitle = request.data['data']
                card.save()
                return render(request, 'troloTest.html', msg)
            elif action == "listTitleUpdate":
                listObject = get_object_or_404(
                    troloList, id=request.data['listId'])
                listObject.listTitle = request.data['listTitle']
                listObject.save()
                return render(request, 'troloTest.html', msg)
            elif action == "cardDescUpdate":
                card = get_object_or_404(troloCard, id=request.data['cardId'])
                if request.data['data'] is None:
                    return render(request, 'troloTest.html', msg)
                card.cardDescription = request.data['data']
                card.save()
                return render(request, 'troloTest.html', msg)
        elif request.method == "DELETE":
            action = request.data['action']
            if action == "listDelete":
                listObject = get_object_or_404(
                    troloList, id=request.data['listId']
                )
                listObject.delete()
                return render(request, 'troloTest.html', msg)
            elif action == "cardDelete":
                print("??")
                card = get_object_or_404(troloCard, id=request.data['cardId'])
                card.delete()
                return render(request, 'troloTest.html', msg)

    else:
        return render(request, 'trolo.html', msg)
