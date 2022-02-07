# 1 Docker install 
[Руководство по установке docker на windows](https://docs.docker.com/desktop/windows/install/)

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

# 4 HTTP Provider
[HTTP provider Infura](https://infura.io/)

[Мануал для получения ссылок провайдера Infura ](https://docs.google.com/document/d/1S8iiQL58zHLdebmAbakcnMEitQlEIimCjuXpLJypByA/edit?usp=sharing)

# 3 docker-compose run
```bash
docker-compose -f docker-compose-local.yml up -d --build
```
# 4 Make order

[Мануал по созданию нового order](https://docs.google.com/document/d/1c5_-flG4l_5OkGY_-6RA1ddEVeL91IlvDsRBew8ENfI/edit)