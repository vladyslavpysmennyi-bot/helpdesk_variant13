from django.contrib import admin
from .models import *
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin): list_display=('id','title','customer','agent','priority','status','deadline'); list_filter=('status','priority','category'); search_fields=('title','description'); autocomplete_fields=('customer','agent');
@admin.register(KnowledgeArticle)
class ArticleAdmin(admin.ModelAdmin): list_display=('title','category','published'); search_fields=('title','body'); list_filter=('published','category')
admin.site.register([Customer,Agent,Category,Priority,Tag,SLAPolicy,Comment,Attachment,CSAT])
