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
""" zojax.skintool interfaces

$Id$
"""
from zope import schema, interface
from zope.i18nmessageid import MessageFactory
from zojax.widget.radio.field import RadioChoice
from zojax.widget.checkbox.field import CheckboxList

_ = MessageFactory('zojax.skintool')


class ISkinable(interface.Interface):
    """ marker interface for skinable objects """


class INoSkinSwitching(interface.Interface):
    """ if default skin provide this interface, do not switch skin """


class IDefaultLayer(interface.interfaces.IInterface):
    """ default layer (automaticlly added to skin) """


class IDefaultLayers(interface.Interface):
    """ adapter that provide default layers """

    layers = interface.Attribute('tuple of ILayer interfaces')


class ISkinTool(interface.Interface):
    """ skin tool, allow generate skin on the fly """

    skin = RadioChoice(
        title = _('Skin'),
        description = _(u'Select portal skin.'),
        vocabulary = "zojax skins",
        required = False)

    layers = CheckboxList(
        title = _(u'Layers'),
        description = _(u'Select skin layers.'),
        vocabulary = "zojax layers",
        default = [],
        required = False)

    skinData = interface.Attribute('Skin data')

    def generate():
        """ generate skin interface """
