from sqlalchemy_schemadisplay import create_schema_graph
from sqlalchemy import MetaData

graph = create_schema_graph(metadata=MetaData('sqlite:///data/database.db'))

graph.write_png('image_name.png')