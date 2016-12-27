 # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

TOPIC_LIST = ['jishu','xinwen','zhengjing','shenghuo','gongzuo','qita','toupiao']
# Create your models here.
class Role(models.Model):
    role = models.IntegerField()
    def __unicode__(self):
        return self.role

class FollowRelationship(models.Model):
    follower = models.ForeignKey('UserProfile',related_name='follower',on_delete=models.CASCADE)
    followeder = models.ForeignKey('UserProfile',related_name='followeder',on_delete=models.CASCADE)

class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=24)
    sex = models.IntegerField(null=True)
    avatar = models.CharField(max_length=64,default=r'/static/avatars/dft.jpg')
    has_avatar = models.BooleanField(default=False)
    latest_login = models.DateField(auto_now=True)
    signature = models.CharField(max_length=64,null=True)
    role = models.ForeignKey(Role,null=True,blank=True)
    mesg_num = models.IntegerField(default=0)

    def is_following(self,user):
        relationship = FollowRelationship.objects.filter(follower=self,followeder=user)
        if len(relationship)>0:
            return True
        return False

    def is_followed_by(self,user):
        relationship = FollowRelationship.objects.filter(follower=user,followeder=self)
        if len(relationship)>0:
            return True
        return False

    def follow(self,user):
        if not self.is_following(user):
            relationship = FollowRelationship(follower=self,followeder=user)
            relationship.save()

    def unfollow(self,user):
        if self.is_following(user):
            relationship = FollowRelationship.objects.filter(follower=self,followeder=user)
            relationship.delete()

    def inc_mesg_num(self):
        self.mesg_num += 1
        self.save()

    def desc_mesg_num(self):
        if self.mesg_num >0:
            self.mesg_num -= 1
            self.save()

    def __unicode__(self):
        return self.username


class Topic(models.Model):
    topic = models.CharField(max_length=32)

        
    def __unicode__(self):
        return self.topic

def add_topic():
    global TOPIC_LIST
    for tpc in TOPIC_LIST:
        t = Topic(topic=tpc)
        t.save()

class Post(models.Model):
    topic = models.ForeignKey(Topic)
    title = models.CharField(max_length=64)
    author = models.ForeignKey(UserProfile,null=True,on_delete=models.CASCADE,related_name='pstauthor')
    create_time = models.DateField(auto_now_add=True)
    context = models.TextField(max_length=65535)
    repliers = models.IntegerField(default=0)
    praises = models.IntegerField(default=0)
    latest_replier = models.ForeignKey(UserProfile,null=True,on_delete=models.CASCADE,related_name='lst_replier')

    def has_praised_by(self,user):
        praise_relation = PostPraiseRelation.objects.filter(post=self,user=user)
        if len(praise_relation)>0:
            return True
        return False

    def praised_by(self,user):
        praise_relation = PostPraiseRelation(post=self,user=user)
        praise_relation.save()
        self.praises += 1
        self.save()

    def __unicode__(self):
        return self.title


class PostPraiseRelation(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,null=True,blank=True,on_delete=models.CASCADE)


class Vote(models.Model):
    post = models.OneToOneField(Post,on_delete=models.CASCADE)
    closed = models.BooleanField(default=False)
    multi_vote = models.BooleanField(default=False)
    description = models.TextField(max_length=65535)
    voter_num = models.IntegerField(default=0)

    def is_voted_by(self,user):
        vote_relationship = VoteRelaionship.objects.filter(user=user,vote=self)
        if len(vote_relationship)>0:
            return True
        return False

    def voted_by(self,user):
        self.voter_num += 1
        self.save()
        vote_relationship = VoteRelaionship(user=user,vote=self)
        vote_relationship.save()


class VoteOption(models.Model):
    vote = models.ForeignKey(Vote,on_delete=models.CASCADE)
    opt_description = models.CharField(max_length=64)
    opt_num = models.IntegerField(default=0)

    def inc_opt_num(self):
        self.opt_num += 1
        self.save()


class VoteRelaionship(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    vote = models.ForeignKey(Vote,on_delete=models.CASCADE)


class Reply(models.Model):
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,null=True,blank=True,on_delete=models.CASCADE)
    id_in_post = models.IntegerField(null=False,default=1)
    context = models.TextField(max_length=65535)
    create_time = models.DateField(auto_now_add=True)
    praises = models.IntegerField(default=0)
    def has_praised_by(self,user):
        praise_relation = ReplyPraiseRelation.objects.filter(reply=self,user=user)
        if len(praise_relation)>0:
            return True
        return False

    def praised_by(self,user):
        praise_relation = ReplyPraiseRelation(reply=self,user=user)
        praise_relation.save()
        self.praises += 1
        self.save()


class ReplyPraiseRelation(models.Model):
    reply = models.ForeignKey(Reply,on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,null=True,blank=True,on_delete=models.CASCADE)


class Mesg(models.Model):
    MSG_TYPE_CHOICES = (
        (0,'none_type'),
        (1,'call'),
        (2,'reply'),
        (3,'reply_for_reply'),
    )
    msg_type = models.IntegerField(default=0,choices=MSG_TYPE_CHOICES)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,null=True,on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply,null=True,on_delete=models.CASCADE)
    mesg = models.CharField(max_length=64)
    create_time = models.DateField(auto_now_add=True)


class GlobalNotice(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    context = models.TextField(max_length=65535)


class GlobalStatistic(models.Model):
    user_statistic = models.IntegerField(default=0)
    post_statistic = models.IntegerField(default=0)
    essence_statistic = models.IntegerField(default=0)

class GlobalInformation(models.Model):
    global_notice = models.ForeignKey(GlobalNotice,on_delete=models.CASCADE)
    global_statistic = models.ForeignKey(GlobalStatistic,on_delete=models.CASCADE)
