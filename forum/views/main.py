from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from forum.models import *
from django.template import RequestContext
from forum.forms import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as login_user,logout as logout_user,authenticate
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from myforum import settings

def get_global_res():
    pass

def index(request):
    limit = 15
    posts = Post.objects.all().order_by('-id')
    paginator = Paginator(posts,limit)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)  
    except PageNotAnInteger:  
        posts = paginator.page(1)
    except EmptyPage: 
        posts = paginator.page(paginator.num_pages)
    return render_to_response("index.html",{'posts':posts,'request':request,})

def posts_list_all(request):
    limit = 10
    posts = Post.objects.all().order_by('-id')
    paginator = Paginator(posts,limit)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)  
    except PageNotAnInteger:  
        posts = paginator.page(1)
    except EmptyPage: 
        posts = paginator.page(paginator.num_pages)
    return render_to_response("posts_list.html",{'posts':posts,})

def posts_list_topic(request,topic):
    limit = 15
    tpc = Topic.objects.filter(id=topic)
    posts = Post.objects.filter(topic=tpc).order_by('-id')
    paginator = Paginator(posts,limit)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)  
    except PageNotAnInteger:  
        posts = paginator.page(1)
    except EmptyPage: 
        posts = paginator.page(paginator.num_pages)
    return render_to_response("post_list_topic.html",{'posts':posts,'request':request})

@login_required
def add_post(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    if request.method == 'POST':
        topic = int(request.POST.get('post_topic',None))
        if topic != 7:
            title = request.POST.get('title',None)
            text = request.POST.get('context')
            topc = Topic.objects.filter(id=topic)
            post = Post(topic=topc[0],title=title,context=text,author=request.user)
            post.save()
        else:
            title = request.POST.get('subject',None)
            topc = Topic.objects.filter(id=topic)
            post = Post(topic=topc[0],title=title,author=request.user)
            post.save()
            text = request.POST.get('introduction',None)
            multi = False
            if request.POST.get('optionsRadios') == 'multi':
                multi = True
            vote = Vote(post=post,multi_vote=multi,description=text)
            vote.save()
            for i in range(10) :
                option_str = "%s%d"%('option',i)
                txt = request.POST.get(option_str)
                if txt is not None and txt != '':
                    vote_option = VoteOption(vote=vote,opt_description=txt)
                    vote_option.save()
        return HttpResponseRedirect('/')
    else:
        post_form= PostForm()
        return render_to_response('add_post.html',{'form': post_form,'request':request})

def get_post(request,post_id):
    post = Post.objects.filter(id=post_id)[0]
    if post.topic.id == 7:
        vote = Vote.objects.filter(post=post)[0]
        vote_options = VoteOption.objects.filter(vote=vote).order_by('-opt_num')
        if request.user.is_authenticated():
            i_have_voted = vote.is_voted_by(request.user)
    form = ReplyForm()
    limit = 15
    replies = Reply.objects.filter(post=post)
    paginator = Paginator(replies,limit)
    page = request.GET.get('page')
    try:
        replies = paginator.page(page)  
    except PageNotAnInteger:  
        replies = paginator.page(1)
    except EmptyPage: 
        replies = paginator.page(paginator.num_pages)
    return render_to_response("post.html",locals())

@login_required
def reply_post(request,post_id):
    if request.method == 'POST':
        post = Post.objects.filter(id=post_id)[0]
        if request.POST.get('reply_submit',None) == 'reply_submit':
            context = request.POST.get('context',None)
            if context is not None:
                rply_cnt = Reply.objects.filter(post=post).count()
                reply = Reply(author=request.user,post=post,id_in_post=rply_cnt+1,context=context)
                reply.save()
                post.latest_replier = request.user
                post.repliers += 1
                post.save()
                if post.author != request.user:
                    msg = Mesg.objects.filter(msg_type=2,post=post)
                    if len(msg) == 0:
                        msg = Mesg(msg_type=2,user=post.author,post=post,mesg='someone replied you...')
                        msg.save()
                        post.author.inc_mesg_num()
    return HttpResponseRedirect('/post/'+str(post_id)+'/#'+str(rply_cnt+1))

@login_required
def vote_post(request,post_id):
    post = Post.objects.filter(id=post_id)[0]
    if request.method == 'POST' and post.topic.id == 7:
        vote = Vote.objects.filter(post=post)[0]
        vote_options = VoteOption.objects.filter(vote=vote)
        if request.POST.get('vote_submit',None) == 'vote_submit_multi':
            for i in range(len(list(vote_options))):
                status = request.POST.get("%s%d"%('option',(i+1)))
                if status == 'on' :
                    vote_options[i].inc_opt_num()
            vote.voted_by(request.user)
        if request.POST.get('vote_submit',None) == 'vote_submit':
            op = request.POST.get('optionsRadios')
            num = int(op[6])
            vote_options[num-1].inc_opt_num()
            vote.voted_by(request.user)
    return HttpResponseRedirect('/post/'+str(post_id))

@login_required
def del_post(request,post_id):
    posts = Post.objects.filter(id=post_id)
    if len(posts)>0:
        post = posts[0]
    else:
        return HttpResponseRedirect('/')
    if request.user == post.author:
        post.delete()
    return HttpResponseRedirect('/')

@login_required
def praise(request,post_id):
    if request.method == 'POST':
        post = Post.objects.filter(id=post_id)[0]
        if not post.has_praised_by(request.user):
            post.praised_by(request.user)
    return HttpResponseRedirect('/post/'+str(post_id))

@login_required
def close_vote(request,post_id):
    if request.method == 'POST':
        post = Post.objects.filter(id=post_id)[0]
        vote = Vote.objects.filter(post=post)[0]
        vote.closed = True
        vote.save()
    return HttpResponseRedirect('/post/'+str(post_id))

def get_user(request,user_id):
    user = UserProfile.objects.filter(id=user_id)[0]
    followings = FollowRelationship.objects.filter(follower=user).count()
    followeders = FollowRelationship.objects.filter(followeder=user).count()
    posts = Post.objects.filter(author=user)
    post_num = posts.count()
    msg_num = Mesg.objects.filter(user=user).count()
    if not request.user.is_authenticated():
        button_tag = 'None'
    elif request.user == user:
        user = request.user
        button_tag = 'None'
    else:
        if request.user.is_following(user):
            button_tag = 'unfollow'
        else:
            button_tag = 'follow'
    return render_to_response('profile.html',locals())

class MesgBody:
    def __init__(self,msg,linkage):
        self.msg = msg
        self.linkage = linkage

@login_required
def get_mesg(request):
    mesgs = Mesg.objects.filter(user=request.user)
    return render_to_response('message.html',locals())

@login_required
def get_mesg_by_id(request,msg_id):
    msg = Mesg.objects.filter(id=msg_id)[0]
    if msg.msg_type == 2:
        post_id = msg.post.id
        linkage = r'/post/'+str(post_id)
    else:
        post_id = msg.post.id
        page = 1+msg.reply.id_in_post//10
        num_in_page = msg.reply.id_in_post
        linkage = r'/post/'+str(post_id)+r'/?page='+str(page)+r'#'+str(num_in_page)
    request.user.desc_mesg_num()
    msg.delete()
    return HttpResponseRedirect(linkage)

@login_required
def del_mesg_all(request):
    mesgs = Mesg.objects.filter(user=request.user)
    for msg in mesgs:
        msg.delete()
    request.user.mesg_num = 0
    request.user.save()
    return HttpResponseRedirect('/')

@login_required
def del_mesg_by_id(request,msg_id):
    mesg = Mesg.objects.filter(user=request.user,id=msg_id)[0]
    mesg.delete()
    request.user.desc_mesg_num()
    return HttpResponseRedirect('/')

@login_required
def edit_user(request):
    if request.method == 'POST':
        if request.POST.get('name') != '':
            request.user.username = request.POST.get('name')
        if request.POST.get('signature') != '':
            request.user.signature = request.POST.get('signature')
        if request.POST.get('sex') != '':
            request.user.sex = request.POST.get('sex')
        imgfile = request.FILES.get('inputfile')
        if imgfile is None:
            return HttpResponseRedirect('/')
        img = imgfile.read()
        dest_path = settings.FORUM_STATIC_ROOT+'/avatars/'
        with  open(dest_path+str(request.user.id),'w') as dest:
            if img is None:
                return HttpResponseRedirect('/')
            dest.write(img)
        request.user.avatar = '/static/avatars/'+str(request.user.id)
        request.user.has_avatar = True
        request.user.save()
        return HttpResponseRedirect('/user/'+str(request.user.id))
    return render_to_response('edit_profile.html',{'request':request})

@login_required
def follow_user(request,user_id):
    if request.user.id != user_id:
        user = UserProfile.objects.filter(id=user_id)[0]
        request.user.follow(user)
    return HttpResponseRedirect('/user/'+user_id)

@login_required
def unfollow_user(request,user_id):
    if request.user.id != user_id:
        user = UserProfile.objects.filter(id=user_id)[0]
        request.user.unfollow(user)
    return HttpResponseRedirect('/user/'+user_id)

def register(request):
    if request.method == 'POST':
        user = UserProfile.objects.filter(username=request.POST.get('username'))
        if len(user)>0:
            msg = 'Username has already been used!'
            return render_to_response('register.html',{'msg':msg})
        user = UserProfile.objects.filter(email=request.POST.get('mailbox'))
        if len(user) > 0:
            msg = 'Email has already been used!'
            return render_to_response('register.html',{'msg':msg})
        if request.POST.get('passwd') != request.POST.get('passwd_again'):
            msg = 'Password is not same!'
            return render_to_response('register.html',{'msg':msg})
        user = UserProfile.objects.create_user(username=request.POST.get('username'),
            email=request.POST.get('mailbox'),
            password=request.POST.get('passwd'))
        user.save()
        return HttpResponseRedirect('/')
    else:
        regform = RegisterForm()
        return render_to_response('register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('passwd')
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login_user(request,user)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            msg = 'username or passwd error!'
            
            return HttpResponse(msg)

def logout(request):
    logout_user(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))




