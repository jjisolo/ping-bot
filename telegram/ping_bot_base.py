import os, aiogram, logging, json, warnings

WARNING_CRITICAL_HIT = "The program experienced critical error. Consider seeing log/dev_log.log to identify the error."

DEV_LOGGER_LOG_FILE_PATH = "logs/dev-logs.log"
USR_LOGGER_LOG_FILE_PATH = "logs/usr-logs.log"

logging.basicConfig(
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt='%H:%M:%S'
)

dev_logger = logging.getLogger("DevLogger")
usr_logger = logging.getLogger("UsrLogger")

dev_logger.setLevel(logging.DEBUG)
usr_logger.setLevel(logging.INFO)

dev_fh = logging.FileHandler(DEV_LOGGER_LOG_FILE_PATH)
dev_fh.setLevel(logging.DEBUG)

usr_fh  = logging.FileHandler(USR_LOGGER_LOG_FILE_PATH)
dev_fh.setLevel(logging.INFO)

dev_logger.addHandler(dev_fh)
usr_logger.addHandler(usr_fh)

ping_bot         = aiogram.Bot(token=str(os.getenv("PINGBOT_KEY")), parse_mode="HTML")
ping_dispatcher  = aiogram.Dispatcher(ping_bot)

with open("resource/message_templates.json") as json_file:
    message_templates = json.load(json_file)

with open("resource/message_log_meta.json") as json_file:
    log_meta          = json.load(json_file)

def commit_critical_error(log_message: str) -> None:
    dev_logger.critical(log_message)
    warnings.warn(WARNING_CRITICAL_HIT, RuntimeWarning)
    raise SystemExit # TODO register exit call in exit-chain?            


   

