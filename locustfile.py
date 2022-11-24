from locust import HttpUser, task, between
import logging
import urllib3

from bot_client import BotClient
from config import Config
from signalr_hub_user import SignalRHubUser
from users_pool import UsersPool

urllib3.disable_warnings()

class BotUser(HttpUser, SignalRHubUser):
    wait_time = between(1, 5)

    users_pool = UsersPool()

    @task
    def run_bot(self):
        self.logger.info('run_bot %s', self.login_data)
        self.bot = BotClient(self.host, self.login_data, self.client, self)
        self.bot.start()
        self.logger.info('finish bot %s', self.login_data)
        self.environment.runner.quit()

    def on_start(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(Config.logging_level)
        if Config.use_debug_auth:
            self.login_data = {
                'authToken': '9oB6HP6FVYVH'
            }
        else:
            email = BotUser.users_pool.get_email()
            password = 'vovaa'
            self.login_data = {
                'email': email,
                'password': password
            }

    def on_stop(self):
        self.bot.stop()
        return super().on_stop()
