from django.contrib.auth.models import User

def create_new_user(username, password, email="", first_name="", last_name=""):
    existing_users = User.objects.filter(username=username)

    if(existing_users.exists()):
        # The username is already taken, return None
        return None

    user = User.objects.create_user(username=username,
                         email=email,
                         password=password,
                         first_name=first_name)
    return user
