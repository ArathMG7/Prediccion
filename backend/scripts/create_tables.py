from database.db import engine
from database.models import Base

Base.metadata.create_all(engine)

print("Tablas creadas correctamente")