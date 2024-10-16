from aiocryptopay import AioCryptoPay, Networks
import asyncio
import logging
import threading

class CryptoClient:
  def __init__(self, api_token) -> None:
    self.crypto_pay_ = AioCryptoPay(
      token = api_token,
      network = Networks.MAIN_NET)
    self.thread_ = threading.Thread(target=self._start_loop)
    self.thread_.start()

  def __del__(self):
    try:
      coroutine = self.crypto_pay_.close()
      return asyncio.run_coroutine_threadsafe(coroutine, self.loop_).result()
    except Exception as error:
      logging.error(f'Unable to close: {str(error)}')

    self.loop_.call_soon_threadsafe(self.loop_.stop)
    self.thread_.join()

  def _start_loop(self):
    self.loop_ = asyncio.new_event_loop()
    asyncio.set_event_loop(self.loop_)
    self.loop_.run_forever()

  def create_invoice(self, amount : float):
    try:
      coroutine = self.crypto_pay_.create_invoice(
        amount=amount, asset='USDT', currency_type='crypto',
        accepted_assets=['USDT', 'USDC', 'BTC', 'ETH', 'LTC', 'BNB', 'TRX', 'TON'])
      return asyncio.run_coroutine_threadsafe(coroutine, self.loop_).result()
    except Exception as error:
      logging.error(f'Unable to create invoice: {str(error)}')

    return None

  def delete_invoice(self, invoice_id):
    try:
      coroutine = self.crypto_pay_.delete_invoice(
        invoice_id = invoice_id)
      return asyncio.run_coroutine_threadsafe(coroutine, self.loop_).result()
    except Exception as error:
      logging.error(f'Unable to create invoice: {str(error)}')

    return None
