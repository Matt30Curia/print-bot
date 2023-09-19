from pprint import pprint
import telepot
from telepot.loop import MessageLoop
from pylovepdf.tools.imagetopdf import ImageToPdf
from time import sleep
import os

TOKEN = "your telegram token"
TOKEN_PDF = "your ILove PDF token"
DIR= "C:\\ your directory where you are going to save the files "



def handle(msg) -> None:

    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == "document":
        print_file(msg)
        pprint(msg)
    elif content_type == "photo":
        print_photo(msg)
        pprint(msg)
    else:
        bot.sendMessage(chat_id, "il file che hai inviato non è supportato")

def print_file(msg) -> None:
    
    file_id = msg["document"]["file_id"]
    
    file_path = get_file_path(msg)

    bot.download_file(file_id, file_path)
    os.startfile(file_path, "print")

                 
def get_file_path(msg) -> str:
    file_name = msg["document"]["file_name"]
    if file_name[-3:] == "odx":
        return DIR + "docx.docx"
    return DIR + f"{file_name[-3:]}.{file_name[-3:]}"
    
                 
def print_photo(msg) -> None:
    photo_id = msg["photo"][-1]["file_id"]
    photo_path = get_photo_path(msg)
    bot.download_file(photo_id, photo_path)
    photo_path = img_to_pdf()
    os.startfile(DIR + photo_path, "print")

def get_photo_path(msg) -> str:
    return DIR + "pdf.jpg"

def img_to_pdf():
    t = ImageToPdf(TOKEN_PDF, verify_ssl=True, proxies = '')
    t.add_file(DIR + 'pdf.jpg')
    t.debug = False
    t.orientation = 'portrait'
    t.margin = 0
    t.pagesize = 'fit'
    t.set_output_folder(DIR)

    t.execute()
    path =t.download() 
    t.delete_current_task()
    return path

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)



while 1:
    sleep(2)
    
