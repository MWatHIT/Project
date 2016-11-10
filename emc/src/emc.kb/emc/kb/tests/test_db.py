#-*- coding: UTF-8 -*-
import datetime
import unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from emc.kb.testing import INTEGRATION_TESTING
#sqlarchemy
from sqlalchemy import text
from sqlalchemy import func

class TestOracleDemoDatabase(unittest.TestCase):

    layer = INTEGRATION_TESTING
    
    def test_oracledb_model(self):
        from emc.kb.mapping_db import  Modeltest
        from emc.kb import pas_session as Session
        

        model = Modeltest()
        import pdb
        pdb.set_trace()
        nums = Session.query(func.count(Model.ID)).scalar()
        if nums != 1:
                    
            model.ID = 100
            model.XHDM = u"C9"
            model.XHMC = u"my phone"        
            Session.add(model)
            Session.commit()     
            self.assertTrue(model.ID is not None)
        
        self.assertTrue(nums is not None)

class TestParametersDatabase(unittest.TestCase):

    layer = INTEGRATION_TESTING
    
    def test_db_mapping_model(self):
        from emc.kb.mapping_db import  Model
        from z3c.saconfig import Session
        

        model = Model()
        model.xhdm = u"C9"
        model.xhmc = u"我的手机"        
        Session.add(model)
        Session.flush()     
        self.assertTrue(model.modelId is not None)
    
    def test_db_mapping_branch(self):
        from emc.kb.mapping_db import  Branch
        from emc.kb.mapping_db import  Model
        from z3c.saconfig import Session

        import pdb
        pdb.set_trace()        
        model = Model()
        model.xhdm = u"C9"
        model.xhmc = u"我的手机"        
        Session.add(model)
                 
        branch = Branch()
        branch.fxtdm = u"C91"
        branch.fxtmc = u"发射器"
        branch.fxtlb = u"fashe"

        branch.model = model                
        Session.add(branch)                
        Session.flush()
         
        self.assertTrue(branch.branchId is not None)
        self.assertTrue(model.modelId is not None)
        self.assertEqual(branch.modelId, model.modelId)
        self.assertEqual(branch.branchId, model.branches[0].branchId)
    
    def test_model_locator(self):
        from emc.kb.mapping_db import  Model
        from emc.kb.interfaces import IModelLocator
        from zope.component import getUtility
        from emc.kb import kb_session as Session
         
        locator = getUtility(IModelLocator)
        #getModel
        xhdm = u'C7'
        xhmc = u"他的手机"
        model = locator.getModelByCode(xhdm)
        #addModel
        if model == None:
            locator.addModel(xhdm=xhdm,xhmc=xhmc)
        else:
            # remove old  delete
            locator.DeleteByCode(xhdm)
            locator.addModel(xhdm=xhdm,xhmc=xhmc)     
#         locator.addModel(model)         

         
        Session.flush()
         
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
         
        portal.invokeFactory('emc.kb.folder', 'folder', title=u"folder")
         
        portal['folder'].invokeFactory('emc.kb.ormfolder', 'ormfolder',
                title=u"ormfolder", description=u"ormfolder",
            )                 
#         paras = {'xhdm':u"C6"}
        model = locator.getModelByCode(xhdm)
         
        self.assertEqual(model.xhdm,xhdm)

        # query pagenation 分页查询
        models = locator.queryModel(start=0,size=1)
        import pdb
        pdb.set_trace()        
        self.assertEqual(len(models),1)
        
#     
#     def test_screening_locator_cinema_lookup(self):
#         from emc.kb.model import Screening
#         from emc.kb.interfaces import IScreeningLocator
#         from zope.component import getUtility
#         from z3c.saconfig import Session
#         
#         model = Screening()
#         model.cinemaCode = u"ABC1"
#         model.filmCode = u"DEF1"
#         model.showTime = datetime.datetime(2011, 1, 1, 12, 0, 0)
#         model.remainingTickets = 10
#         Session.add(model)
#         
#         model = Screening()
#         model.cinemaCode = u"ABC1"
#         model.filmCode = u"DEF2"
#         model.showTime = datetime.datetime(2011, 1, 1, 12, 0, 0)
#         model.remainingTickets = 10
#         Session.add(model)
#         
#         Session.flush()
#         
#         portal = self.layer['portal']
#         setRoles(portal, TEST_USER_ID, ('Manager',))
#         
#         portal.invokeFactory('optilux.CinemaFolder', 'cinemas', title=u"Cinemas")
#         
#         portal['cinemas'].invokeFactory('optilux.Cinema', 'cinema1',
#                 title=u"Cinema 1", description=u"First cinema",
#                 cinemaCode=u"ABC1",
#             )
#         portal['cinemas'].invokeFactory('optilux.Cinema', 'cinema2',
#                 title=u"Cinema 2", description=u"Second cinema",
#                 cinemaCode=u"ABC2",
#             )
#         
#         locator = getUtility(IScreeningLocator)
#         
#         cinemas = locator.cinemasForFilm(u"DEF1", 
#                 datetime.datetime(2011, 1, 1, 0, 0, 0),
#                 datetime.datetime(2011, 1, 1, 23, 59, 59),
#             )
#         
#         self.assertEqual(cinemas, [{'address': 'First cinema',
#                                     'cinemaCode': 'ABC1',
#                                     'name': 'Cinema 1',
#                                     'url': 'http://nohost/plone/cinemas/cinema1'}])
#     
#     def test_screening_locator_screening_lookup(self):
#         from emc.kb.model import Screening
#         from emc.kb.interfaces import IScreeningLocator
#         from zope.component import getUtility
#         from z3c.saconfig import Session
#         
#         screeningId = None
#         
#         model = Screening()
#         model.cinemaCode = u"ABC1"
#         model.filmCode = u"DEF1"
#         model.showTime = datetime.datetime(2011, 1, 1, 12, 0, 0)
#         model.remainingTickets = 10
#         Session.add(model)
#         
#         Session.flush()
#         
#         screeningId = model.screeningId
#         
#         model = Screening()
#         model.cinemaCode = u"ABC1"
#         model.filmCode = u"DEF2"
#         model.showTime = datetime.datetime(2011, 1, 1, 12, 0, 0)
#         model.remainingTickets = 10
#         Session.add(model)
#         
#         Session.flush()
#         
#         locator = getUtility(IScreeningLocator)
#         
#         model = locator.screeningById(screeningId)
#         
#         self.assertEqual(model.cinemaCode, u"ABC1")
#         self.assertEqual(model.filmCode, u"DEF1")
#     
#     def test_screening_locator_screening_listing(self):
#         from emc.kb.model import Screening
#         from emc.kb.interfaces import IScreeningLocator
#         from zope.component import getUtility
#         from z3c.saconfig import Session
#         
#         model = Screening()
#         model.cinemaCode = u"ABC1"
#         model.filmCode = u"DEF1"
#         model.showTime = datetime.datetime(2011, 1, 1, 12, 0, 0)
#         model.remainingTickets = 10
#         Session.add(model)
#         
#         model = Screening()
#         model.cinemaCode = u"ABC1"
#         model.filmCode = u"DEF2"
#         model.showTime = datetime.datetime(2011, 1, 1, 12, 0, 0)
#         model.remainingTickets = 10
#         Session.add(model)
#         
#         Session.flush()
#         
#         portal = self.layer['portal']
#         setRoles(portal, TEST_USER_ID, ('Manager',))
#         
#         portal.invokeFactory('optilux.CinemaFolder', 'cinemas', title=u"Cinemas")
#         
#         portal['cinemas'].invokeFactory('optilux.Cinema', 'cinema1',
#                 title=u"Cinema 1", description=u"First cinema",
#                 cinemaCode=u"ABC1",
#             )
#         portal['cinemas'].invokeFactory('optilux.Cinema', 'cinema2',
#                 title=u"Cinema 2", description=u"Second cinema",
#                 cinemaCode=u"ABC2",
#             )
#         
#         portal.invokeFactory('optilux.FilmFolder', 'films', title=u"Films")
#         
#         portal['films'].invokeFactory('optilux.Film', 'film1',
#                 title=u"Film 1", description=u"First film", filmCode=u"DEF1",
#             )
#         portal['films'].invokeFactory('optilux.Film', 'film2',
#                 title=u"Film 2", description=u"Second film", filmCode=u"DEF2",
#             )
#         
#         locator = getUtility(IScreeningLocator)
#         screenings = locator.screenings(u"DEF1", u"ABC1",
#                 datetime.datetime(2011, 1, 1, 0, 0, 0),
#                 datetime.datetime(2011, 1, 1, 23, 59, 59),
#             )
#         
#         self.assertEqual(len(screenings), 1)
#         self.assertEqual(screenings[0].filmCode, u"DEF1")
#         self.assertEqual(screenings[0].cinemaCode, u"ABC1")
#         self.assertEqual(screenings[0].remainingTickets, 10)
#     
#     def test_ticket_reserver(self):
#         from emc.kb.model import Screening
#         from emc.kb.reservation import Reservation
#         from emc.kb.interfaces import ITicketReserver
#         from z3c.saconfig import Session
#         from zope.component import getUtility
#         
#         model = Screening()
#         model.cinemaCode = u"ABC1"
#         model.filmCode = u"DEF1"
#         model.showTime = datetime.datetime(2011, 1, 1, 12, 0, 0)
#         model.remainingTickets = 10
#         
#         Session.add(model)
#         Session.flush()
#         
#         reservation = Reservation()
#         reservation.numTickets = 2
#         reservation.customerName = u"John Smith"
#         reservation.model = model
#         
#         reserver = getUtility(ITicketReserver)
#         reserver(reservation)
#         
#         Session.flush()
#         
#         self.assertTrue(reservation.reservationId is not None)
#         self.assertEqual(model.remainingTickets, 8)
#     
#     def test_ticket_reserver_no_remaining_tickets(self):
#         from emc.kb.model import Screening
#         from emc.kb.reservation import Reservation
#         
#         from emc.kb.interfaces import ITicketReserver
#         from emc.kb.interfaces import ReservationError
#         from z3c.saconfig import Session
#         from zope.component import getUtility
#         
#         model = Screening()
#         model.cinemaCode = u"ABC1"
#         model.filmCode = u"DEF1"
#         model.showTime = datetime.datetime(2011, 1, 1, 12, 0, 0)
#         model.remainingTickets = 0
#         
#         Session.add(model)
#         Session.flush()
#         
#         reservation = Reservation()
#         reservation.numTickets = 2
#         reservation.customerName = u"John Smith"
#         reservation.model = model
#         
#         reserver = getUtility(ITicketReserver)
#         
#         self.assertRaises(ReservationError, reserver, reservation)
#     
#     def test_ticket_reserver_insufficient_tickets(self):
#         from emc.kb.model import Screening
#         from emc.kb.reservation import Reservation
#         
#         from emc.kb.interfaces import ITicketReserver
#         from emc.kb.interfaces import ReservationError
#         from z3c.saconfig import Session
#         from zope.component import getUtility
#         
#         model = Model()
#         model.xhdm = u"ABC1"
#         model.xhmc = u"DEF1"
# 
#         
#         Session.add(model)
#         Session.flush()
#         
#         reservation = Reservation()
#         reservation.numTickets = 11
#         reservation.customerName = u"John Smith"
#         reservation.model = model
#         
#         reserver = getUtility(ITicketReserver)
#         
#         self.assertRaises(ReservationError, reserver, reservation)
