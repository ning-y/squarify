import io, logging
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from squarify import squarify

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Bot(Updater):
    def __init__(self, *, token):
        super().__init__(token=token, use_context=True)
        self.dispatcher.add_handler(
                MessageHandler(
                    Filters.document.image | Filters.photo,
                    self.handle_image_documents))
        logger.info('Bot initialised.')

    @staticmethod
    def handle_image_documents(update, context):
        user = update.effective_user
        logger.info('Handling request from @{} ({})'.format(
                user.username, user.id))

        infile = io.BytesIO()
        attachment = update.effective_message.effective_attachment
        # if Filters.photo, attachment is list of PhotoSize's
        attachment = attachment[-1] if type(attachment) == list else attachment
        attachment.get_file().download(out=infile)
        infile.seek(0)

        outfile = squarify(infile)
        outfile.seek(0)

        update.effective_chat.send_document(
                outfile,
                reply_to_message_id=update.effective_message.message_id)

