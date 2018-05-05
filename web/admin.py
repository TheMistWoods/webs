from django.contrib import admin

# 我的模型
from web.models import Topic,Entry

admin.site.register(Topic)
admin.site.register(Entry)
