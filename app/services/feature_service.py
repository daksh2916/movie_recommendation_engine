from sqlalchemy.orm import Session
from app.schemas.database_schemas import FeatureConfig, FeatureSpace
from app.db.db import SessionLocal
import json
import uuid

def init_features():

    session: Session = SessionLocal()

    with open(r"C:\Users\anjut\Desktop\learn\recommendation_system\features.json", "r") as f:
        features_data = json.load(f)

    existing = session.query(FeatureConfig).first()
    if existing:
        session.close()
        return {"message": "Features already initialized."}
    
    config = FeatureConfig(id=uuid.uuid4(), version=1)
    session.add(config)
    session.commit()

    position = 0
    for category, items in features_data.items():
        for item in items:
            feature = FeatureSpace(
                id=uuid.uuid4(),
                config_id=config.id,
                category=category,
                name=item,
                position=position
            )
            session.add(feature)
            position += 1

    session.commit()
    session.close()
    return {"message": f"✅ FeatureConfig v1 created with {position} features"}
