import string
import csv
from sys import stdout, exit
from time import sleep
import re
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty


def main():
    api_access_answer = input('\nTelegram APIsine kaydınız var mı? e/h: ')

    if api_access_answer != 'e':
        print('\nŞuradan Telegram APIsi için başvurunuz: https://core.telegram.org/api/obtaining_api_id#obtaining-api-id')
        print('\nAPI ID ve hash aldıktan sonra geri dönüp programı tekrar çalıştırınız\n')
        exit(1)

    print('\nAPI bilgilerizi giriniz. Yanlış girerseniz program hata verecektir\n')

    api_id = input('API ID: ')
    api_hash = input('API Hash: ')
    phone = input('Telegram hesabınızın bağlı olduğu telefon numarası (başında + ve ülke kodu ile, boşluksuz): ')

    client = TelegramClient(phone, api_id, api_hash)
    client.connect()

    if not client.is_user_authorized():
        client.send_code_request(phone)
        auth_code = input('\nTelegramına kod attım, girer misin yavrum: ')
        client.sign_in(phone, auth_code)

    result = client(
        GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=200,
            hash = 0,
        ))

    print('')

    for group_idx, group in enumerate(result.chats):
        print(str(group_idx).rjust(3) + '  ' +  group.title)

    selected_group_idx = \
        input('\nİstediğin grubun nosunu girer misin canım: ')

    target_group = result.chats[int(selected_group_idx)]

    participants = {}

    print('')

    for char in list(string.ascii_lowercase + string.digits):
        print('İçinde "' + char + '" geçen kullanıcılar çekiliyor...')

        for p in client.get_participants(target_group, search=char):
            participants[p.id] = p

        sleep(2)

    print('\nRaporunuz hazırdır. İşbu rapor çekim talebinizi onaylamak için 15 saniye içinde "Şemsi Paşa pasajında sesi büzüşesiceler" ifadesini tersten yazmanız gerekmektedir.')
    print('\nSize verilen süre içinde yazamamanız halinde Telegramınız ÇÖKECEKTİR.')

    sleep(15)

    print('\nŞAKA ŞAKA... EHEHE. Entera basman yeterli..\n')

    input()

    writer = csv.writer(stdout, delimiter=',', lineterminator='\n')

    writer.writerow(['username', 'name', 'surname', 'id'])

    for p in sorted(participants.values(), key=lambda p: str(p.username).lower()):
        writer.writerow([p.username, p.first_name, p.last_name, p.id])

    print('\nKopyalayıp münasip yere yapıştırabilirsin. Rica ederim.....\n')


main()
