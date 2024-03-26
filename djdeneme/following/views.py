from django.shortcuts import render, get_object_or_404, Http404
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth.models import User
from following.models import Following
from django.template.loader import render_to_string


# Create your views here.
def modal_user_follow_unfollow(request):
    response = sub_user_follow_unfollow(request)
    follow_type = request.GET.get('follow_type')
    owner = request.GET.get('owner')
    print(owner,request.user.username)
    data = response.get('data')
    followed = response.get('followed')
    my_followings = Following.get_followed_username(user=request.user)
    if owner == request.user.username:
        followers_followeds_counts = Following.user_followers_followeds(request.user)
        takipci_sayisi = followers_followeds_counts['takipciler']
        takip_edilenler = followers_followeds_counts['takip_edilenler']
        context2 = {'user': request.user, 'takipciler': takipci_sayisi, 'takip_edilenler': takip_edilenler}
        html_counts = render_to_string('auths/profile/include/following/follower_counts.html', context=context2,
                                request=request)
        if follow_type == "followedes":
            following = Following.get_followings(user=request.user)
        elif follow_type == "followers":
            following = Following.get_followers(user=request.user)
        context = {'following': following, 'my_followings': my_followings, 'follow_type': follow_type}
        html = render_to_string('auths/profile/include/following/followers_following_list.html', context=context,
                                request=request)
        data.update({'html_counts':html_counts ,'html': html , 'owner': True})
    else:
        #profil başkasının ise
        data.update({'owner':False})
    return JsonResponse(data=data)


def user_follow_unfollow(request):
    response = sub_user_follow_unfollow(request)
    data = response.get('data')
    followed = response.get('followed')
    followers_followeds_counts = Following.user_followers_followeds(followed)
    takipciler = followers_followeds_counts['takipciler']
    takip_edilenler = followers_followeds_counts['takip_edilenler']
    context = {'user': followed, 'takipciler': takipciler, 'takip_edilenler': takip_edilenler}
    html = render_to_string('auths/profile/include/following/follower_counts.html', context=context, request=request)
    data.update({'html': html})
    return JsonResponse(data=data)


def sub_user_follow_unfollow(request):
    if not request.is_ajax():  # Ajax isteği değilse bad response hatası
        return HttpResponseBadRequest()
    data = {'takip_durum':True ,'html': '', 'is_valid': True, 'msg': '<b>Takibi bırak</b>'}
    follower_username = request.GET.get('follower_username', None)
    followed_username = request.GET.get('followed_username', None)
    follower = get_object_or_404(User, username=follower_username)
    followed = get_object_or_404(User, username=followed_username)
    is_following = Following.is_user_following(follower=follower, followed=followed)
    if not is_following:
        Following.follow(follower=follower, followed=followed)
    else:
        Following.unfollow(follower=follower, followed=followed)
        data.update({'msg': "<b>Takip et</b>" , 'takip_durum': False})
    return {'data': data, 'followed': followed}


def follower_and_followed_list(request, follow_type):
    data = {'is_valid': True, 'html': ''}
    username = request.GET.get('username', None)
    if not username:
        raise Http404

    user = get_object_or_404(User, username=username)
    # my_followings = Following.get_followings(user=request.user)
    my_followings = Following.get_followed_username(user=request.user)

    if follow_type == "followedes":
        followedes = Following.get_followings(user=user)
        html = render_to_string('auths/profile/include/following/followers_following_list.html',
                                context={'my_followings': my_followings, 'following': followedes,
                                         'follow_type': follow_type}, request=request)
        # kullanıcının takip ettiği kişiler
    elif follow_type == "followers":
        followers = Following.get_followers(user=user)
        html = render_to_string('auths/profile/include/following/followers_following_list.html',
                                context={'my_followings': my_followings, 'following': followers,
                                         'follow_type': follow_type}, request=request)

        # kullanıcıyı takip eden kişiler
    else:
        raise Http404

    data.update({'html': html})
    return JsonResponse(data=data)
