import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен из переменных окружения
BOT_TOKEN = os.environ['BOT_TOKEN']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"👋 Привет, {user.first_name}! Я бот-модератор.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📚 Команды:
/start - Запуск бота
/help - Помощь  
/ping - Проверка работы
/ban - Бан пользователя
/staff - Список администраторов
/info - Информация о пользователе

💡 Для бана ответьте на сообщение пользователя!
    """
    await update.message.reply_text(help_text)

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Понг! Бот работает.")

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Ответьте на сообщение пользователя!")
        return
    
    target_user = update.message.reply_to_message.from_user
    try:
        await update.effective_chat.ban_user(target_user.id)
        await update.message.reply_text(f"🛑 Пользователь {target_user.first_name} забанен!")
    except Exception as e:
        await update.message.reply_text("❌ Ошибка! Проверьте права бота.")

async def staff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat = update.effective_chat
        admins = await chat.get_administrators()
        
        staff_list = "👥 Администраторы чата:\n\n"
        for admin in admins:
            user = admin.user
            status = "👑 Создатель" if admin.status == 'creator' else "⭐ Администратор"
            username = f"@{user.username}" if user.username else user.first_name
            staff_list += f"• {username} - {status}\n"
        
        await update.message.reply_text(staff_list)
    except Exception as e:
        await update.message.reply_text("❌ Ошибка при получении списка администраторов.")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user
    else:
        target_user = update.effective_user
    
    user_info = f"""
📊 Информация о пользователе:

• Имя: {target_user.first_name or 'Не указано'}
• Фамилия: {target_user.last_name or 'Не указана'} 
• Username: @{target_user.username or 'Не указан'}
• ID: {target_user.id}
    """
    await update.message.reply_text(user_info)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("ban", ban))
    application.add_handler(CommandHandler("staff", staff))
    application.add_handler(CommandHandler("info", info))
    
    print("=" * 50)
    print("🤖 Бот запущен на Railway!")
    print("🌐 Теперь он работает 24/7")
    print("📱 Тестируйте команды в Telegram")
    print("=" * 50)
    
    application.run_polling()

if __name__ == '__main__':
    main()
