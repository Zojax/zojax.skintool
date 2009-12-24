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
"""Tests for the Preferences System

$Id$
"""
import os.path, unittest, doctest

from zope import component
from zope.component import testing
from zope.testing import doctestunit
from zope.app.testing import setup, functional
from zope.app.intid.interfaces import IIntIds
from zope.app.intid import IntIds
from zope.app.rotterdam import Rotterdam

from zojax.controlpanel.testing import setUpControlPanel
from zojax.layoutform.interfaces import ILayoutFormLayer
from zojax.skintool.tool import SkinTool


class IDefaultSkin(ILayoutFormLayer, Rotterdam):
    """ skin """


class ITestSkin(IDefaultSkin):
    """ test Skin """


zojaxSkinTool = functional.ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'zojaxSkinTool', allow_teardown=True)


def FunctionalDocFileSuite(*paths, **kw):
    globs = kw.setdefault('globs', {})
    globs['sync'] = functional.sync
    globs['http'] = functional.HTTPCaller()
    globs['getRootFolder'] = functional.getRootFolder

    kw['package'] = doctest._normalize_module(kw.get('package'))

    kwsetUp = kw.get('setUp')
    def setUp(test):
        functional.FunctionalTestSetup().setUp()

        root = functional.getRootFolder()
        root['intid'] = IntIds()
        component.provideUtility(root['intid'], IIntIds)

    kw['setUp'] = setUp

    kwtearDown = kw.get('tearDown')
    def tearDown(test):
        functional.FunctionalTestSetup().tearDown()

    kw['tearDown'] = tearDown

    if 'optionflags' not in kw:
        old = doctest.set_unittest_reportflags(0)
        doctest.set_unittest_reportflags(old)
        kw['optionflags'] = (old
                             | doctest.ELLIPSIS
                             | doctest.NORMALIZE_WHITESPACE)

    suite = doctest.DocFileSuite(*paths, **kw)
    suite.layer = zojaxSkinTool
    return suite

def setUp(test):
    site = setup.placefulSetUp(site=True)
    setup.setUpTestAsModule(test, 'zojax.skintool.README')
    site['intid'] = IntIds()
    component.provideUtility(site['intid'], IIntIds)
    setUpControlPanel()
    # register utility


def tearDown(test):
    setup.placefulTearDown()
    setup.tearDownTestAsModule(test)

def test_suite():
    testbrowser = FunctionalDocFileSuite("testbrowser.txt")

    return unittest.TestSuite((
            testbrowser,
            doctest.DocFileSuite(
                '../README.txt',
                setUp=setUp, tearDown=tearDown,
                globs={'pprint': doctestunit.pprint},
                optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
            ))
