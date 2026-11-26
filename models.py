from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,DateTime,Text
from .db import Base
class SLAEvent(Base):
 __tablename__='sla_events'; id:Mapped[int]=mapped_column(primary_key=True); ticket_id:Mapped[int]=mapped_column(index=True); deadline:Mapped[str]=mapped_column(String(64)); status:Mapped[str]=mapped_column(String(20),default='tracking')
class ChatMessage(Base):
 __tablename__='chat_messages'; id:Mapped[int]=mapped_column(primary_key=True); ticket_id:Mapped[int]=mapped_column(index=True); sender:Mapped[str]=mapped_column(String(100)); body:Mapped[str]=mapped_column(Text); created_at:Mapped[str]=mapped_column(String(64))
