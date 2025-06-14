# Generated by Django 4.1.7 on 2023-05-16 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('central_api', '0022_enrollmentstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='conceptMedicationForm',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='central_api.conceptmedicationforms'),
        ),
        migrations.AlterField(
            model_name='medication',
            name='medicationGenericStrengths',
            field=models.ManyToManyField(null=True, to='central_api.medicationgenericstrength'),
        ),
        migrations.AlterField(
            model_name='medication',
            name='medicationInventory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='medication_medication_inventory', to='central_api.medicationinventory'),
        ),
    ]
