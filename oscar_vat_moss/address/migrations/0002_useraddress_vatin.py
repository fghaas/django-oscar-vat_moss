# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import oscar_vat_moss.fields


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='vatin',
            field=oscar_vat_moss.fields.VATINField(help_text='Required if you are associated with a business registered for VAT in the European Union.', verbose_name='VAT Identification Number (VATIN)', blank=True),
        ),
    ]
