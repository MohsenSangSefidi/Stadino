from django import forms


class SearchForm(forms.Form):
    text = forms.CharField(label='', widget=forms.TextInput(attrs={"type":"text", "placeholder":"محصول خود را جستجو کنید", "class":"form-control search-input", "id":"search-input"}), error_messages={'required' : 'لطفا این کادر را پر کنید.'})