#! /usr/bin/env python

import sys
import os
import time
import unittest
import testcases

def main():
    child_pid = os.fork()
    if child_pid:
        try:
            time.sleep(5)
            suite = unittest.TestLoader().loadTestsFromModule(testcases)
            result = unittest.TextTestRunner().run(suite)
            if result.wasSuccessful(): exitcode = 0
            else: exitcode = 1
        except:
            exitcode = 1
        finally:
            os.kill(child_pid, 9)
        return exitcode
    else:
        os.execlp('dev_appserver.py', 'dev_appserver.py', '-c', 'build/gelt')

if __name__ == '__main__':
    sys.exit(main())
