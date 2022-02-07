from django.core.signing import Signer
from django.db import models
from django.contrib.auth import get_user_model


class WalletManager(models.Manager):
    use_in_migrations = True

    def __init__(self):
        super().__init__()
        self._signer = Signer()

    def _create_wallet(self, user, address: str, private_key: str):
        sign_obj = self._signer.sign_object({'private_key': private_key})
        obj = self.model(user=user, address=address, private_key=sign_obj)
        obj.save(self._db)
        return obj

    def create(self, user, address: str, private_key: str):
        return self._create_wallet(user=user, address=address, private_key=private_key)

    def get_private_key(self, address: str, password: str):
        wallet = self.get(address=address)
        if wallet.user.check_password(password):
            data = self._signer.unsign_object(wallet.private_key)
            return data['private_key']


class Wallet(models.Model):
    address = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='wallets')
    private_key = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = WalletManager()
