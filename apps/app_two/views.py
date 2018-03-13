from django.shortcuts import render, HttpResponse, redirect
from ..app_one.models import User
from .models import Invitation
from django.contrib import messages


def index(request):
    if 'user_id' not in request.session:
        return redirect('app1:index')
    else:
        print("This is index function in app2 views.py")
        user_id = request.session['user_id']
        session_user = User.objects.get(id=user_id)
        print(session_user.name, session_user.email, session_user.desc, "user id is:", user_id)

# finds professional network: invitees who accepted user's invitations
# Note: some early Invitation objects had session users inviting themselves
# last exclusion is to filter those out
        user_invitees = Invitation.objects.filter(inviter=session_user).exclude(invitee=session_user)
        accepted_invitations = []
        for invitee in user_invitees:
            if invitee.accept == True:
                print(invitee.invitee.name,"has accepted")
                accepted_invitations.append(invitee)
            else:
                print(invitee.invitee.name, "has not accepted")

# finds all users who extended an invitation to session user
# uses reverse lookup for FK invitee link
# excludes those who session user has already accepted or ignored
# also excludes session user, in case of erroneous invites
        inviters = session_user.was_invited.all().exclude(inviter=session_user).exclude(accept=True).exclude(ignore=True)

        context = {
            'user': session_user,
            'allfriends': accepted_invitations, # professional network
            'inviters': inviters,
        }
        return render(request, 'app_two/index.html', context)


# renders all_users.html - DONE
# displays users not in session user's network
# needs to exclude all users who are not invitees of session user
def all_users(request):
    print("This is all_users function in app2 views.py")
    user_id = request.session['user_id']
    session_user = User.objects.get(id=user_id)
    other_users = User.objects.exclude(id=user_id) # all users except session user

# this is a handy query, except it's not what I need for this particular function:
    users_invited = session_user.invited.all() # all users who have been invited by session user

# what I need is all users who have NOT been invited by the session user
# ** and all users who have not invited the session user **
# but I can't use the above query to exclude the invited ones, because it returns Invitation objects
# users not invited have no Invitation objects, only User objects


# this section finds all Users who have not sent an invitation to the session user

    all_users = User.objects.exclude(id=user_id) # all users except session user
    users_not_inviters = []
    for user in all_users:
        # checks all Invitation objects sent to the session user
        invite_check = Invitation.objects.filter(inviter=user).filter(invitee=session_user)
# gets the count (will be zero or 1) of invitations each user has sent to the session user)
        invite_check_count = invite_check.count()
        if invite_check_count == 0: # no invitation
            print(user.name, "has not invited", session_user.name)
            users_not_inviters.append(user) # creates an array of all users who didn't send invitations
        else: # one invitation (or more, in error)
            print(user.name, "has sent an invitation")
            # if the user has sent an invitation, but ignore = True
            for invite in invite_check:
                if invite.ignore == True:
                    print(invite.inviter.name, "ignore is True")
                    # puts user who sent ignored invitation back on all_users list
                    users_not_inviters.append(user)

    context = {
        'other_users': users_not_inviters,
    }
    return render(request, 'app_two/all_users.html', context)


# creates Invitation object when Connect button is clicked - DONE
def connect(request, user_id):
    this_invitee = User.objects.get(id=user_id)
    print("Invitee is:", this_invitee.name, this_invitee.id)
    this_inviter = User.objects.get(id=request.session['user_id'])
    print("Session user is", this_inviter.name, this_inviter.id)

    # send an invitation to selected User
    this_invitation = Invitation.objects.create(invitee=this_invitee, inviter=this_inviter)

    return redirect('app2:all_users')


# displays users.html - DONE
def users(request, user_id):
    print("This is users function in app2 views.py")
    context = {
        'user': User.objects.get(id=user_id),
    }
    return render(request, 'app_two/users.html', context)


# changes accept status to True - DONE
# id is for Invitation object
def accept(request, id):
    print("This is accept function in app2 views.py")
    this_invitation = Invitation.objects.get(id=id)
    this_invitation.accept = True
    this_invitation.save()
    print("ID is:", id, "id is", this_invitation.id)
    print(this_invitation.invitee.name, "is accepting an invitation from", this_invitation.inviter.name)
# The code above puts the invitee in the inviter's network
# The code below puts the inviter in the invitee's network, by creating a new Invitation object with accept field True
    this_inviter = User.objects.get(id=this_invitation.inviter.id)
    this_invitee = User.objects.get(id=this_invitation.invitee.id)
    reverse_connection = Invitation.objects.create(accept=True, invitee=this_inviter, inviter=this_invitee)

    return redirect('app2:index')


# changes ignore status to True - DONE
# id is for Invitation object
def ignore(request, id):
    print("This is ignore function in app2 views.py")
    this_invitation = Invitation.objects.get(id=id)
    this_invitation.ignore = True
    this_invitation.save()
    print(this_invitation.invitee.name, "is ignoring an invitation from", this_invitation.inviter.name)
    return redirect('app2:index')
