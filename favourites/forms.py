from django import forms


#this class is to send a stop from the delete stop selector menu to the back end
class StopForm(forms.Form):
    name = forms.CharField(widget=forms.HiddenInput(), max_length = 200)
    #hidden_input = forms.CharField(widget=forms.HiddenInput(), initial="value")max_length=100)