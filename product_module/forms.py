from django import forms


class CommentForm(forms.Form):
    rating1 = forms.CharField(label='', widget=forms.TextInput(
        attrs={"type": "radio", "id": "star1", "name": "rating", "value": "1"}), required=False)
    rating2 = forms.CharField(label='', widget=forms.TextInput(
        attrs={"type": "radio", "id": "star2", "name": "rating", "value": "2"}), required=False)
    rating3 = forms.CharField(label='', widget=forms.TextInput(
        attrs={"type": "radio", "id": "star3", "name": "rating", "value": "3"}), required=False)
    rating4 = forms.CharField(label='', widget=forms.TextInput(
        attrs={"type": "radio", "id": "star4", "name": "rating", "value": "4"}), required=False)
    rating5 = forms.CharField(label='', widget=forms.TextInput(
        attrs={"type": "radio", "id": "star5", "name": "rating", "value": "5"}), required=False)
    parent = forms.CharField(label='', widget=forms.TextInput(attrs={"type": "hidden", "id": "parent", "value": "0"}), required=False)
    text = forms.CharField(label='', widget=forms.Textarea(attrs={"class": "form-control pt-3", "id": "floatingTextarea2", "style": "height: 150px"}))


class PriceRangeForm(forms.Form):
    start = forms.CharField(label='', widget=forms.TextInput(attrs={"type":"number", "name":"",  "min":"10000", "class":"form-control input-range-filter", "placeholder":"از 1500000"}))
    end = forms.CharField(label='', widget=forms.TextInput(attrs={"type":"number", "name":"",  "min":"10000", "max":"1500000", "class":"form-control input-range-filter", "placeholder":"از 3000000"}))


class CatgoryForm(forms.Form):
    catgory = forms.ChoiceField(
        choices=[('کتاب-کمک-درسی', 'کتاب کمک درسی'), ('کتاب-عمومی', 'کتاب عمومی'), ('کتاب-کودک-و-نوجوان', 'کتاب کودک و نوجوان'), ('کتاب-دانشگاهی', 'کتاب دانشگاهی')],
        widget=forms.RadioSelect
    )