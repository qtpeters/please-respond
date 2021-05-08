
import unittest
from pleaserespond import aggregator
from test.util import _get_data

class TestAggregator(unittest.TestCase):

    def test_aggregator( self ):
        data1 = _get_data( "response1.json" )
        data2 = _get_data( "response2.json" )
        agg = aggregator.Aggregator()
        agg.consume( data1.encode() )
        agg.consume( data2.encode() )

        data = agg.get_data()

        updated = data[ "updated" ]
        self.assertTrue( updated )

        total = data[ "total" ]
        self.assertEqual( total, 2 )

        latest = data[ "latest" ]
        url = latest[ "url" ]
        self.assertEqual( url, "SECOND" )

        npc = data[ "npc" ]
        us = npc[ " United States" ]
        self.assertEqual( us, 1 )
        fr = npc[ " France" ]
        self.assertEqual( fr, 1 )   

if __name__ == '__main__':
    unittest.main()