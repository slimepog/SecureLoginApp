from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import database

def chatbot_init():
    chatbot = ChatBot(
        'MyBot',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///chatbot_db.sqlite3'
    )
    trainer = ChatterBotCorpusTrainer(chatbot)
    # trains on known training db in english
    trainer.train("chatterbot.corpus.english")
    return chatbot

def send_message_to_bot(message, bot, username):
    bot_reponse = str(bot.get_response(message))
    database.add_conversation(message, bot_reponse, username)
    return {"response": bot_reponse}