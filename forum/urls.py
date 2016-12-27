from django.conf.urls import url
from views import main
urlpatterns = [
    url(r'^$',main.index,name='home'),
    url(r'^register/$',main.register,name='register'),
    url(r'^login/$',main.login,name='login'),
    url(r'^logout/$',main.logout,name='logout'),
    url(r'^add_post/$',main.add_post,name='add_post'),
    url(r'^del_post/(\d+)/$',main.del_post,name='del_post'),
    url(r'^posts_list_all/$',main.posts_list_all,name='posts_list_all'),
    url(r'^topic/(\d+)/$',main.posts_list_topic,name='topic'),
    url(r'^post/(\d+)/$',main.get_post,name='post'),
    url(r'^user/(\d+)/$',main.get_user,name='user'),
    url(r'^edit_profile/$',main.edit_user,name='edit_profile'),
    url(r'^follow/(\d+)/$',main.follow_user,name='follow'),
    url(r'^unfollow/(\d+)/$',main.unfollow_user,name='unfollow'),
    url(r'^message/$',main.get_mesg,name='message'),
    url(r'^message/(\d+)/$',main.get_mesg_by_id,name='message_by_id'),
    url(r'^praise/(\d+)/$',main.praise,name='praise'),
    url(r'^reply_post/(\d+)/$',main.reply_post,name='reply_post'),
    url(r'^vote_post/(\d+)/$',main.vote_post,name='vote_post'),
    url(r'^close_vote/(\d+)/$',main.close_vote,name='close_vote'),
]