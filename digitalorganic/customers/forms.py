from allauth.account.forms import SignupForm
#from .models import CustomerModel


class SignupForm(SignupForm):

    first_name = forms.CharField(
        max_length=30, required=True
    )
    last_name = forms.CharField(
        max_length=30,
    )
    city = forms.CharField(max_length=75)
    country = forms.CharField(max_length=25)
   
    password = SetPasswordField(label=_("Password"))
    confirm_password = PasswordField(label=_("Password (again)"))
    confirmation_key = forms.CharField(max_length=40,
                                       required=False,
                                       widget=forms.HiddenInput())

    def clean(self):
        super(SignupForm, self).clean()
        if  "password" in self.cleaned_data \
                and "confirm_password" in self.cleaned_data:
            if self.cleaned_data["password"] \
                    != self.cleaned_data["confirm_password"]:
                raise forms.ValidationError(_("You must type the same password"
                                              " each time."))
        return self.cleaned_data

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        # TODO: Move into adapter `save_user` ?
        setup_user_email(request, user, [])
        return user
