from __future__ import annotations

from aiogram import Bot, Dispatcher, F
from aiogram.filters import BaseFilter, Command
from aiogram.types import Message

from games_classes import GuessGame
from help_text import HELP_TEXT
from PRIVATE_INFO import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Словарь вида айди_пользователя : его игра
users_games: dict[str, GuessGame] = {}


class NumbersInMessage(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, list[int]]:
        numbers = []
        # Разрезаем сообщение по пробелам, нормализуем каждую часть, удаляя
        # лишние знаки препинания и невидимые символы, проверяем на то, что
        # в таких словах только цифры, приводим к целым числам
        # и добавляем их в список
        for word in message.text.split():
            normalized_word = word.replace('.', '').replace(',', '').strip()
            if normalized_word.isdigit():
                numbers.append(int(normalized_word))
        # Если в списке есть числа - возвращаем словарь со списком чисел по ключу 'numbers'
        if numbers:
            return {'numbers': numbers}
        return False


def get_game(message: Message) -> GuessGame:
    """получить игру отправителя сообщения, если ее нет, то создать ее и поместить
    в словарь users_games"""
    game: GuessGame = users_games.setdefault(str(message.from_user.id), GuessGame())
    return game


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\n' 'Меня зовут Угадай-Число-Бот!\n' 'Чтоб ознакомиться с правилами отправь /help \n' 'Сыграем?'
    )


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=HELP_TEXT, parse_mode="MarkdownV2")


@dp.message(Command(commands='stats'))
async def process_stats_command(message: Message):
    game: GuessGame = get_game(message)
    await message.answer(game.stats())


@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    game: GuessGame = get_game(message)
    game.cancell_game()
    await message.reply("Игра отменена, чтоб начать снова напишите 'да','сыграем' или 'начнем'")


@dp.message(F.text.lower().startswith("найди числа"), NumbersInMessage())
async def process_if_numbers(message: Message, numbers: list[int]):
    await message.answer(text=f"Нашел: {", ".join(str(num) for num in numbers)}")


@dp.message(F.text.lower().startswith('найди числа'))
async def process_if_not_numbers(message: Message):
    await message.answer(text='Не нашел что-то :(')


@dp.message(F.text)
async def process_game_messages(message: Message):
    message_text: str | int = message.text.lower()
    game: GuessGame = get_game(message)

    if message_text in ["да", "конечно", "давай", 'сыграем']:
        await message.reply(game.start_game())

    elif message_text in ["нет", "не сейчас"]:
        await message.reply("Жаль ;(")

    elif message_text.isdigit():
        await message.reply(game.trie_to_guess(int(message_text)))

    else:
        await message.reply(
            "Извините, я не понимаю что это значит.\n" "воспользуйся командой /help, чтоб узнать правила"
        )


if __name__ == '__main__':
    dp.run_polling(bot)
