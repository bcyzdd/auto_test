from django.contrib import admin

# Register your models here.
from MyApp.models import *

admin.site.register(DB_tucao) # admin.site.register() 是注册用的函数，里面写类名，注意是类名，并不是类本身，所以不要加()
admin.site.register(DB_home_href)
admin.site.register(DB_project)
admin.site.register(DB_apis)
admin.site.register(DB_apis_log)
admin.site.register(DB_cases)