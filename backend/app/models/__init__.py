"""Import every model module so SQLAlchemy metadata (and Alembic
autogenerate) sees all tables. See handbook Chapter 14 for the schema
architecture these models implement."""
from app.models.animal import Animal, Flock, Herd  # noqa: F401
from app.models.farm import Farm, Location  # noqa: F401
from app.models.feed import FeedDistribution, FeedItem, FeedLot  # noqa: F401
from app.models.knowledge import Decision, KnowledgeObject, Recommendation  # noqa: F401
from app.models.observation import Observation  # noqa: F401
from app.models.production import EggCollection, MilkRecord  # noqa: F401
from app.models.user import User  # noqa: F401
