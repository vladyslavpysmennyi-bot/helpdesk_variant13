import json, httpx
from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from rest_framework import viewsets,permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Ticket,Comment,KnowledgeArticle,Customer,Agent,SLAPolicy
from .serializers import TicketSerializer,CommentSerializer,ArticleSerializer
class IsTicketParticipant(permissions.BasePermission):
 def has_object_permission(self,request,view,obj): return request.user.is_staff or obj.customer.user_id==request.user.id or (obj.agent and obj.agent.user_id==request.user.id)
class TicketViewSet(viewsets.ModelViewSet):
 serializer_class=TicketSerializer; permission_classes=[permissions.IsAuthenticated,IsTicketParticipant]; filterset_fields=['status','priority','agent']; search_fields=['title','description']; ordering_fields=['created_at','deadline']
 def get_queryset(self):
  qs=Ticket.objects.select_related('customer__user','agent__user','category','priority').prefetch_related('tags','comments')
  return qs if self.request.user.is_staff or Agent.objects.filter(user=self.request.user).exists() else qs.filter(customer__user=self.request.user)
 def perform_create(self,serializer):
  customer,_=Customer.objects.get_or_create(user=self.request.user); data={'title':serializer.validated_data.get('title',''),'description':serializer.validated_data.get('description','')}
  try:
   r=httpx.post(settings.FASTAPI_URL+'/classify',json=data,timeout=2); r.raise_for_status()
   # Suggestion only; category and priority are still chosen from Django's catalogue.
  except Exception: pass
  serializer.save(customer=customer)
 @action(detail=True,methods=['post'])
 def assign(self,request,pk=None):
  ticket=self.get_object(); agent=Agent.objects.get(user_id=request.data['agent_user_id']); ticket.agent=agent; ticket.save(); return Response(TicketSerializer(ticket).data)
 @action(detail=True,methods=['post'])
 def transition(self,request,pk=None):
  ticket=self.get_object(); allowed={'new':['working'],'working':['waiting','resolved'],'waiting':['working','resolved'],'resolved':['closed','working'],'closed':[]}
  target=request.data.get('status')
  if target not in allowed.get(ticket.status,[]): return Response({'detail':'Недопустимий перехід статусу'},status=400)
  ticket.status=target
  if target=='resolved': ticket.resolved_at=timezone.now()
  ticket.save(); return Response(TicketSerializer(ticket).data)
 @action(detail=False,methods=['get'])
 def overdue(self,request): return Response(TicketSerializer(self.get_queryset().filter(deadline__lt=timezone.now()).exclude(status__in=['resolved','closed']),many=True).data)
class CommentViewSet(viewsets.ModelViewSet):
 serializer_class=CommentSerializer
 def get_queryset(self):
  qs=Comment.objects.select_related('ticket','author')
  return qs.filter(ticket__in=TicketViewSet().get_queryset())
 def perform_create(self,serializer): serializer.save(author=self.request.user)
class ArticleViewSet(viewsets.ModelViewSet):
 serializer_class=ArticleSerializer; permission_classes=[permissions.IsAuthenticatedOrReadOnly]; search_fields=['title','body']; queryset=KnowledgeArticle.objects.filter(published=True)
def home(request): return render(request,'core/home.html')
