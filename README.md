# neo4j_marshaller
`neo4j_marshaller` is a Python library that takes a Cypher query, executes it, and returns the resultset as a JSON object.


### Here is the GitHub repo:
- <https://github.com/arunsundaram50/neo4j_marshaller>

### Here is the pip command to install it:
```
pip install neo4j_marshaller
```


### Here’s a simple example of how you might use `neo4j_marshaller`:

```python
from neo4j_marshaller import Neo4JMarshallerResource
import json, sys, os

if __name__ == "__main__":

  username = os.environ['EMAIL_ADDRESS']
  cypher_query = """
      MATCH (user:ExplUser {name: $username})
      RETURN user
    """

  with Neo4JMarshallerResource() as nmr:
    userJson = nmr.get_one(cypher_query, username=username)
    json.dump(userJson, indent=2, fp=sys.stdout)

```

