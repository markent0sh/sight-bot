from aiohttp import web
from aiocryptopay import AioCryptoPay, Networks
from aiocryptopay.models.update import Update
import logging
import os
import sys

sys.path.append(
  os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '../'))

import config
from mongo.user import UserDB
from mongo.invoice import InvoiceDB

logging.basicConfig(
  filename = '/root/logs/crypto-webhook.log',
  filemode = 'a',
  level = logging.INFO,
  format = '%(name)s - %(levelname)s - %(message)s'
)

class CryptoHook:
  def __init__(self) -> None:
    self.client_ = AioCryptoPay(token=config.CRYPTO_API_TOKEN, network=Networks.MAIN_NET)
    self.user_db_client_ = UserDB()
    self.invoice_db_client_ = InvoiceDB()

    self.client_.register_pay_handler(self.invoice_paid)

  def run(self):
    web_app = web.Application()
    web_app.add_routes([web.post('/mish-go-wkaes-apotom-vdoty', self.client_.get_updates)])
    web_app.add_routes([web.post('/test-route', self._test_route)])
    web_app.on_shutdown.append(self.shutdown)
    web.run_app(app=web_app, host='127.0.0.1', port=config.CRYPTO_WEBHOOK_PORT)

  async def shutdown(self, app) -> None:
    await self.client_.close()

  async def invoice_paid(self, update: Update, app) -> None:
    paid_invoice = update.payload
    logging.info(f'CryptoHook :: New paid invoice: {paid_invoice}')

    if None != paid_invoice:
      try:
        local_invoice = self.invoice_db_client_.get_invoice(paid_invoice.invoice_id)
        logging.info(f'>>> Found invoice, uid: {local_invoice.user_id_}, iid: {local_invoice.invoice_id_}, paid: {local_invoice.paid_}')

        if(None is not local_invoice and False == local_invoice.paid_):
          user = self.user_db_client_.get_user(local_invoice.user_id_)

          if(None is not user):
            top_up_amount = paid_invoice.paid_amount * config.DIAMOND_EXCHANGE_RATE

            logging.info(f'>>> Found user, ID: {user.user_id_}, Beneficiary ID: {user.beneficiary_}')
            logging.info(f'>>> Top up amount: {top_up_amount}, current balance: {user.balance_}')

            self.user_db_client_.update_user_balance(user.user_id_, user.balance_ + top_up_amount)
            self.invoice_db_client_.update_status(local_invoice.invoice_id_, True)

            beneficiary = self.user_db_client_.get_user(user.beneficiary_)

            if(None is not beneficiary):
              ben_top_up_amount = round(top_up_amount / 10, 2)
              logging.info(f'>>> Beneficiary {beneficiary.user_id_} bonus amount: {ben_top_up_amount}')
              self.user_db_client_.update_user_balance(
                beneficiary.user_id_, beneficiary.balance_ + ben_top_up_amount)

              for ref in beneficiary.referrals_.referrals_:

                if ref['id'] == user.user_id_:
                  ref['bonuses'] += ben_top_up_amount
                  break

              self.user_db_client_.update_referrals(
                beneficiary.user_id_, beneficiary.referrals_.referrals_)

          else:
            logging.error(f'>>> User {local_invoice.user_id_} not found')

        else:
          logging.error(f'>>> Invoice {paid_invoice.invoice_id} not found')

      except Exception as error:
        logging.error(f'Unable to process invoice {paid_invoice}, error: {str(error)}')

  def _test_route(self, request):
    logging.info(f'_test_route: {request}')
    return web.Response(text="Test route successful", status=200)

def main():
  hook = CryptoHook()
  hook.run()

if __name__ == "__main__":
  main()
