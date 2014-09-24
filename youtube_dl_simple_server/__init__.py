#!/usr/bin/env python
#-*- encoding:utf-8 -*-

__author__  = 'Carlos Ramos'
__license__ = 'The MIT License'
__version__ = '0.1'

import os
import sys
import urllib2
import subprocess
from argparse import ArgumentParser, RawTextHelpFormatter
from Paths import Paths
from HttpServer import HttpServerHandler, HttpServerThread

def main():
    parser = ArgumentParser(description='Download videos from some video platforms via http requests using youtube-dl', formatter_class=RawTextHelpFormatter)
    parser.add_argument('-v', '--version', action='version', version=__version__)
    parser.add_argument('-u', '--update', action='store_true', help='update or install youtube-dl and exit\n\n')
    parser.add_argument('-p', '--port', type=int, default=49149, help='select server listening port (49149 by default)')
    parser.add_argument('--verbose', action='store_true', help='show what the program is doing')
    args = parser.parse_args()

    try:
        paths = Paths()

        if (args.update):
            update(paths, args.verbose)
        else:
            checkYoutubedl(paths, args.verbose)
            runServer(args.port, args.verbose)
    except KeyboardInterrupt:
        sys.exit(0)

def update(paths, v):
    _update(paths, v)
    sys.exit(0)

def _update(paths, v):
    show('Downloading latest version', v)
    try:
        latest = urllib2.urlopen('https://yt-dl.org/latest/' + paths.getYdlName())
    except:
        show('\nNo Internet connexion', v)
        sys.exit(1)

    if not os.path.isdir(paths.getYdlPath()):
        os.makedirs(paths.getYdlPath())

    output = open(paths.getYdlLocation(), 'wb')
    output.write(latest.read())
    output.close()

    if (os.name != 'nt'):
        show('Changing permissions', v)
        subprocess.check_output(['chmod', 'a+x', paths.getYdlLocation()])

    print '\nUpdated successfully'

def checkYoutubedl(paths, v):
    show('Cheecking youtube-dl\n', v)
    if (not os.path.exists(paths.getYdlLocation())):
        _update(paths, v)
    else:
        show('Cheecking youtube-dl version', v)
        version = subprocess.check_output([paths.getYdlLocation(), '--version']).replace('\n', '')
        try:
            latestVersion = urllib2.urlopen('https://yt-dl.org/latest/version').read()
            show(' - Latest ' + latestVersion, v)
            show(' - Yours  ' + version, v)
            if not latestVersion in version:
                _update(paths, v)
        except:
            show('\nNo Internet connexion', v)
            sys.exit(1)

def runServer(port, v):
    show('\nRunning serer at http://localhost:' + str(port), v)
    httpd = HttpServerThread(('localhost', port), HttpServerHandler)
    httpd.serve_forever()

def show (s, v):
    if (v):
        print s

if __name__ == '__main__':
    main()
