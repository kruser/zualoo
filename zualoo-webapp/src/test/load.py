#! /usr/bin/env python

import sys
from pyamf.remoting.client import RemotingService
import loaddata

def main(host):
    gw = RemotingService('http://%s/gateway' % host)
    service = gw.getService('grocery')
    for store in loaddata.stores:
        service.create('RetailStore', dict(name=store))
    for key in loaddata.sections.keys():
        id = service.create('StoreSection', dict(name=key))
        for item in loaddata.sections[key]:
            service.create('ItemDescription', dict(store_section=id,
                                              description=item[0],
                                              is_default=item[1]))

if __name__ == '__main__':
    if 1 == len(sys.argv): host = "localhost:8080"
    else: host = sys.argv[1]
    main(host)
