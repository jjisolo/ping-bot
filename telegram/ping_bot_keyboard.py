from ping_bot_base import message_templates
from aiogram                import types

# 'MENU' message main keyboard
track_ip_start_inline_button = types.InlineKeyboardButton(message_templates["track-start"], callback_data='!track-ip-start')
track_ip_stop_inline_button  = types.InlineKeyboardButton(message_templates["track-stop"],  callback_data='!track-ip-stop')
track_ip_get_inline_button   = types.InlineKeyboardButton(message_templates["track-get"],   callback_data='!track-ip-get')

menu_inline_keyboard = types.InlineKeyboardMarkup()
menu_inline_keyboard.add(track_ip_start_inline_button)
menu_inline_keyboard.add(track_ip_stop_inline_button) 
menu_inline_keyboard.add(track_ip_get_inline_button)
