import datetime
import random

from app import app
from faker import Faker
from models import Campsite, Park, db

fake = Faker()

with app.app_context():
    print("Clearing db...")

    Park.query.delete()
    Campsite.query.delete()

    print("Seeding parks...")

    parks = []

    park_names = [
        "Quartz Lake Recreation Area",
        "Eagle Trail Recreation Area",
        "Castlewood Canyon State Park",
        "State Forest State Park",
    ]

    spring_start, spring_end = datetime.date(2024, 3, 20), datetime.date(2024, 5, 15)
    fall_start, fall_end = datetime.date(2024, 9, 17), datetime.date(2024, 11, 10)

    for name in park_names:
        park = Park(
            name=name,
            address=fake.address(),
            entrance_fee=round(random.uniform(13.99, 25.00), 2),
            has_trails=random.choice((True, False)),
            has_RV_cleanout=random.choice((True, False)),
            begin_camping_season=fake.date_between(spring_start, spring_end),
            end_camping_season=fake.date_between(fall_start, fall_end),
        )
        parks.append(park)
    db.session.add_all(parks)
    db.session.commit()

    print("Seeding campsites...")

    sites = []

    for _ in range(10):
        site = Campsite(
            park_id=random.choice(parks).id,
            max_capacity=random.randint(2, 10),
            type=random.choice(("tent", "RV")),
            site_fee=round(random.uniform(9.99, 19.99), 2),
            has_water=random.choice((True, False)),
            has_bathroom=random.choice((True, False)),
            has_grill=random.choice((True, False)),
        )
        sites.append(site)
    db.session.add_all(sites)
    db.session.commit()

    print("Done seeding...")
