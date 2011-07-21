#!/usr/bin/env python

#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
# Authors:
# Caner Candan <caner@candan.fr>, http://caner.candan.fr
#

# TODO
#
# options -path
# options -password
#
# delete_hosts.py
#

import optparse, logging, sys, os, common

logger = logging.getLogger('Create Host')

def makedirs(dirname):
    try: os.makedirs(dirname)
    except OSError: pass

def symlink(src, dst):
    try: os.symlink(src, dst)
    except OSError: pass

def build_path(pre, post):
    tab = [post, '_', '_', '_', '_', 'docs']

    for i in range(0, 3):
        if i < len(pre):
            tab[i+1] = pre[i]
    if len(pre) >= 4:
        tab[4] = pre[3:]

    return tab

def main():
    parser = optparse.OptionParser()
    parser.add_option('-d', '--domain', help='domain name to create')
    parser.add_option('-p', '--path', default='.', help='path where to create the web space')
    options = common.parser(parser)

    if not options.domain:
        logger.error('no domain name specified')
        return

    domain = options.domain.split('.')

    if len(domain) == 3:
        logger.info('create a subdomain name %s' % options.domain)

        sub, name, ext = domain
        tab = build_path(sub, '.'.join(domain[1:]))

        subpath = '/'.join(tab)
        fullpath = '%s/%s' % (options.path, subpath)

        logger.info('create path directories (%s)' % fullpath)
        makedirs(fullpath)

        logger.info('create symbolic links to docs (%s)' % fullpath)
        symlink(subpath, '%s/%s_docs' % (options.path, options.domain))

        logger.info('created')

        return

    logger.info('create a domain name %s' % options.domain)

    if len(domain) < 2:
        logger.error('incorrect domain')
        return

    if domain[0] == 'www':
        logger.error('don\'t use www ahead your domain')
        return

    pre, post = domain

    tab = build_path(pre, post)

    path_docs = '%s/w/w/w/_/docs' % options.domain
    fullpath_docs = '%s/%s' % (options.path, path_docs)
    path_alias = '/'.join(tab[:-1])
    fullpath_alias = '%s/%s' % (options.path, path_alias)
    path_alias_docs = '/'.join(tab)
    fullpath_alias_docs = '%s/%s' % (options.path, path_alias_docs)

    logger.info('create alias path directories (%s)' % fullpath_alias)
    makedirs(fullpath_alias)

    logger.info('create path to docs (%s)' % fullpath_docs)
    makedirs(fullpath_docs)

    logger.info('create symbolic links to docs (%s)' % fullpath_alias_docs)
    symlink('../../../../../%s' % path_docs, fullpath_alias_docs)
    symlink(path_docs, '%s/%s_docs' % (options.path, options.domain))

    logger.info('created')

if __name__ == '__main__':
    main()
