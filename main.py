import telebot
from rembg import remove
from PIL import Image
from pathlib import Path

api = telebot.TeleBot('TOKEN')

@api.message_handler(content_types=['photo'])
def handle_docs_document(message):
    Path(f'./input_img/{message.chat.id}/').mkdir(parents=True, exist_ok=True)
    

    file_info = api.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = api.download_file(file_info.file_path)
    src = f'./input_img/{message.chat.id}/' + message.photo[1].file_id.replace('photos/', '') + '.png'
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    Path(f'./output_img/{message.chat.id}/').mkdir(parents=True, exist_ok=True)
    input_path = src
    output_path = f'./output_img/{message.chat.id}/' + message.photo[1].file_id.replace('photos/', '') + '.png'

    input = Image.open(input_path)
    output = remove(input)
    output.save(output_path)

    photo = open(output_path, 'rb')
    api.send_document(message.chat.id, photo, caption='Ваше фото готово! <3')

api.polling()
