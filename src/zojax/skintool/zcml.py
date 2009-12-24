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
""" zojax:layer directive

$Id$
"""
from zope import schema, interface, component
from zope.configuration.fields import Tokens, GlobalInterface, PythonIdentifier

from skindatatype import SkinDataType

from zojax.skintool import tool


class ISkinDirective(interface.Interface):

    layer = GlobalInterface(
                title = u'Skin',
                description = u'Skin interface.',
                required = True)

    name = PythonIdentifier(
                title = u'Name',
                description = u'Content name.',
                required = True)

    title = schema.TextLine(
                title = u'Title',
                description = u'Content title.',
                required = True)

    description = schema.TextLine(
                title = u'Description',
                description = u'Content description.',
                required = False)

    require = Tokens(
                title = u'Require',
                description = u'Interface of layers that are '\
                    u'required by this layer.',
                required = False,
                value_type = GlobalInterface())

    schema = GlobalInterface(
                title = u'Schema',
                description = u'Skin schema interface.',
                default = interface.Interface)


class ILayerDirective(interface.Interface):

    layer = GlobalInterface(
                title = u'Layer',
                description = u'Skin layer.',
                required = True)

    name = PythonIdentifier(
                title = u'Name',
                description = u'Content name.',
                required = True)

    title = schema.TextLine(
                title = u'Title',
                description = u'Content title.',
                required = True)

    description = schema.TextLine(
                title = u'Description',
                description = u'Content description.',
                required = False)


def skinDirectiveHandler(_context, layer, name, title,
                         description='',require=[],schema=interface.Interface):
    _context.action(
        discriminator = ('zojax.skintool-skin', layer, name),
        callable = skinDirective,
        args = (layer, name, title, description, require, schema))


def skinDirective(layer, name, title, description,
                  require, schema=interface.Interface):
    sitemanager = component.getGlobalSiteManager()

    tool.skins_byname[name] = layer
    skinDataClass = SkinDataType('ui.portalskin.skindata', schema)
    interface.classImplements(skinDataClass, schema)
    tool.skins_registry[layer] = (layer, name, title,
                                  description, require, skinDataClass)


def layerDirectiveHandler(_context, layer, name, title, description=''):
    _context.action(
        discriminator = ('zojax.skintool-layer', layer, name),
        callable = layerDirective,
        args = (layer, name, title, description))


def layerDirective(layer, name, title, description):
    sitemanager = component.getGlobalSiteManager()

    tool.layers_byname[name] = layer
    tool.layers_registry[layer] = (layer, name, title, description)
