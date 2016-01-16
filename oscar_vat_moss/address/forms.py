from oscar.apps.address.forms import UserAddressForm as CoreUserAddressForm
from django.utils.translation import ugettext_lazy as _
from oscar_vat_moss import vat


class UserAddressForm(CoreUserAddressForm):

    class Meta(CoreUserAddressForm.Meta):
        fields = CoreUserAddressForm.Meta.fields + ['vatin']

    def clean(self):
        """Perform necessary form verification."""
        data = super(UserAddressForm, self).clean()
        # The superclass has taken care of individual field
        # verification, applying field validators to the form
        # input. Now we need to compare fields to each other.

        # Grab the interesting fields from the form
        company = data.get('line1')
        city = data.get('line4')
        country_code = data.get('country').code
        postcode = data.get('postcode')
        phone_number = data.get('phone_number')
        vatin = data.get('vatin')

        address_vat_rate = None
        phone_vat_rate = None

        # Do we have a VATIN? If so, the field validator will have
        # checked whether it is valid. Now we need to check whether it
        # agrees with the company name.
        if vatin:
            try:
                vat.lookup_vat_by_vatin(country_code, vatin, company)
            except Exception as e:
                message = _("VATIN does not match country: %s" % str(e))
                self.add_error('line1', message)
                self.add_error('vatin', message)

        # Get the tax rate for the city/country/postcode combination
        if city and country_code:
            try:
                address_vat_rate = vat.lookup_vat_by_city(country_code,
                                                          postcode,
                                                          city)
            except Exception as e:
                message = _("Unable to determine the "
                            "applicable VAT rate for "
                            "your address: %s" % str(e))
                # Flag all possibly faulty fields with the same
                # message
                self.add_error('line4', message)
                self.add_error('country', message)
                self.add_error('postcode', message)

        # Get the tax rate for the phone number
        if phone_number:
            try:
                phone_vat_rate = vat.lookup_vat_by_phone_number(phone_number,
                                                                country_code)
            except Exception as e:
                message = _("Unable to determine the "
                            "applicable VAT rate for "
                            "your phone number: %s" % str(e))
                # Flag all possibly faulty fields with the same
                # message
                self.add_error('country', message)
                self.add_error('phone_number', message)

        # Is one of the two rates still None? We can return now; no
        # need to check whether they agree (and confuse the user with
        # duplicate error messages)
        if None in [address_vat_rate, phone_vat_rate]:
            return

        # Does the address tax rate agree with the phone tax rate?
        if address_vat_rate != phone_vat_rate:
            message = _("Unable to determine the applicable VAT rate "
                        "based on address and phone information")
            self.add_error('line4', message)
            self.add_error('country', message)
            self.add_error('postcode', message)
            self.add_error('phone_number', message)
