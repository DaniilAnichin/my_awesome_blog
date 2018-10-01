from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Post, Tag


class PostAdminForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        Tag.objects.all(),
        widget=FilteredSelectMultiple('Tags', False),
        required=False,
    )

    class Meta:
        model = Post
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['tags'] = self.instance.tags.values_list('pk', flat=True)

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        if instance.pk:
            instance.tags.clear()
            instance.tags.add(*self.cleaned_data['tags'])
        return instance


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('views',)
    form = PostAdminForm


admin.site.register(Tag)
