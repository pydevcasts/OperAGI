import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('content_generator', '0001_initial'),
        ('social_accounts', '0002_connection_metadata'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.AlterModelOptions(name='post', options={'ordering': ('-created_at',)}),
        migrations.AlterField(model_name='post', name='platform', field=models.CharField(choices=[('instagram', 'Instagram'), ('twitter', 'Twitter/X'), ('youtube', 'YouTube')], max_length=20, verbose_name='Platform')),
        migrations.AlterField(model_name='post', name='social_account', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='social_accounts.usersocialaccount')),
        migrations.AlterField(model_name='post', name='status', field=models.CharField(choices=[('draft', 'Draft'), ('generating_content', 'Generating Content'), ('content_generated', 'Content Generated'), ('ready_to_publish', 'Ready to Publish'), ('scheduled', 'Scheduled'), ('published', 'Published'), ('failed', 'Failed')], default='draft', max_length=24, verbose_name='Status')),
        migrations.AlterField(model_name='post', name='visual_idea', field=models.TextField(blank=True, default='', verbose_name='Visual Idea / Prompt')),
        migrations.AddField(model_name='post', name='generation_error', field=models.TextField(blank=True, default='')),
        migrations.AddField(model_name='post', name='language', field=models.CharField(choices=[('en', 'English'), ('fa', 'Persian')], default='en', max_length=2)),
        migrations.AddField(model_name='post', name='tone', field=models.CharField(default='professional', max_length=50)),
        migrations.AddIndex(model_name='post', index=models.Index(fields=['user', 'status'], name='content_gen_user_id_ff901b_idx')),
        migrations.AddIndex(model_name='post', index=models.Index(fields=['platform', 'created_at'], name='content_gen_platfor_eb3bd0_idx')),
        migrations.AlterField(model_name='generatedcontent', name='suggested_hashtags', field=models.TextField(blank=True, default='', verbose_name='Suggested Hashtags')),
        migrations.AddField(model_name='generatedcontent', name='description', field=models.TextField(blank=True, default='')),
        migrations.AddField(model_name='generatedcontent', name='hashtags', field=models.JSONField(blank=True, default=list)),
        migrations.AddField(model_name='generatedcontent', name='provider', field=models.CharField(default='local', max_length=40)),
        migrations.AddField(model_name='generatedcontent', name='provider_metadata', field=models.JSONField(blank=True, default=dict)),
        migrations.AddField(model_name='generatedcontent', name='title', field=models.CharField(blank=True, default='', max_length=255)),
        migrations.AddField(model_name='generatedcontent', name='updated_at', field=models.DateTimeField(auto_now=True)),
        migrations.CreateModel(name='Schedule', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('scheduled_for', models.DateTimeField(db_index=True)), ('timezone', models.CharField(default='UTC', max_length=64)),
            ('status', models.CharField(choices=[('queued', 'Queued'), ('processing', 'Processing'), ('published', 'Published'), ('cancelled', 'Cancelled'), ('failed', 'Failed')], db_index=True, default='queued', max_length=16)),
            ('task_id', models.CharField(blank=True, default='', max_length=255)), ('last_error', models.TextField(blank=True, default='')),
            ('created_at', models.DateTimeField(auto_now_add=True)), ('updated_at', models.DateTimeField(auto_now=True)), ('processed_at', models.DateTimeField(blank=True, null=True)),
            ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='schedule', to='content_generator.post')),
        ], options={'ordering': ('scheduled_for',)}),
        migrations.CreateModel(name='AnalyticsSnapshot', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('platform', models.CharField(choices=[('instagram', 'Instagram'), ('twitter', 'Twitter/X'), ('youtube', 'YouTube')], max_length=20)),
            ('impressions', models.PositiveBigIntegerField(default=0)), ('reach', models.PositiveBigIntegerField(default=0)), ('likes', models.PositiveBigIntegerField(default=0)),
            ('comments', models.PositiveBigIntegerField(default=0)), ('shares', models.PositiveBigIntegerField(default=0)), ('clicks', models.PositiveBigIntegerField(default=0)),
            ('views', models.PositiveBigIntegerField(default=0)), ('followers', models.PositiveBigIntegerField(default=0)), ('captured_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)), ('metadata', models.JSONField(blank=True, default=dict)),
            ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='analytics_snapshots', to='content_generator.post')),
            ('social_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='analytics_snapshots', to='social_accounts.usersocialaccount')),
            ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analytics_snapshots', to=settings.AUTH_USER_MODEL)),
        ], options={'ordering': ('-captured_at',)}),
        migrations.AddIndex(model_name='analyticssnapshot', index=models.Index(fields=['user', 'platform', 'captured_at'], name='content_gen_user_id_ec5743_idx')),
    ]
