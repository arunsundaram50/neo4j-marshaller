#!/usr/bin/env python3

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

  nm = Neo4JMarshaller()
  with nm.getSession() as sess:
    userJson = get_one(sess, cypher_query, username = username)
    print('-'*80)
    json.dump(userJson, indent=2, fp=sys.stdout)
    
    print('-'*80)
    dirListJson = get_all(sess, """
      MATCH (d:ExplDir)
      RETURN d LIMIT 10
    """)
    json.dump(dirListJson, indent=2, fp=sys.stdout)
  
  nm.close()