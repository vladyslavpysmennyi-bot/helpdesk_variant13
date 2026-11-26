from fastapi import FastAPI,HTTPException,WebSocket,BackgroundTasks
from pydantic import BaseModel
from sqlalchemy import select
from .db import Base,engine,Session
from .models import SLAEvent,ChatMessage
from datetime import datetime,timezone
app=FastAPI(title='SLA & Classification Service',version='1.0.0')
@app.on_event('startup')
async def startup():
 async with engine.begin() as conn: await conn.run_sync(Base.metadata.create_all)
class TicketIn(BaseModel): ticket_id:int; deadline:str
class ClassifyIn(BaseModel): title:str; description:str
class MessageIn(BaseModel): ticket_id:int; sender:str; body:str
@app.get('/health')
async def health(): return {'status':'ok'}
@app.post('/sla/track')
async def track(x:TicketIn):
 async with Session() as s: s.add(SLAEvent(ticket_id=x.ticket_id,deadline=x.deadline)); await s.commit()
 return {'ticket_id':x.ticket_id,'tracking':True}
@app.get('/sla/breaches')
async def breaches():
 async with Session() as s:
  events=(await s.scalars(select(SLAEvent))).all(); now=datetime.now(timezone.utc)
  return [{'ticket_id':e.ticket_id,'deadline':e.deadline,'breached':e.deadline < now.isoformat()} for e in events]
@app.post('/classify')
async def classify(x:ClassifyIn):
 text=(x.title+' '+x.description).lower(); priority='high' if any(w in text for w in ['терміново','авар','не працю','urgent','down']) else ('medium' if any(w in text for w in ['помил','error','проблем']) else 'low')
 category='Технічні проблеми' if any(w in text for w in ['помил','не працю','error','bug']) else ('Обліковий запис' if any(w in text for w in ['парол','вхід','login']) else 'Загальні питання')
 return {'category_suggestion':category,'priority_suggestion':priority,'confidence':0.65,'method':'keyword-rules'}
@app.post('/sla/escalate')
async def escalate(background_tasks:BackgroundTasks): background_tasks.add_task(lambda:None); return {'queued':True}
@app.websocket('/ws/tickets/{ticket_id}')
async def chat(ws:WebSocket,ticket_id:int):
 await ws.accept()
 try:
  while True:
   msg=await ws.receive_text()
   async with Session() as s: s.add(ChatMessage(ticket_id=ticket_id,sender='websocket-user',body=msg,created_at=datetime.now(timezone.utc).isoformat())); await s.commit()
   await ws.send_text(f'Повідомлення отримано: {msg}')
 except Exception: await ws.close()
