from django import forms

class NetworkForm(forms.Form):
    DHCP_CHOICES = [('DHCPv4', 'DHCPv4'), ('DHCPv6', 'DHCPv6')]
    mac_address = forms.CharField(label='MAC Address', max_length=17)
    dhcp_version = forms.ChoiceField(choices=DHCP_CHOICES)
