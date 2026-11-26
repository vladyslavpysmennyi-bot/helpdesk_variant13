from rest_framework import serializers
from .models import Ticket,Comment,KnowledgeArticle
class TicketSerializer(serializers.ModelSerializer):
 class Meta: model=Ticket; fields='__all__'
class CommentSerializer(serializers.ModelSerializer):
 class Meta: model=Comment; fields='__all__'
class ArticleSerializer(serializers.ModelSerializer):
 class Meta: model=KnowledgeArticle; fields='__all__'
