#!/usr/bin/env python3

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

  nm = Neo4JMarshaller()
  try:
    userJson = nm.get_one(cypher_query, username = username)
    print('-'*80)
    json.dump(userJson, indent=2, fp=sys.stdout)
      
    print('-'*80)
    dirListJson = nm.get_all("""
      MATCH (d:ExplDir)
      RETURN d LIMIT 10
    """)
    json.dump(dirListJson, indent=2, fp=sys.stdout)

  finally:
    nm.close()

