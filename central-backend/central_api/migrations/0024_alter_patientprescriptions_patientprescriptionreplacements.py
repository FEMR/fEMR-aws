# Generated by Django 4.1.7 on 2023-05-16 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('central_api', '0023_alter_medication_conceptmedicationform_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientprescriptions',
            name='patientPrescriptionReplacements',
            field=models.ManyToManyField(null=True, to='central_api.patientprescriptionreplacement'),
        ),
    ]
