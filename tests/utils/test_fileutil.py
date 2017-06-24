import os
import unittest

from tinyenv.utils import fileutil as fu

NASDAQ = {
    'path': 'tests/fixtures/nasdaq.csv',
    'sha': '8e0a44364a771140e6b18944b49aafe6fc79b366e8a93ebdab6be5fc9241c935',
    'md5': 'f0308d6addae051758dfbf80a3b22676',
}

BASE_URL = 'http://static.bearhug.cc/tiny/loadertest/'


class TestFileUtil(unittest.TestCase):

    def test_download_file(self):
        fname = 'hmda.tar.gz'
        fu.download_file(BASE_URL + fname, fname)
        assert fu.validate_file(fname, 'bf9f2662eb25683ca26fc58e3f90b2ad')
        os.remove(fname)

    def test_hash_file(self):
        path = NASDAQ['path']
        assert fu.hash_file(path) == NASDAQ['sha']
        assert fu.hash_file(path, chunk_size=1715) == NASDAQ['sha']
        assert fu.hash_file(path, algo='md5') == NASDAQ['md5']
        assert fu.hash_file(path, algo='md5', chunk_size=1715) == NASDAQ['md5']

    def test_validate_file(self):
        path = NASDAQ['path']
        assert fu.validate_file(path, NASDAQ['sha'])
        assert fu.validate_file(path, NASDAQ['md5'])
        assert not fu.validate_file(path, NASDAQ['md5'], algo='sha256')
        assert not fu.validate_file(path, NASDAQ['sha'], algo='md5')
