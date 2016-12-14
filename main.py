import threading
from parsers import *
import urllib 
import sys
import Queue

job_done = False

def ReviewConsumer():
    while True:
        data = ReviewsReview
        if data is None:
            break
        do_other_work()


product_base_url = 'http://hansamkt2rr6nfg3.onion/listing/'
suffix = "/feedback/"




try:
  start, stop = sys.argv[1], sys.argv[2]

except IndexError:
  print '%s start stop'%sys.argv[0]
  sys.exit(-1)


jobs =  [i  for i in xrange(int(start),int(stop))]

def get_product(pid):
  url = product_base_url + str(pid) + suffix
  get_content()



