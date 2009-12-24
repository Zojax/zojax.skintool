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
""" skintool implementation

$Id$
"""
from BTrees import OOBTree

from zope import interface, component
from zope.component import getSiteManager
from zope.component import getUtility, getAdapters, getUtilitiesFor
from zope.security.proxy import removeSecurityProxy
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.publisher.interfaces.browser import \
     IDefaultSkin, IBrowserRequest, IDefaultBrowserLayer
from zope.app.component.hooks import getSite
from zope.app.intid.interfaces import IIntIds

from zojax.layoutform import Fields, PageletEditSubForm
from zojax.controlpanel.browser.configlet import Configlet

from interfaces import IDefaultLayer, IDefaultLayers, ISkinTool

cache = {}
skins_byname = {}
skins_registry = {}
layers_byname = {}
layers_registry = {}

default_skin = 'zojax'


class SkinTool(object):
    interface.implements(ISkinTool)

    def generate(self):
        bases = []

        # first add default layers
        for name, adapter in getAdapters((getSite(),), IDefaultLayers):
            for layer in adapter.layers:
                if layer not in bases:
                    bases.append(layer)

        for name, layer in getUtilitiesFor(IDefaultLayer):
            if layer not in bases:
                bases.append(layer)

        # second add skin
        if self.skin:
            skin = skins_byname.get(self.skin)
            if not skin:
                skin = skins_byname.get(default_skin)

            if skin:
                bases.append(skin)
                info = skins_registry.get(skin)
                if info:
                    for layer in info[4]:
                        if layer not in bases:
                            bases.append(layer)

        #third add layers
        for name in self.layers:
            layer = layers_byname.get(name)
            if layer and layer not in bases:
                bases.append(layer)

        # get base skin
        adapters = getSiteManager().adapters
        skin = adapters.lookup((IBrowserRequest,), IDefaultSkin, name='')
        if skin is not None:
            bases.insert(0, skin)
        else:
            bases.insert(0, IDefaultBrowserLayer)

        bases.reverse()
        return bases

    @property
    def skinData(self):
        skin = skins_byname.get(self.skin)
        if skin:
            data = self.data.get('skinData')
            if data is None or not isinstance(data, OOBTree.OOBTree):
                data = OOBTree.OOBTree()
                self.data['skinData'] = data
            return skins_registry[skin][-1](data)
        return None


@component.adapter(ISkinTool, IObjectModifiedEvent)
def skinToolModified(*args):
    global cache

    id = getUtility(IIntIds).queryId(getSite())
    if id in cache:
        del cache[id]


class ConfigletEditForm(Configlet):

    def nextURL(self):
        return self.request.getURL()


class SchemaEditForm(PageletEditSubForm):

    @property
    def fields(self):
        data = self.getContent()
        if data is not None:
            return Fields(data.__schema__)
        return Fields(interface.Interface)

    def getContent(self):
        return removeSecurityProxy(self.context).skinData

    def isAvailable(self):
        return len(self.fields)
