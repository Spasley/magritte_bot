import requests
import datetime
import sys


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = 'https://api.telegram.org/bot{}/'.format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        payload = {'timeout': timeout, 'offset': offset}
        response = requests.get(self.api_url + method, data=payload)
        result_json = response.json()['result']
        return result_json

    def get_last_update(self):
        updates = self.get_updates()
        print('updates ' + str(updates) + '\n------------------')
        if len(updates) > 0:
            last_update = updates[-1]
        else:
            last_update = None
        return last_update

    def send_message(self, chat_id, text):
        method = 'sendMessage'
        payload = {'chat_id': chat_id, 'text': text}
        response = requests.post(self.api_url + method, data=payload)
        print(response.text  + '\n------------------')
        return response

token = sys.argv[1]
greet_bot = BotHandler(token)
greetings = ('hello', 'bonjour', 'privet')
now = datetime.datetime.now()


def main():
    new_offset = None
    today = now.day
    hour = now.hour
    
    while True:
        greet_bot.get_updates(new_offset)
            
        last_update = greet_bot.get_last_update()
            
        if last_update is not None:
            print('last_update ' + str(last_update) + '\n------------------')

            last_update_id = last_update['update_id']
            print('last_update_id ' + str(last_update_id) + '\n------------------')
            last_chat_text = last_update['message']['text']
            print('last_chat_text ' + last_chat_text + '\n------------------')
            last_chat_id = last_update['message']['chat']['id']
            print('last_chat_id ' + str(last_chat_id) + '\n------------------')
            last_chat_name = last_update['message']['chat']['first_name']
            print('last_chat_name ' + last_chat_name + '\n------------------')

            if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
                greet_bot.send_message(last_chat_id, 'Good morning, {}'.format(last_chat_name))
                today += 1

            elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
                greet_bot.send_message(last_chat_id, 'Good day, {}'.format(last_chat_name))
                today += 1

            elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
                greet_bot.send_message(last_chat_id, 'Good evening, {}'.format(last_chat_name))
                today += 1

            new_offset = last_update_id + 1
            print('new_offset ' + str(new_offset) + '\n------------------')
        

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()