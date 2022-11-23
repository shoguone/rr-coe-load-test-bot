from locust import HttpUser, task, between

from bot_client import BotClient
from signalr_hub_user import SignalRHubUser
from users_pool import UsersPool

class BotUser(HttpUser, SignalRHubUser):
    wait_time = between(1, 5)

    users_pool = UsersPool()

    @task
    def run_bot(self):
        print('run_bot ', self.login_data['email'])
        self.bot = BotClient(self.host, self.login_data, self.client, self)
        self.bot.start()
        print('finish bot', self.login_data['email'])

    def on_start(self):
        email = BotUser.users_pool.get_email()
        password = 'vovaa'

        print(email)

        self.login_data = {
            'email': email,
            'password': password
        }

    def on_stop(self):
        self.bot.stop()
        return super().on_stop()
