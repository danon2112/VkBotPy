import vk_api
from vk_api import longpoll
from vk_api.bot_longpoll import VkBotEvent, VkBotEventType, VkBotLongPoll


def write_msg(chat_id, message):
    vk.method('messages.send', {'chat_id': chat_id, 'message': message, 'random_id': 0})

def user_kick(chat_id, user_id):
    vk.method('messages.removeChatUser', {'chat_id': chat_id, 'member_id': user_id, 'user_id': user_id})


token = "You token"
group_id = 'You group ID'


vk = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk, group_id=group_id)

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_chat:
            message = event.message
            text = event.message.text
            action = message.get('action') # Получаем объект action из объекта message

            # Если есть объект action:
            if action:
                # Проверяем тип действия, исключаем юзера
                if action['type'] == 'chat_kick_user':
                    write_msg(event.chat_id, f'[id{action['member_id']}|Пользователь] вышел.')
                    user_kick(event.chat_id, action['member_id'])

            # Команда остановки бота
            if text == '/stop':
                write_msg(event.chat_id, '✅ | Бот выключен')
                print('Bot off')
                break
