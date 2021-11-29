import unittest
import main_runner
import requests
import unittest.mock
from unittest.mock import patch

class TestStuff(unittest.TestCase):

    #checks if able to connect with api with given username and password
    def test_gettingToServer(self):
        url = "https://" + main_runner.subdomain + ".zendesk.com/api/v2/tickets.json"
        params = {"per page": 25, "page": 1}
        auth = (main_runner.username, main_runner.password)
        stuff = requests.get(url=url, params=params, auth=auth)
        self.assertEqual(stuff.status_code,201)
    
    #checks if code gets the correct ticket
    def test_getOneTicket(self):
        ticketData = main_runner.getOne(501)
        self.assert_Equal(ticketData["ticket"]["id"], 501)
    
    #checks if code gets all 100 tickets I created
    def test_getAllTickets(self):
        ticketData = main_runner.getAll()
        self.assertEqual(ticketData["count"], 100)

    #making sure running the page printer goes smoothly
    @patch('builtins.input', side_effect=['q'])
    def test_printAll(self, mock_inputs):
        main_runner.printAll(1)
        self.assertFalse(False)
    
    #making sure the program exits when q is hit
    @patch('builtins.input', side_effect=['q'])
    def test_callWhen(self, mock_inputs, mock_print):
        main_runner.callWhenProblem()
        self.assertFalse(False)

