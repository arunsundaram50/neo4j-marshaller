import traceback, sys, neo4j, json, hashlib
from datetime import datetime
DEBUG = False


def get_hash(content):
  hasher = hashlib.md5()
  hasher.update(str.encode(content))
  return 'xx'+hasher.hexdigest()


def get_all(sess, cql, **kwargs):
  if DEBUG:
    print('-'*80)
    print(cql)
    for key in kwargs:
      print(f"{key}={kwargs[key]}")
    sys.stdout.flush()
  nodes = sess.run(cql, **kwargs)
  node_objs = []
  for node in nodes:
    serialized = serialize_node_as_json(node)
    node_objs.append(serialized)
  if DEBUG:
    json.dump(node_objs, indent=2, fp=sys.stdout)
    print("")
    sys.stdout.flush()
  return node_objs


def cql_run(sess, cql, **kwargs):
  if DEBUG:
    print('-'*80)
    print(cql)
    for key in kwargs:
      print(f"{key}={kwargs[key]}")
    sys.stdout.flush()
  res = sess.run(cql, **kwargs)
  if DEBUG:
    print(res)
    print("")
    sys.stdout.flush()
  return res


def get_one(sess, cql, **kwargs):
  if DEBUG:
    print('-'*80)
    print(cql)
    for key in kwargs:
      print(f"{key}={kwargs[key]}")
    sys.stdout.flush()
  nodes = sess.run(cql, **kwargs)
  for node in nodes:
    serialized = serialize_node_as_json(node)
    if DEBUG:
      json.dump(serialized, indent=2, fp=sys.stdout)
      print("")
      sys.stdout.flush()
    return serialized
  return None


def serialize_relation_as_json(rel):
  ret = {}
  if 'id' in rel:
    ret['id'] = rel.id
  ret['name'] = type(rel).__name__
  return ret


def serialize_node_as_json(node) -> dict|list|float|None:
  node_type = type(node)
  if hasattr(neo4j, 'BoltStatementResult') and node_type == neo4j.BoltStatementResult:
    records = []
    for item in list(node.records()):
      records.append(serialize_node_as_json(item))
    return records
  elif node_type == neo4j.Record:
    my_record = {}
    for key in node.keys():
      my_record[key] = serialize_node_as_json(node.get(key))
    return my_record
  elif node_type == dict:
    my_dict = {}
    for key in node:
      my_dict[key] = serialize_node_as_json(node[key])
    return my_dict
  elif (hasattr(neo4j, 'graph') and node_type == neo4j.graph.Node) or \
    (hasattr(neo4j, 'types') and node_type == neo4j.types.graph.Node):
    # labels = list(node.labels)
    my_dict = {}
    for key in node.keys():
      my_dict[key] = serialize_node_as_json(node.get(key))
    return my_dict
  elif node_type == int or node_type == float:
    return node
  elif node_type == str:
    return node
  elif node_type == bool:
    return node
  elif str(node_type).startswith("<class 'abc."):
    return serialize_relation_as_json(node)
  elif node_type == list:
    my_items = []
    for item in node:
      my_items.append(serialize_node_as_json(item))
    return my_items
  elif str(node_type) == "<class 'neotime.DateTime'>":
    return datetime.timestamp(node)
  elif str(node_type) == "<class 'NoneType'>":
    return None
  else:
    print(f"Don't know how to handle: {node_type}")
    return None
