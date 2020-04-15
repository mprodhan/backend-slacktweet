#!/usr/bin/env python3
"""A standalone Slack client implementation
see https://slack.dev/python-slackclient/
"""
from slack import RTMClient, WebClient
import os
import sys
from slack.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()

bot_user_token = os.environ["BOT_USER_TOKEN"]
client = WebClient(token=bot_user_token)

try:
  response = client.chat_postMessage(
    channel="#bot-test",
    text="Hello from your app! :tada:"
  )
except SlackApiError as e:
  assert e.response["error"]

BOT_NAME = "zuschauer-bot"

class SlackClient:
    def __init__(self, bot_user_token, bot_id=None):
        self.name = BOT_NAME
        self.bot_id = bot_id
        if not self.bot_id:
            response = WebClient(token=bot_user_token).api_call("auth.test")
            self.bot_id = response["user_id"]
            print(f"My bot_id is {self.bot_id}")
        
        self.sc = RTMClient(token=bot_user_token, run_async=True)
        RTMClient.run_on(event="hello")(self.on_hello)
        RTMClient.run_on(event="message")(self.on_message)
        RTMClient.run_on(event="goodbye")(self.on_goodbye)

        self.future = self.sc.start()
        self.at_bot = f"<@{self.bot_id}>"
        print("Created new SlackClient Instance")

    def on_hello(self, **payload):
        pass

    def on_message(self, **payload):
        pass 

    def on_goodbye(self, **payload):
        pass

    def run(self):
        print("Waiting fo things to happen...")
        loop = self.future.get_loop()
        loop.run_until_complete(self.future)
        print("Done3 waiting for things. DONE DONE!")

def main(args):
    slackclient = SlackClient(
        os.environ["BOT_USER_TOKEN"]
        # os.environ["BOT_USER_ID"]
    ).run()


if __name__ == '__main__':
    main(sys.argv[1:])
