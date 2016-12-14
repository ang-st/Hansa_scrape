import threading
from parsers import *
import urllib 
import urllib2
import sys
import Queue
import logging
import coloredlogs
import pymongo
import traceback

logger = logging.getLogger('Hansa_main')
coloredlogs.install(level='DEBUG')

job_queue = Queue.Queue()

mongo=pymongo.MongoClient("127.0.0.1", 27017)

base_url = "http://hansamkt2rr6nfg3.onion"
product_base_url = base_url+'/listing/'
suffix = "/feedback/"
thread_pool_size = 15


def main():

  try:
    start, stop = sys.argv[1], sys.argv[2]

  except IndexError:
    logger.error( '%s start stop'%sys.argv[0] ) 
    sys.exit(-1)


  logger.info("Scaper Start")
  [ job_queue.put(product_base_url+str(i)+suffix)  for i in xrange(int(start),int(stop))]
  logger.info("Got %d products in queue"%job_queue.qsize())
  threads = [threading.Thread(target=hansa_worker) for x in xrange(thread_pool_size)]
  for thread in threads:
      thread.start()
  for thread in threads:
      thread.join()

def parse_insert(html):
  try:
      p=parser_product(html)
      try:
        mongo.mydb.prod.insert(p)
      except pymongo.errors.DuplicateKeyError:
        pass
      next_feed, feeds= parser_feedback(html)
      try:
        mongo.mydb.feedback.insert(feeds)
      except pymongo.errors.InvalidOperation:
        pass
      if next_feed:
        job_queue.put(base_url+next_feed)
  except AttributeError:
    #logging.exception("Parse")
    #logging.debug(html)
    pass
    #raise Exception("Error Parse")


def hansa_worker():
  job_done = False
  while not job_done:
    try:
      url = job_queue.get(True, 15)
      req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:45.0) Gecko/20100101 Firefox/45.0' })
      html= urllib2.urlopen(req).read()
      if html.strip() :
        parse_insert(html)
      
    except Queue.Empty:
      job_done=True

    except Exception, e: 
      logger.error("Exception in thread, url :%s "%url)
      traceback.print_exc()
      #print html
      #job_done=True
      #logger.debug(html)
    
    
  logger.info("Thread exit")


if __name__ == "__main__":
  main()

