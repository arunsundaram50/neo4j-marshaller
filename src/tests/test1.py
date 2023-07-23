#!/usr/bin/env python3

"""
Using Neo4JMarshallerResource for automatically closing the marshaller
"""


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
