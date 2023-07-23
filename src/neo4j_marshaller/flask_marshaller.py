from flask import jsonify

def send_json(j):
  return jsonify(j)


def send_all(sess, cql, **kwargs):
  return jsonify(get_all_cql_result_as_json(sess, cql, **kwargs))


def send_one(sess, cql, **kwargs):
  try:
    node_objs = get_one_cql_result_as_json(sess, cql, **kwargs)
    if not node_objs:
      node_objs = {}
    return jsonify(node_objs)
  except:
    err = traceback.format_exc(chain=True)
    print(err, file=sys.stdout)
    return jsonify({
      "err": err
    }), 500
