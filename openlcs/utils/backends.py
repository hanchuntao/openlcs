from django.contrib.auth.backends import RemoteUserBackend
from django.conf import settings


class ModAuthKerbBackend(RemoteUserBackend):
    """
    mod_auth_kerb modules authorization backend for OpenLCS.
    """
    def configure_user(self, user):
        # Get triggered upon user creation.
        user.email = user.username + '@' + settings.EMAIL_REALM.lower()
        nodes = settings.WORKER_NODES
        user.set_unusable_password()
        for node in nodes:
            # FIXME: the max length of the builtin user model is 30.
            # Thus longer usernames get truncated under ModAuthKerbBackend.
            if len(node) > 30:
                node = node[:30]
            # Grant permissions for worker nodes automatically
            # FIXME: sort out needed permissions for worker nodes.
            # Apply them instead of simply add to 'reviewers' group.
            if node == user.username:
                # Activate worker nodes automatically.
                user.is_active = True
                # FIXME: Comment it out first, because we don't have
                #  permission management now
                # from django.contrib.auth.models import Group
                # group_name = 'Reviewers'
                # g = Group.objects.get(name=group_name)
                # g.user_set.add(user)
        user.save()
        return user

    def clean_username(self, username):
        """
        Performs any cleaning on the 'username' prior to using it to get or
        create the user object. Returns the cleaned username.
        """
        username = username.replace('@' + settings.EMAIL_REALM, '')
        username_tuple = username.split('/')
        if len(username_tuple) > 1:
            username = username_tuple[1]
        return len(username) > 30 and username[:30] or username
