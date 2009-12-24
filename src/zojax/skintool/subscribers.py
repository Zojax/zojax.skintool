##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import component
from zope.proxy import removeAllProxies
from zope.component import getUtility
from zope.interface import directlyProvides
from zope.app.intid.interfaces import IIntIds
from zope.app.component.interfaces import ISite
from zope.app.publication.interfaces import IBeforeTraverseEvent

from tool import cache
from interfaces import ISkinTool, ISkinable, INoSkinSwitching


@component.adapter(ISite, IBeforeTraverseEvent)
def threadServiceSubscriber(site, event,
                            ISkinable = ISkinable,
                            removeAllProxies=removeAllProxies,
                            directlyProvides=directlyProvides):

    if INoSkinSwitching.providedBy(event.request):
        return

    site = removeAllProxies(site)

    if not ISkinable.providedBy(site):
        return

    id = getUtility(IIntIds).queryId(site)
    if id not in cache:
        skin = getUtility(ISkinTool).generate()
        cache[id] = skin
    else:
        skin = cache[id]

    if skin:
        directlyProvides(event.request, *skin)
