from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from typing import List, Optional
from uuid import UUID

from .models import Clan
from .schemas import ClanCreate, ClanOut
from .deps import get_db
from .database import Base, engine

# Create tables on startup if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vertigo Clans API")


@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"status": "ok", "endpoints": ["/health", "/docs", "/clans"]}

@app.post("/clans", response_model=dict, status_code=201)
def create_clan(payload: ClanCreate, db: Session = Depends(get_db)):
    clan = Clan(name=payload.name, region=payload.region)
    db.add(clan)
    db.commit()
    db.refresh(clan)
    return {"id": str(clan.id), "message": "Clan created successfully."}

@app.get("/clans", response_model=List[ClanOut])
def list_clans(
    region: Optional[str] = Query(default=None, description="Filter by region code"),
    sort: Optional[str] = Query(default=None, description="Sort by created_at: asc|desc"),
    db: Session = Depends(get_db),
):
    stmt = select(Clan)
    if region:
        stmt = stmt.where(Clan.region == region)
    if sort:
        if sort.lower() == "asc":
            stmt = stmt.order_by(Clan.created_at)
        elif sort.lower() == "desc":
            stmt = stmt.order_by(desc(Clan.created_at))
    result = db.execute(stmt).scalars().all()
    return result

@app.get("/clans/{clan_id}", response_model=ClanOut)
def get_clan(clan_id: UUID, db: Session = Depends(get_db)):
    clan = db.get(Clan, clan_id)
    if not clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    return clan

@app.delete("/clans/{clan_id}", response_model=dict)
def delete_clan(clan_id: UUID, db: Session = Depends(get_db)):
    clan = db.get(Clan, clan_id)
    if not clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    db.delete(clan)
    db.commit()
    return {"message": "Clan deleted"}