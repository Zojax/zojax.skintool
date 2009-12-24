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
""" Skin Data metaclass

$Id$
"""
import sys
from zope.schema import getFields
from persistent import Persistent
from zope.app.container.contained import Contained

from interfaces import _
from zojax.controlpanel.storage import ConfigletData
from zojax.controlpanel.configlettype import DataProperty

from interfaces import _

_marker = object()


class SkinData(object):

    __data__ = None

    def __init__(self, data):
        self.__data__ = data


class ConfigProperty(object):

    def __init__(self, field, name=None):
        if name is None:
            name = field.__name__

        self.__field = field
        self.__name = name

    def __get__(self, inst, klass):
        if inst is None:
            return self

        value = inst.__data__.get(self.__name, _marker)
        if value is _marker:
            return self.__field.default

        return value

    def __set__(self, inst, value):
        field = self.__field.bind(inst)
        field.validate(value)
        if field.readonly and \
               inst.__data__.get(self.__name, _marker) is not _marker:
            raise ValueError(self.__name, _(u'Field is readonly'))

        inst.__data__[self.__name] = value

    def __delete__(self, inst):
        del inst.__data__[self.__name]


class SkinDataType(type):
    """ Metaclass for skin data """

    def __new__(cls, name, schema, class_=None, *args, **kw):
        cname = 'SkinData<%s>'%name
        if type(class_) is tuple:
            bases = class_ + (SkinData,)
        elif class_ is not None:
            bases = (class_, SkinData)
        else:
            bases = (SkinData,)

        tp = type.__new__(cls, str(cname), bases, {})
        setattr(sys.modules['zojax.skintool.skindatatype'], cname, tp)

        return tp

    def __init__(cls, name, schema, class_=None, title='', description=''):
        for f_id in getFields(schema):
            if not hasattr(cls, f_id):
                setattr(cls, f_id, ConfigProperty(schema[f_id]))

        cls.__id__ = unicode(name)
        cls.__title__ = title
        cls.__description__ = description
        cls.__schema__ = DataProperty(schema)
