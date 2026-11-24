from django.contrib.auth.decorators import user_passes_test

admin_required = user_passes_test(
    lambda u: u.is_authenticated and u.is_superuser,
    login_url='/login/'
)