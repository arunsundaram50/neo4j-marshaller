# neo4j_marshaller
`neo4j_marshaller` is a Python library that takes a Cypher Query, executes it, and returns the resultset as a JSON object.
The idea is to 
- avoid the boiler-plate code that has to "interpret" the returned `BoltResultSet` in-order to use the results
- easily supply named parameters in the Cypher Query
- `get_one()`: pick one row from returned `BoltResultSet` and return it as an object
- `get_all()`: treat the `BoltResultSet` and return it as an array 


### Here is the GitHub repo:
- <https://github.com/arunsundaram50/neo4j-marshaller>


### Here is the pip command to install it:
```
pip install neo4j-marshaller
```


### Here’s a simple example of how you might use `neo4j_marshaller`:
```python
from neo4j_marshaller import Neo4JMarshallerResource
import json, sys, os

if __name__ == "__main__":

  email_address = os.environ['EMAIL_ADDRESS']
  cypher_query = """
      MATCH (user:ExplUser {name: $username})
      RETURN user
    """

  with Neo4JMarshallerResource() as nmr:
    userJson = nmr.get_one(cypher_query, username=email_address)
    json.dump(userJson, indent=2, fp=sys.stdout)
```

