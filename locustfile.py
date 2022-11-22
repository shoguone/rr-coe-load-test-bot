from locust import User, task, between

from app import App
from users_pool import UsersPool

class MyUser(User):
    wait_time = between(1, 5)

    users_pool = UsersPool()

    def __init__(self, environment):
        super().__init__(environment)
        self.stop = False

    @task
    def run_bot(self):
        print('run_bot')
        app = App(self.login_data)
        app.start()
        print('finish bot')

    def on_start(self):
        email = MyUser.users_pool.get_email()
        password = 'vovaa'

        print(email)

        self.login_data = {
            'email': email,
            'password': password
        }
