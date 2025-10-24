from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from datetime import date
from pydantic import BaseModel
from typing import List
from database import SessionLocal, Event, Participant
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Sistem Event Kampus",
    description="Sistem manajemen event kampus dengan pendaftaran peserta"
)

# Mount static files (for frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root redirect info
@app.get("/")
def read_root():
    return {"message": "Selamat datang di Sistem Event Kampus! Akses frontend di /static/index.html"}

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication for admin
def verify_admin_token(x_token: str = Header(...)):
    if x_token != "santo_admin":
        raise HTTPException(status_code=403, detail="Admin access required")

# Pydantic Models
class EventCreate(BaseModel):
    title: str
    date: date
    location: str
    quota: int

class EventResponse(EventCreate):
    id: int
    class Config:
        orm_mode = True

class ParticipantCreate(BaseModel):
    name: str
    email: str
    event_id: int

class ParticipantResponse(BaseModel):
    id: int
    name: str
    email: str
    event_id: int
    class Config:
        orm_mode = True

# --- Event Endpoints (Admin-only for write operations) ---

@app.get("/events", response_model=List[EventResponse])
def get_events(db: Session = Depends(get_db)):
    return db.query(Event).all()

@app.post("/events", response_model=EventResponse, dependencies=[Depends(verify_admin_token)])
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.put("/events/{event_id}", response_model=EventResponse, dependencies=[Depends(verify_admin_token)])
def update_event(event_id: int, event: EventCreate, db: Session = Depends(get_db)):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event gak ada")
    for key, value in event.dict().items():
        setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.delete("/events/{event_id}", dependencies=[Depends(verify_admin_token)])
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event gak ada")
    db.delete(db_event)
    db.commit()
    return {"message": "Event dihapus"}

# --- Participant Endpoints ---

@app.post("/register", response_model=ParticipantResponse)
def register_participant(participant: ParticipantCreate, db: Session = Depends(get_db)):
    # Check if event exists
    event = db.query(Event).filter(Event.id == participant.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event gak ada")
    
    # Check quota
    current_count = db.query(Participant).filter(Participant.event_id == participant.event_id).count()
    if current_count >= event.quota:
        raise HTTPException(status_code=400, detail="Partisipan Event udah penuh")

    # Create participant
    db_participant = Participant(**participant.dict())
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant

@app.get("/participants", response_model=List[ParticipantResponse])
def get_participants(db: Session = Depends(get_db)):
    return db.query(Participant).all()