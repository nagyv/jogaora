from django import forms
from .models import Participant, Session


class SessionForm(forms.ModelForm):

    class Meta:
        model = Session
        fields = ['name']


class ParticipantListForm(forms.Form):

    session = forms.ModelChoiceField(
        queryset=Session.objects.all(),
        widget=forms.HiddenInput
    )
    participant = forms.ModelChoiceField(
        queryset=Participant.objects.all(),
        empty_label="New Participant",
        required=False
    )
    name = forms.CharField(max_length=255, required=False)
    email = forms.EmailField(required=False)
    paid = forms.DecimalField(required=False, max_digits=7, decimal_places=2)

    def clean(self):
        # TODO oran: fix this
        cleaned_data = super(ParticipantListForm, self).clean()
        if getattr(cleaned_data['participant'], 'active_season_ticket', False):
            return cleaned_data
        elif cleaned_data['participant'] and cleaned_data['paid']:
            return cleaned_data

        if not cleaned_data['name']:
            msg = u"The name should have filled if no participant is selected."
            self._errors["name"] = self.error_class([msg])
        if not cleaned_data['paid']:
            msg = u"The paid should have filled if participant does not have a valid season ticket."
            self._errors["paid"] = self.error_class([msg])

        return cleaned_data

    def save(self):
        if not self.cleaned_data['participant']:
            participant = Participant.objects.create(
                name=self.cleaned_data['name'],
                email=self.cleaned_data['email']
            )
        else:
            participant = self.cleaned_data['participant']
        return self.cleaned_data['session'].participant_add(participant, paid=self.cleaned_data['paid'])
