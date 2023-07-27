# neo4j_marshaller
`neo4j_marshaller` is a Python library that takes a Cypher Query, executes it, and returns the resultset as a JSON object.

The idea is to 
- avoid the boiler-plate code that has to "interpret" the returned `BoltResultSet` in-order to use the results
- easily supply named parameters in the Cypher Query
- provide Driver-level, and Session-level resources so that `with` can be used and Neo4J resources are cleaned up automatically
- provide non-resource style calls for cases where `with` is not practical.

In both resource style and non-resource style usage, two functions are provided
- `get_one()`: substitute named paramers, execute query, fetch first  `BoltResultSet` row, and return it as an JSON object
- `get_all()`: substitute named paramers, execute query, fetch all `BoltResultSet` rows, and return it as an JSON array


### Here is the GitHub repo:
- <https://github.com/arunsundaram50/neo4j-marshaller>


### Here is the pip command to install it:
```
pip install neo4j-marshaller
```


## Following is a simple example of how you might use `neo4j_marshaller`:
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

## Following closes the driver manually, does not use session
```python
"""
Using Neo4JMarshaller for manually closing the marshaller.
This requires some care to call Neo4JMarshaller.close() to avoid resource leak.

Neo4JMarshaller methods are called in a try block so that Neo4JMarshaller.close() 
will be guarenteed to be called by putting it in the finally block.
"""


from neo4j_marshaller import Neo4JMarshaller
import json, sys, os

if __name__ == "__main__":

  username = os.environ['EMAIL_ADDRESS']
  cypher_query = """
      MATCH (u:ExplUser {name: $username})
      RETURN u
    """
  dir_list_query = """
      MATCH (d:ExplDir)
      RETURN d LIMIT 10
    """

  nm = Neo4JMarshaller()
  try:
    userJson = nm.get_one(cypher_query, username = username)
    print('-'*80)
    json.dump(userJson, indent=2, fp=sys.stdout)
      
    print('-'*80)
    dirListJson = nm.get_all(dir_list_query)
    json.dump(dirListJson, indent=2, fp=sys.stdout)

  finally:
    nm.close()
```

## Following closes the driver manually, uses session, closes it automatically
```python
"""
Using Neo4JMarshaller for manually obtaining a session and manually closing the marshaller
"""


from neo4j_marshaller import get_one, get_all, Neo4JMarshaller
import json, sys, os

if __name__ == "__main__":

  username = os.environ['EMAIL_ADDRESS']
  cypher_query = """
      MATCH (u:ExplUser {name: $username})
      RETURN u
    """
  dir_list_query = """
      MATCH (d:ExplDir)
      RETURN d LIMIT 10
    """

  nm = Neo4JMarshaller()
  with nm.getSession() as sess:
    userJson = get_one(sess, cypher_query, username = username)
    print('-'*80)
    json.dump(userJson, indent=2, fp=sys.stdout)
    
    print('-'*80)
    dirListJson = get_all(sess, dir_list_query)
    json.dump(dirListJson, indent=2, fp=sys.stdout)
  
  nm.close()
```


## Following closes driver and session automatically
```python

"""
Using Neo4JMarshallerResource and Session for automatically closing the marshaller and the session
"""


from neo4j_marshaller import get_one, get_all, Neo4JMarshallerResource
import json, sys, os

if __name__ == "__main__":

  username = os.environ['EMAIL_ADDRESS']
  user_query = """
      MATCH (u:ExplUser {name: $username})
      RETURN u
    """
  dir_list_query = """
      MATCH (d:ExplDir)
      RETURN d LIMIT 10
    """

  with Neo4JMarshallerResource() as nmr:
    with nmr.getSession() as sess:
      userJson = get_one(sess, user_query, username = username)
      print('-'*80)
      json.dump(userJson, indent=2, fp=sys.stdout)
      
      print('-'*80)
      dirListJson = get_all(sess, dir_list_query)
      json.dump(dirListJson, indent=2, fp=sys.stdout)
  
```