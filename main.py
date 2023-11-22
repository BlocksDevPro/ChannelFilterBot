import time
import asyncio
import config
from pyrogram import Client


with open('channelsList.txt', 'r') as f:
    channelsList = f.read().split('\n')


async def main():
    async with Client(config.PHONE_NUMBER, config.API_ID, config.API_HASH, phone_number=config.PHONE_NUMBER) as client:
        resultText = ''
        for channel in channelsList:
            channelUsername = '@' + \
                channel.replace('https://', '', 1).split('/')[1]
            print("Fetching channel :", channelUsername, '...')
            try:
                time.sleep(0.3)
                channelInfo = await client.get_chat(channelUsername)
            except Exception as telegram_error:
                if 'FLOOD_WAIT_X' in str(telegram_error):
                    waitingSeconds = str(telegram_error).split(
                        '-')[1].split()[3]
                    print('waiting', waitingSeconds,
                          'before trying next channel!')
                    time.sleep(float(waitingSeconds))
                else:
                    print(telegram_error)
            else:
                if channelInfo and channelInfo.linked_chat and str(channelInfo.linked_chat.type) == "ChatType.SUPERGROUP":
                    print("Fetched channel :", channelUsername,
                          'Discussion Group found.')
                    resultText += f"{channelUsername} : @{channelInfo.linked_chat.username}"
                else:
                    print("Fetched channel :", channelUsername,
                          'Discussion Group not found!')
        with open('resultChannels.txt', 'w') as f:
            f.write(resultText)


asyncio.run(main())
