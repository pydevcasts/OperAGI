from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('social_accounts', '0001_initial')]
    operations = [
        migrations.AddField(model_name='usersocialaccount', name='display_name', field=models.CharField(blank=True, default='', max_length=255)),
        migrations.AddField(model_name='usersocialaccount', name='external_url', field=models.URLField(blank=True, default='')),
        migrations.AddField(model_name='usersocialaccount', name='is_active', field=models.BooleanField(default=True)),
        migrations.AddField(model_name='usersocialaccount', name='connected_at', field=models.DateTimeField(auto_now_add=True)),
        migrations.AddField(model_name='usersocialaccount', name='updated_at', field=models.DateTimeField(auto_now=True)),
        migrations.AlterModelOptions(name='usersocialaccount', options={'ordering': ('social_account__provider', 'id')}),
    ]
