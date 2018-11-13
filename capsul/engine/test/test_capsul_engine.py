from __future__ import print_function

import unittest
import tempfile
import os

try:
    import populse_db
except ImportError:
    populse_db = None

from capsul.api import Pipeline, capsul_engine

class TestCapsulEngine(unittest.TestCase):
    def test_default_engine(self):
        tmp = tempfile.mktemp(suffix='.json')
        ce = capsul_engine(tmp)
        ce.save()
        try:
            ce2 = capsul_engine(tmp)
            self.assertEqual(ce.execution_context.to_json(),
                             ce2.execution_context.to_json())
            self.assertEqual(ce.database.named_directory('capsul_engine'),
                             ce2.database.named_directory('capsul_engine'))
            self.assertIsInstance(ce.get_process_instance('capsul.pipeline.test.test_pipeline.MyPipeline'),
                                  Pipeline)
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)
        
    def test_populse_db_engine(self):
        if populse_db is None:
            self.skipTest('populse_db is not installed')
        tmp = tempfile.mktemp(suffix='.sqlite')
        ce = capsul_engine(tmp)
        ce.save()
        try:
            ce2 = capsul_engine(tmp)
            self.assertEqual(ce.execution_context.to_json(),
                             ce2.execution_context.to_json())
            self.assertEqual(ce.database.named_directory('capsul_engine'),
                             ce2.database.named_directory('capsul_engine'))
            self.assertIsInstance(ce.get_process_instance('capsul.pipeline.test.test_pipeline.MyPipeline'),
                                  Pipeline)
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)

def test():
    """ Function to execute unitest.
    """
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCapsulEngine)
    runtime = unittest.TextTestRunner(verbosity=2).run(suite)
    return runtime.wasSuccessful()


if __name__ == "__main__":
    print("RETURNCODE: ", test())
