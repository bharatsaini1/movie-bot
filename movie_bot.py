import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from groq import AsyncGroq

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize the asynchronous Groq client
GROQ_API_KEY = "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"  # Replace with your actual Groq API key
client = AsyncGroq(api_key=GROQ_API_KEY)

# System prompt for the chatbot
movie_prompt = (
    "You are a chatbot that only talks about movies. "
    "Answer the user's questions about movies, provide movie recommendations, trivia, or anything related to movies."
)

# Initialize conversation history
conversation_history = [{"role": "system", "content": movie_prompt}]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the /start command is issued."""
    await update.message.reply_text("🎬 Hi! I'm your Movie Chatbot. Ask me anything about movies!")

async def generate_response(user_message: str) -> str:
    """Generate a response from the Groq API."""
    try:
        conversation_history.append({"role": "user", "content": user_message})
        chat_completion = await client.chat.completions.create(
            messages=conversation_history,
            model="llama3-8b-8192",
        )
        response = chat_completion.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": response})
        return response
    except Exception as e:
        logger.error(f"Error interacting with Groq API: {e}")
        return "I'm sorry, something went wrong. Please try again later."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages from users."""
    user_message = update.message.text
    bot_response = await generate_response(user_message)
    await update.message.reply_text(bot_response)

def main() -> None:
    """Start the bot."""
    TELEGRAM_BOT_TOKEN = "7591081971:AAGa7ymnJCDCJFFlhvIdh8oQOzU0B8-OOP0"  # Replace with your actual Telegram Bot Token

    # Create the Application and pass it your bot's token
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Register the /start command handler
    application.add_handler(CommandHandler("start", start))

    # Register the message handler for text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until you press Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()
