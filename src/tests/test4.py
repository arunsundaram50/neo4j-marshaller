#!/usr/bin/env python3

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
  
