"""
ChainLink bot for the RightToMove Discord
Code contributors: Koa Wells koa.wells@hotmail.com
"""
import logging
import smtplib
import discord
import csv
from discord.ext import commands
from email.mime.text import MIMEText
from email.utils import formataddr
from zoneinfo import ZoneInfo

from config import CONF
from logger import setup_logger

class ChainLink(commands.Bot):
  """
  ChainLink class
  """
  def __init__(self):
    """
    Default constructor - sets up the discord bot and logging
    """
    intents = discord.Intents.default()
    intents.message_content = True
    super().__init__(command_prefix='!', intents=intents)
    setup_logger()

    with open(CONF.RECIPIENTS_FILE, encoding="utf-8") as csv_file:
      reader = csv.reader(csv_file)
      # unpacks the recipients list into a list of emails
      self.recipients = [email.strip() for email in next(reader) if email.strip()]
    self.email_footer = ('\n'
                         '--\n'
                         'This email originates from the RTM volunteer Discord server. Attachments, emojis, and reactions '
                         'are not visible here, but can be seen on the Discord server.')

  def send_email(self, subject, body):
    """
    Sends Discord message as email to the emailing list
    :param subject: Subject of the email containing the Discord channel where the message was sent
    :param body: Body of the message sent in the Discord server
    :return: None
    """
    email = MIMEText(body)
    email['Subject'] = subject
    email['From'] = formataddr(('ChainLink Discord Bot ⚙️', CONF.EMAIL))
    email['To'] = 'undisclosed-recipients:;'
    with smtplib.SMTP_SSL(CONF.SMTP_SERVER, CONF.SMTP_PORT) as smtp_server:
      smtp_server.login(CONF.EMAIL, CONF.EMAIL_PASSWORD)
      smtp_server.sendmail(CONF.EMAIL, self.recipients, email.as_string())
    print('Message sent')

  async def on_ready(self):
    """
    Prints successful connection message once the ChainLink bot has logged in.
    :return: none
    """
    logging.info(f'We have logged in as {self.user}')

  async def on_message(self, message: discord.Message):
    """
    On message listener for when a message is sent in the Discord server
    :param message: Message from the Discord server
    :return: None
    """
    discord_user = message.author
    discord_user_nickname = message.author.display_name
    channel = message.channel
    posted_message = message.content
    # gets datetime object of when the message was sent and converts it from UTC to EST
    created_at = message.created_at.astimezone(ZoneInfo("America/Montreal"))
    date = f'{created_at.year}/{created_at.month}/{created_at.day}'
    time = f'{created_at.hour}:{created_at.minute}'
    logging.info(f'Discord username of sender: {discord_user} \n'
                 f'Server nickname of sender: {discord_user_nickname} \n'
                 f'Channel where message was sent: {channel} \n'
                 f'Message content: {posted_message}')

    subject = f'[rtmlvlvolunteers] discussion in #{channel} by {discord_user_nickname}'
    body = (f'From {discord_user_nickname} via Discord on {date} at {time} EST\n'
            f'\n'
            f'{posted_message}'
            f'{self.email_footer}')

    self.send_email(subject, body)

if __name__ == '__main__':
  bot = ChainLink()
  bot.run(CONF.DISCORD_TOKEN)