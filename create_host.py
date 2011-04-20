#!/usr/bin/env python

HOSTS_PATH = "/hosts"

import optparse, logging, sys, os, common

logger = logging.getLogger('Create Host')

def makedirs(dirname):
    try: os.makedirs(dirname)
    except OSError: pass

def symlink(src, dst):
    try: os.symlink(src, dst)
    except OSError: pass

def main():
    parser = optparse.OptionParser()
    parser.add_option('-d', '--domain', help='domain name to create')
    options = common.parser(parser)

    if not options.domain:
        logger.error('no domain name specified')
        return

    logger.info('create domain name %s' % options.domain)

    domain = options.domain.split('.')

    if len(domain) < 2:
        logger.error('incorrect domain')
        return

    if domain[0] == 'www':
        logger.error('don\'t use www ahead your domain')
        return

    pre, post = domain

    tab = ['%s' % post, '_', '_', '_', '_', 'docs']

    for i in range(0, 3):
        if i < len(pre):
            tab[i+1] = pre[i]
    if len(pre) >= 4:
        tab[4] = pre[3:]

    path_docs = '%s/w/w/w/_/docs' % options.domain
    alias_path = '/'.join(tab[:-1])
    alias_path_docs = '/'.join(tab)

    logger.info('create alias path directories (%s)' % alias_path)
    makedirs(alias_path)

    logger.info('create path to docs (%s)' % path_docs)
    makedirs(path_docs)

    logger.info('create symbolic links to docs (%s)' % alias_path_docs)
    symlink('../../../../../%s' % path_docs, alias_path_docs)
    symlink(path_docs, '%s_docs' % options.domain)

    logger.info('created')

if __name__ == '__main__':
    main()
