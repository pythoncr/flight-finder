from telethon.sync import TelegramClient, events

api_id = "2343814"
api_hash = " bddb188b93d630690c6f7b0cebe104d5 "

with TelegramClient('name', api_id, api_hash) as client:
   client.send_message('me', 'Hello, myself!')
   print(client.download_profile_photo('me'))

   @client.on(events.NewMessage(pattern='(?i).*Hello'))
   async def handler(event):
      await event.reply('Hey!')

   client.run_until_disconnected()
