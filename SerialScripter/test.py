from sqlalchemy_schemadisplay import create_schema_graph
from sqlalchemy import MetaData

graph = create_schema_graph(metadata=MetaData('sqlite:///data/database.db'),rankdir="LR")
graph.set('scale', 20)
graph.write_png('image_name.png')
