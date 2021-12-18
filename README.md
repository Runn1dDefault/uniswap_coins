# 1 Docker install
# 2 Env configurations
    В дериктории uniswap_backend рядом с файлом manage.py создайте файл .env
```bash
DEBUG_VALUE=True
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost 0.0.0.0 127.0.0.1

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=jjsja7123jdasdkk21238882jjejq

PROVIDER=https://main.infura.io/v3/$SOME_ID
TEST_PROVIDER=https://ropsten.infura.io/v3/$SOME_ID
ADDRESS=$WALLET_ADDRESS
PRIVATE_KEY=$WALLET_PRIVATE_KEY
```
# 3 docker-compose run
```bash
docker-compose -f docker-compose-local.yml up -d --build
```
# 4 Make order
```bash

```