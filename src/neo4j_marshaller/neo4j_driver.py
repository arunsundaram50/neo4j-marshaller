
import traceback, os, json, traceback
from neo4j import GraphDatabase, basic_auth
import neo4j_marshaller


class Neo4JMarshallerResource(object):
  nm = None
  def __enter__(self, uri_or_filename=None, userid=None, password=None):
    self.nm = Neo4JMarshaller(uri_or_filename, userid, password)
    return self
  
  def __exit__(self, exc_type, exc_value, traceback):
    if not self.nm:
      raise ValueError("Neo4JMarshaller was not constructed properly")
    self.nm.close()

  def get_one(self, csql, **kwargs):
    if not self.nm:
      raise ValueError("Neo4JMarshaller was not constructed properly")
    return self.nm.get_one(csql, **kwargs)

  def get_all(self, csql, **kwargs):
    if not self.nm:
      raise ValueError("Neo4JMarshaller was not constructed properly")
    return self.nm.get_all(csql, **kwargs)
  
  def execute(self, csql, **kwargs):
    if not self.nm:
      raise ValueError("Neo4JMarshaller was not constructed properly")
    return self.nm.cql_run(csql, **kwargs)
  
  def getSession(self):
    if not self.nm:
      raise ValueError("Neo4JMarshaller was not constructed properly")
    return self.nm.getSession()


class Neo4JMarshaller(object):
  """
    Calling options:
      Neo4JMarshaller()
      Neo4JMarshaller(configFilename)
      Neo4JMarshaller(uri, userid, password)
  """
  def __init__(self, uri_or_filename=None, userid=None, password=None):

    if not uri_or_filename:
      uri_or_filename = f"~/.neo4j.json"
    
    if uri_or_filename and not userid: # uri_or_filename is a filename
      filename = os.path.expanduser(uri_or_filename)
      if os.path.exists(filename):
        with open(filename) as fp:
          configJson = json.load(fp)
          n4j = configJson['neo4j']
          self._uri = n4j['uri']
          self._userid = n4j['userid']
          self._password = n4j['password']
      else:
        # Nothing passed, and defaul config file doesn't exist. Make things up and try!
        self._uri = 'bolt://localhost:7687'
        self._userid = 'neo4j'
        self._password = os.environ['NEO4J_PASSWORD']
    else:
      self._uri = uri_or_filename # it's an URL
      self._userid = userid
      self._password = password

    self._driver = None
    self.retryConnection()

  @classmethod
  def create_default_driver(cls):
    with open(os.path.expanduser(f"~/.neo4j.json")) as fp:
      configJson = json.load(fp)
      n4j = configJson['neo4j']
      nm = Neo4JMarshaller(n4j['uri'], n4j['userid'], n4j['password'])
    return nm

  def retryConnection(self):
    uri = self._uri
    userid = self._userid
    password = self._password
    try:
      if(password.startswith('$')):
        password = os.environ[password[1:]]
        if password == None:
          raise ValueError(f"Environment variable {password[1:]} is not set")
      self._driver = GraphDatabase.driver(uri, auth=basic_auth(userid, password), encrypted = False)
      TEST_CQL = """
        MATCH(n) RETURN n LIMIT 1
      """
      with self._driver.session() as sess:
        res = neo4j_marshaller.get_one(sess, TEST_CQL)
    except:
      traceback.print_exc()
      raise ValueError(f"Error connecting to {uri}, userid {userid}, password = *******")

  def getDriver(self):
    if self._driver == None:
      self.retryConnection()
    return self._driver
  
  def getSession(self):
    return self.getDriver().session()

  def close(self):
    if self._driver:
      self._driver.close()
  
  # CQL executors
  def get_one(self, csql, **kwargs):
    with self.getSession() as sess:
      return neo4j_marshaller.get_one(sess, csql, **kwargs)

  def get_all(self, csql, **kwargs):
    with self.getSession() as sess:
      return neo4j_marshaller.get_all(sess, csql, **kwargs)
  
  def cql_run(self, csql, **kwargs):
    with self.getSession() as sess:
      return neo4j_marshaller.cql_run(sess, csql, **kwargs)
