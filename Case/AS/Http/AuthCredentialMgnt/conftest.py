import pytest
from Common.get_token import Token
from Common.readConfig import readconfigs


@pytest.fixture(scope="module", autouse=True)
def token_cache(request, metadata_host):
    host = metadata_host["self.eisoo.com"]
    host = (host.split(":")[1]).strip("/")
    cache_path = "cache/token"
    request.config.cache.set(cache_path, Token(host=host).get_token())
