# Generated by Django 2.2.16 on 2021-07-09 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='djangocms_comments.Comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='requires_attention',
            field=models.CharField(blank='', choices=[('spam', 'Spam'), ('edited', 'Edited'), ('created', 'Created')], max_length=16),
        ),
        migrations.AlterField(
            model_name='comments',
            name='cmsplugin_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='djangocms_comments_comments', serialize=False, to='cms.CMSPlugin'),
        ),
    ]
