"""Seed script - realistic mixed-species Origami Farms test data, per
handbook Chapter 18 §18.4 ("test fixtures reflect the mixed-farm reality
Origami Farms actually has"). Includes one animal engineered to trigger
the health-decline-v1 correlation pattern, so a Recommendation is
demonstrable end-to-end without waiting on real usage.

Run with: python -m app.seed
"""
import uuid
from datetime import date, datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.animal import Animal, AnimalSpecies, Flock, FlockSpecies
from app.models.farm import Farm, Location
from app.models.feed import FeedDistribution, FeedItem, FeedLot, LotSource
from app.models.observation import Observation, ObservationQuality
from app.models.production import EggCollection, MilkDestination, MilkRecord
from app.models.production import MilkSession as MilkSessionEnum
from app.models.user import User, UserRole
from app.services.knowledge_engine import evaluate_entity

now = datetime.now(timezone.utc)


def days_ago(n: int, hour: int = 7) -> datetime:
    return (now - timedelta(days=n)).replace(hour=hour, minute=0, second=0, microsecond=0)


def seed(db: Session) -> None:
    farm = Farm(name="Origami Farms", country="Lebanon")
    db.add(farm)
    db.flush()

    barn = Location(farm_id=farm.id, name="Main Dairy Barn", location_type="barn")
    coop = Location(farm_id=farm.id, name="Poultry Coop", location_type="barn")
    pasture = Location(farm_id=farm.id, name="North Pasture", location_type="pasture")
    db.add_all([barn, coop, pasture])
    db.flush()

    owner = User(farm_id=farm.id, email="owner@origamifarms.io", full_name="Farm Owner", role=UserRole.OWNER, hashed_password=hash_password("password123"))
    manager = User(farm_id=farm.id, email="manager@origamifarms.io", full_name="Farm Manager", role=UserRole.MANAGER, hashed_password=hash_password("password123"))
    worker = User(farm_id=farm.id, email="worker@origamifarms.io", full_name="Ali (Worker)", role=UserRole.WORKER, hashed_password=hash_password("password123"))
    vet = User(farm_id=farm.id, email="vet@origamifarms.io", full_name="Dr. Nour (Vet)", role=UserRole.VETERINARIAN, hashed_password=hash_password("password123"))
    db.add_all([owner, manager, worker, vet])
    db.flush()

    # Mixed species animals (Constitution Principle 16 - Mixed Farm by Design)
    cow_healthy = Animal(farm_id=farm.id, tag_number="C-101", name="Bessie", species=AnimalSpecies.COW, breed="Holstein", sex="female", birth_date=date(2022, 3, 1), current_location_id=barn.id)
    cow_declining = Animal(farm_id=farm.id, tag_number="C-744", name=None, species=AnimalSpecies.COW, breed="Holstein", sex="female", birth_date=date(2021, 6, 15), current_location_id=barn.id)
    sheep = Animal(farm_id=farm.id, tag_number="S-201", species=AnimalSpecies.SHEEP, sex="female", birth_date=date(2023, 1, 10), current_location_id=pasture.id)
    goat = Animal(farm_id=farm.id, tag_number="G-301", species=AnimalSpecies.GOAT, sex="female", birth_date=date(2022, 11, 20), current_location_id=pasture.id)
    horse = Animal(farm_id=farm.id, tag_number="H-401", name="Amir", species=AnimalSpecies.HORSE, sex="male", birth_date=date(2019, 5, 5), current_location_id=pasture.id)
    db.add_all([cow_healthy, cow_declining, sheep, goat, horse])
    db.flush()

    chicken_flock = Flock(farm_id=farm.id, name="Layer Flock A", species=FlockSpecies.CHICKEN, bird_count=150, location_id=coop.id)
    duck_flock = Flock(farm_id=farm.id, name="Duck Flock A", species=FlockSpecies.DUCK, bird_count=40, location_id=coop.id)
    turkey_flock = Flock(farm_id=farm.id, name="Turkey Flock A", species=FlockSpecies.TURKEY, bird_count=25, location_id=coop.id)
    db.add_all([chicken_flock, duck_flock, turkey_flock])
    db.flush()

    # Feed
    hay = FeedItem(farm_id=farm.id, name="Alfalfa Hay", unit="kg")
    layer_mash = FeedItem(farm_id=farm.id, name="Layer Mash", unit="kg")
    db.add_all([hay, layer_mash])
    db.flush()

    hay_lot = FeedLot(farm_id=farm.id, feed_item_id=hay.id, source=LotSource.PURCHASE, quantity_received=500.0, unit_cost=0.35, received_at=days_ago(10))
    mash_lot = FeedLot(farm_id=farm.id, feed_item_id=layer_mash.id, source=LotSource.PURCHASE, quantity_received=200.0, unit_cost=0.5, received_at=days_ago(10))
    db.add_all([hay_lot, mash_lot])
    db.flush()

    for n in range(10, 0, -1):
        db.add(FeedDistribution(farm_id=farm.id, feed_lot_id=hay_lot.id, entity_type="Animal", entity_id=cow_healthy.id, quantity=22.0, distributed_at=days_ago(n), recorded_by=worker.id))
        # cow_declining's feed intake declines over the last 3 days (health-decline-v1 signal)
        qty = 20.0 if n > 3 else 16.5
        db.add(FeedDistribution(farm_id=farm.id, feed_lot_id=hay_lot.id, entity_type="Animal", entity_id=cow_declining.id, quantity=qty, distributed_at=days_ago(n), recorded_by=worker.id))
        db.add(FeedDistribution(farm_id=farm.id, feed_lot_id=mash_lot.id, entity_type="Flock", entity_id=chicken_flock.id, quantity=18.0, distributed_at=days_ago(n), recorded_by=worker.id))
    db.commit()

    # Milk history: cow_healthy stable ~28L/day; cow_declining drops in the last 3 days
    for n in range(10, 0, -1):
        db.add(MilkRecord(farm_id=farm.id, animal_id=cow_healthy.id, session=MilkSessionEnum.AM, volume_liters=14.0, destination=MilkDestination.SALE, recorded_at=days_ago(n, 6), recorded_by=worker.id))
        db.add(MilkRecord(farm_id=farm.id, animal_id=cow_healthy.id, session=MilkSessionEnum.PM, volume_liters=14.0, destination=MilkDestination.SALE, recorded_at=days_ago(n, 18), recorded_by=worker.id))

        volume = 13.5 if n > 3 else 10.0
        db.add(MilkRecord(farm_id=farm.id, animal_id=cow_declining.id, session=MilkSessionEnum.AM, volume_liters=volume, destination=MilkDestination.SALE, recorded_at=days_ago(n, 6), recorded_by=worker.id))
        db.add(MilkRecord(farm_id=farm.id, animal_id=cow_declining.id, session=MilkSessionEnum.PM, volume_liters=volume, destination=MilkDestination.SALE, recorded_at=days_ago(n, 18), recorded_by=worker.id))
    db.commit()

    # Companion Observations for milk_yield (mirrors what the API does automatically - Ch.7 RULE-DAIRY-101)
    for n in range(10, 0, -1):
        db.add(Observation(farm_id=farm.id, entity_type="Animal", entity_id=cow_healthy.id, observation_type="milk_yield", value_numeric=28.0, unit="L", quality=ObservationQuality.B_COUNTED, confidence=0.8, observer_id=worker.id, observed_at=days_ago(n), source="worker"))
        db.add(Observation(farm_id=farm.id, entity_type="Animal", entity_id=cow_healthy.id, observation_type="feed_intake", value_numeric=22.0, unit="kg", quality=ObservationQuality.B_COUNTED, confidence=0.8, observer_id=worker.id, observed_at=days_ago(n), source="worker"))

        milk_volume = 27.0 if n > 3 else 20.0
        feed_qty = 20.0 if n > 3 else 16.5
        db.add(Observation(farm_id=farm.id, entity_type="Animal", entity_id=cow_declining.id, observation_type="milk_yield", value_numeric=milk_volume, unit="L", quality=ObservationQuality.B_COUNTED, confidence=0.8, observer_id=worker.id, observed_at=days_ago(n), source="worker"))
        db.add(Observation(farm_id=farm.id, entity_type="Animal", entity_id=cow_declining.id, observation_type="feed_intake", value_numeric=feed_qty, unit="kg", quality=ObservationQuality.B_COUNTED, confidence=0.8, observer_id=worker.id, observed_at=days_ago(n), source="worker"))
    db.commit()

    # Health signs for cow_declining in the last 2 days (Ch.4.4.3 worked example)
    db.add(Observation(farm_id=farm.id, entity_type="Animal", entity_id=cow_declining.id, observation_type="temperature", value_numeric=39.7, unit="C", quality=ObservationQuality.A_INSTRUMENT, confidence=0.95, observer_id=worker.id, observed_at=days_ago(1, 8), source="worker"))
    db.add(Observation(farm_id=farm.id, entity_type="Animal", entity_id=cow_declining.id, observation_type="appetite", value_text="reduced", quality=ObservationQuality.C_HUMAN_OBSERVED, confidence=0.55, observer_id=worker.id, observed_at=days_ago(1, 8), source="worker", notes="Left feed largely untouched this morning."))
    db.commit()

    # Egg collections: chicken flock has a genuine decline in the last 3 days
    for n in range(10, 0, -1):
        total = 130 if n > 3 else 95
        db.add(EggCollection(farm_id=farm.id, flock_id=chicken_flock.id, total_eggs=total, broken_eggs=3, consumed=10, sold=total - 20, hatching=7, collected_at=days_ago(n, 9), recorded_by=worker.id))
        db.add(Observation(farm_id=farm.id, entity_type="Flock", entity_id=chicken_flock.id, observation_type="egg_total", value_numeric=float(total), unit="eggs", quality=ObservationQuality.B_COUNTED, confidence=0.8, observer_id=worker.id, observed_at=days_ago(n, 9), source="worker"))

        db.add(EggCollection(farm_id=farm.id, flock_id=duck_flock.id, total_eggs=28, broken_eggs=1, consumed=5, sold=20, hatching=2, collected_at=days_ago(n, 9), recorded_by=worker.id))
    db.commit()

    # Evaluate the knowledge engine now that history exists, so recommendations are ready immediately.
    evaluate_entity(db, farm_id=farm.id, entity_type="Animal", entity_id=cow_declining.id)
    evaluate_entity(db, farm_id=farm.id, entity_type="Flock", entity_id=chicken_flock.id)

    print("Seed complete.")
    print(f"Farm ID: {farm.id}")
    print("Login as: owner@origamifarms.io / manager@origamifarms.io / worker@origamifarms.io / vet@origamifarms.io (password: password123)")


if __name__ == "__main__":
    session = SessionLocal()
    try:
        seed(session)
    finally:
        session.close()
