import re
import time
from typing import Callable
from locust import User
from signalrcore.hub_connection_builder import HubConnectionBuilder


class SignalRHubUser(User):
    abstract = True

    windows_tick = 10000000
    sec_to_unix_epoch = 11644473600
    timestamp_pattern = re.compile('"UtcTimeStamp":(\d+)')

    def send(self, method, body, *args, **kwargs):
        body_str = str(body)

        time_start = time.time()
        send_result = self.hub.send(method, body, *args, **kwargs)
        time_delta = time.time() - time_start

        self.environment.events.request.fire(
            request_type="WSS",
            name=method,
            response_time=time_delta * 1000,
            response_length=len(body_str),
            exception=None,
            context=self.context(),
        )

        return send_result

    def on(self, event, callback: Callable):
        self.hub.on(event, lambda msg: self.__handle_message(event, msg, callback))

    def __handle_message(self, message_name, message, callback):
        message_str = str(message)
        time_sent = self.__extract_timestamp_from_message(message_str)
        time_delta = time.time() - time_sent \
            if time_sent is not None \
            else 0

        self.environment.events.request.fire(
            request_type="WSR",
            name=message_name,
            response_time=time_delta * 1000,
            response_length=len(message_str),
            exception=None,
            context=self.context(),
        )

        callback(message)

    # handler = logging.StreamHandler()
    # handler.setLevel(logging.DEBUG)
    def connect_to_hub(self, url, access_token = None):
        access_token = self.access_token if access_token == None else access_token
        hub = HubConnectionBuilder()\
            .with_url(url, options={
                "access_token_factory": lambda: access_token,
                "verify_ssl": False
            }) \
            .with_automatic_reconnect({
                "type": "interval",
                "keep_alive_interval": 10,
                "intervals": [1, 3, 5, 6, 7, 87, 3]
            }) \
            .build()
            # .configure_logging(logging.DEBUG, socket_trace=True, handler=handler)

        self.hub = hub
        return hub

    def __extract_timestamp_from_message(self, message_str):
        matches = SignalRHubUser.timestamp_pattern.search(message_str)
        if matches is None:
            return None
        windows_time_sent = int(matches.groups()[0])
        time_sent = (windows_time_sent / SignalRHubUser.windows_tick) - SignalRHubUser.sec_to_unix_epoch
        return time_sent
