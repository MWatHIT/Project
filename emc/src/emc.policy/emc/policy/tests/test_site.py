#-*- coding: UTF-8  -*-
import unittest
from emc.policy.testing import INTEGRATION_TESTING

from Products.CMFCore.utils import getToolByName

class TestSetup(unittest.TestCase):
    
    layer = INTEGRATION_TESTING
    
    def test_portal_title(self):
        portal = self.layer['portal']
        self.assertEqual("EMC", portal.getProperty('title'))
    
    def test_portal_description(self):
        portal = self.layer['portal']
        self.assertEqual("EMC中国", portal.getProperty('description'))
   

     
    
    def test_Requirements_installed(self):
        portal = self.layer['portal']
        portal_types = getToolByName(portal, 'portal_types')
        
        self.assertTrue('emc.bokeh.fearture' in portal_types)
       
    
#    def test_metaTypesNotToList_configured(self):
#        portal = self.layer['portal']
#        portal_properties = getToolByName(portal, 'portal_properties')
#        navtree_properties = portal_properties['navtree_properties']
#        metaTypesNotToList = navtree_properties.getProperty('metaTypesNotToList')
#        
#        self.assertTrue("Promotion" in metaTypesNotToList)
#        self.assertTrue("Discussion Item" in metaTypesNotToList)
#        self.assertFalse("Cinema" in metaTypesNotToList)
#    
#    def test_add_promotion_permission_for_staffmember(self):
#        portal = self.layer['portal']
#        
#        self.assertTrue('Optilux: Add Promotion' in [r['name'] for r in 
#                                portal.permissionsOfRole('StaffMember')
#                                if r['selected']])
#    
#    def test_dam_report_installed(self):
#        portal = self.layer['portal']
#        portal_actions = getToolByName(portal, 'portal_actions')
#        
#        self.assertTrue('dam-report' in portal_actions['site_actions'])
#    
#    def test_contact_action_installed(self):
#        portal = self.layer['portal']
#        portal_actions = getToolByName(portal, 'portal_actions')
#        
#        self.assertTrue('enquiry' in portal_actions['site_actions'])
#        self.assertFalse(portal_actions['site_actions']['contact'].visible)
#
#    def test_manage_own_portlets_permission(self):
#        portal = self.layer['portal']
#        
#        self.assertTrue('Portlets: Manage own portlets' in
#                [r['name'] for r in 
#                    portal.permissionsOfRole('StaffMember')
#                        if r['selected']])
#        self.assertFalse('Portlets: Manage own portlets' in
#                [r['name'] for r in 
#                    portal.permissionsOfRole('Member')
#                        if r['selected']])
#    
#    def test_add_portal_member_permission(self):
#        portal = self.layer['portal']
#        
#        self.assertTrue('Add portal member' in
#                [r['name'] for r in 
#                    portal.permissionsOfRole('Anonymous')
#                    if r['selected']])

