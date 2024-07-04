from django import forms


class DeliveryForm(forms.Form):
    delivery_type = forms.CharField(label='', widget=forms.TextInput(attrs={'type': 'hidden', 'id': 'delivery', 'value': 'normal'}))


class DeliveryIdForm(forms.Form):
    delivery_Id = forms.CharField(label='', widget=forms.TextInput(attrs={'type': 'hidden', 'id': 'delivery_id'}), error_messages={'required' : 'لطفا یک آدرس را انتخاب کنید.'})


class DiscountCodeForm(forms.Form):
    DiscountCode = forms.CharField(label='', widget=forms.TextInput(attrs={"type": "text", "placeholder": "اعمال کد تخفیف", "class": "form-control search-input"}))
