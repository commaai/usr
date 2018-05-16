
""" This file contains some helpers methods in both Python2 and 3 """
import sys
import re
import os

if sys.version < '3':
    # Python2.x imports
    import zmq
    import codecs
else:
    # Python 3.x imports
    import queue

LOGENTRIES_PORT = 8811

class ZMQueue(object):
  def __init__(self, max_size):
    self.gsocket = None
    self.psocket = None

  def empty(self):
    return False

  # can only get or put
  # and only one getter i think
  def get(self, block=True):
    #print "get waiting"
    if self.gsocket == None:
      self.context = zmq.Context()
      #print "open gsocket"
      self.gsocket = self.context.socket(zmq.PULL)
      self.gsocket.bind("tcp://127.0.0.1:%d" % (LOGENTRIES_PORT))
    ret = self.gsocket.recv()
    #print "got", ret
    return ret

  def put_nowait(self, msg):
    #print "put", type(msg), msg
    if self.psocket == None or self.pid != os.getpid():
      #print "open psocket"
      self.context = zmq.Context()
      self.psocket = self.context.socket(zmq.PUSH)
      self.psocket.connect("tcp://127.0.0.1:%d" % (LOGENTRIES_PORT))
      self.pid = os.getpid()

    self.psocket.send(msg, zmq.NOBLOCK)
    #self.psocket.send(msg)
    #print "put done"

def check_token(token):
    """ Checks if the given token is a valid UUID."""
    valid = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-"
                       r"[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")

    return valid.match(token)

# We need to do some things different pending if its Python 2.x or 3.x
if sys.version < '3':
    def to_unicode(ch):
        return codecs.unicode_escape_decode(ch)[0]

    def is_unicode(ch):
        return isinstance(ch, unicode)

    def create_unicode(ch):
        try:
            return unicode(ch, 'utf-8')
        except UnicodeDecodeError as e:
            return str(e)

    def create_queue(max_size):
        return ZMQueue(max_size)
else:
    def to_unicode(ch):
        return ch

    def is_unicode(ch):
        return isinstance(ch, str)

    def create_unicode(ch):
        return str(ch)

    def create_queue(max_size):
        return queue.Queue(max_size)
