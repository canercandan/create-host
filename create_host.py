#!/usr/bin/env python

HOSTS_PATH = "/hosts"

import optparse, logging, sys, os, common

logger = logging.getLogger('Create Host')

def makedirs(dirname):
    try:
        os.makedirs(dirname)
    except OSError:
        pass

def main():
    parser = optparse.OptionParser()
    parser.add_option('-d', '--domain', help='domain name to create')
    options = common.parser(parser)

    logger.info('create domain name %s' % options.domain)

    domain = options.domain.split('.')

    if len(domain) < 2:
        logger.error('incorrect domain')
        return

    if domain[0] == 'www':
        logger.error('don\'t use www ahead your domain')
        return

    pre, post = domain

    tab = ['_', '_', '_', '_']

    for i in range(0, 3):
        if i < len(pre):
            tab[i] = pre[i]
    if len(pre) >= 4:
        tab[3] = pre[3:]

    path = '%s/%s' % (post, '/'.join(tab))

    print path

    makedirs(path)

if __name__ == '__main__':
    main()
