import telebot
import base64
import json

TOKEN = "8700350848:AAFjCmHteNFx2EldRGxtvEXfaRWxS9RsIk4"
ADMIN_ID = 8271084626

bot = telebot.TeleBot(TOKEN)

SERVERS = {
    "🇩🇪 آلمان": {"ip": "185.165.29.188", "port": 443, "uuid": "b1ebd5fc-9170-45d4-9887-a39c9fc65298"},
    "🇳🇱 هلند": {"ip": "146.190.10.150", "port": 443, "uuid": "b1ebd5fc-9170-45d4-9887-a39c9fc65298"},
    "🇺🇸 آمریکا": {"ip": "209.126.84.189", "port": 443, "uuid": "b1ebd5fc-9170-45d4-9887-a39c9fc65298"},
    "🇫🇷 فرانسه": {"ip": "152.228.162.19", "port": 443, "uuid": "b1ebd5fc-9170-45d4-9887-a39c9fc65298"},
    "🇹🇷 ترکیه": {"ip": "176.239.145.110", "port": 443, "uuid": "b1ebd5fc-9170-45d4-9887-a39c9fc65298"},
}

def make_vmess(ip, port, uuid, name):
    config = {
        "v": "2", "ps": name, "add": ip, "port": str(port),
        "id": uuid, "aid": "0", "net": "ws", "type": "none",
        "host": ip, "path": "/", "tls": "none"
    }
    return "vmess://" + base64.b64encode(json.dumps(config).encode()).decode()

@bot.message_handler(commands=['start'])
def start(msg):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    for country in SERVERS.keys():
        markup.add(telebot.types.InlineKeyboardButton(country, callback_data=country))
    bot.reply_to(msg, "🔥 **پنل بلیز**\nکشور مورد نظر رو انتخاب کن:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data in SERVERS)
def handle(call):
    country = call.data
    s = SERVERS[country]
    link = make_vmess(s["ip"], s["port"], s["uuid"], f"Blaze-{country}")
    bot.edit_message_text(
        f"✅ **سرور {country}**\n\n📍 IP: `{s['ip']}`\n🔌 پورت: {s['port']}\n\n🔗 **لینک کانفیگ:**\n`{link}`",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        parse_mode="Markdown"
    )

print("✅ بات پنل بلیز روشن شد!")
bot.infinity_polling()
