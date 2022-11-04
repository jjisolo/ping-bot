from ping_bot_base          import  ping_dispatcher, ping_bot, dev_logger, usr_logger, message_templates, log_meta
from ping_bot_keyboard      import  menu_inline_keyboard
from ping_bot_forms         import  track_ip_form, untrack_ip_form 

import aiogram, logging

                            ####### Process INLINE BUTTONS actions. ########
@ping_dispatcher.callback_query_handler(lambda c: c.data and c.data.startswith("!"))
async def process_inline_buttons_callbacks(callback_query: aiogram.types.CallbackQuery):
    match callback_query.data[1:]:
        case "track-ip-start":
            # Start tracking of an ip address.
            await track_ip_form.adress.set()
            dev_logger.info((log_meta["send_to"]  + "(START TRACK IP)" ).format(str(callback_query.from_user.id)))
            await ping_bot.send_message(callback_query.from_user.id, text=message_templates["track-start"])
        
        case "track-ip-stop":
            # Stop tracking ip address.
            await untrack_ip_form.address.set()
            dev_logger.info((log_meta["send_to"]  + "(UNTRACK  IP)" ).format(str(callback_query.from_user.id)))
            await ping_bot.send_message(callback_query.from_user.id, text=message_templates["track-end"])
        

                            ####### Track the IP-Address. ########
@pign_dispatcher.message_handler(state=track_ip_form.address) -> None:
async def process_tracked_ip_address(message: aiogram.types.message, state: FSMContext) -> None:
    """
    Process tracked id form.
    Engaged from '!track-ip-start' command.
    """
    
    # State routine.
    dev_logger.info((log_meta["start-action"]  + "(START IP TRACKING)" ).format(str(message.from_user.id)))
    await state.finish()
    
    # Database routine.



                            ####### Get MENU message  ########
@ping_dispatcher.message_handler(commands=["menu", "Menu", "MENU"])
async def command_start(message : aiogram.types.Message) -> None:
    """
    Send menu form to the user.
    """
    dev_logger.info((log_meta["send_to"]  + "(MENU command)" ).format(str(message.from_user.id)))
    await message.answer(message_templates["menu"], reply_markup=menu_inline_keyboard)


                            ####### Get START/HELP message  ########
@ping_dispatcher.message_handler(commands=["start", "help"])
async def command_start(message : aiogram.types.Message) -> None:
    """
    Send start message to the user.
    """
    dev_logger.info((log_meta["send_to"]  + " (START/HELP command)" ).format(str(message.from_user.id)))
    await message.answer(message_templates["help"])
