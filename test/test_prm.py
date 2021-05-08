import unittest
from pleaserespond.prm import PleaseRespond
from pleaserespond.aggregator import Aggregator
from importlib_resources import files

class TestPrm( unittest.TestCase ):

    def _get_data( self, json_file ):
        return files( "test.data" ) \
        .joinpath( json_file ) \
        .read_text()

    def _consume_test_data( self, pr ):

        data1 = self._get_data( "response1.json" )
        data2 = self._get_data( "response2.json" )
        data3 = self._get_data( "response3.json" )
        pr.ag.consume( data1.encode() )
        pr.ag.consume( data2.encode() )
        pr.ag.consume( data3.encode() )


    def test_prm( self ):

        pr = PleaseRespond( 0 )
        pr.ag = Aggregator()
        self._consume_test_data( pr )
        report = pr.report()

        self.assertEqual( report, "3,2021-06-22 18:03:20+10:00,FIRST,au,1,fr,1,us,1" )

if __name__ == '__main__':
    unittest.main()