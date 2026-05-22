import re
import os
from os import environ, getenv
from Script import script

# ─────────────────────────────────────────
#  Helper
# ─────────────────────────────────────────
id_pattern = re.compile(r'^.\d+$')

def is_enabled(value, default):
    if str(value).lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif str(value).lower() in ["false", "no", "0", "disable", "n"]:
        return False
    return default


# ═══════════════════════════════════════════════════════════
#  1. TELEGRAM API CREDENTIALS
#     Get these from https://my.telegram.org
# ═══════════════════════════════════════════════════════════
API_ID    = int(environ.get('API_ID', ''))      # Integer ID from my.telegram.org
API_HASH  = environ.get('API_HASH', '')          # Hash string from my.telegram.org
BOT_TOKEN = environ.get('BOT_TOKEN', '')         # Token from @BotFather
SESSION   = environ.get('SESSION', 'Mai_Fuyuki') # Session file name (any string)


# ═══════════════════════════════════════════════════════════
#  2. MONGODB DATABASE
# ═══════════════════════════════════════════════════════════
DATABASE_URI  = environ.get('DATABASE_URI', '')             # MongoDB connection string
DATABASE_NAME = environ.get('DATABASE_NAME', 'Cluster0')    # Database name
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Mai_Fuyuki_files')  # Collection for indexed files

# Second database (only used when MULTIPLE_DB = True)
MULTIPLE_DB   = is_enabled(os.environ.get('MULTIPLE_DB', 'False'), False)
DATABASE_URI2 = environ.get('DATABASE_URI2', '')            # Second MongoDB URI

if not MULTIPLE_DB:
    DATABASE_URI2 = DATABASE_URI  # Falls back to primary DB


# ═══════════════════════════════════════════════════════════
#  3. ADMIN & OWNER
# ═══════════════════════════════════════════════════════════
ADMINS = [
    int(admin) if id_pattern.search(admin) else admin
    for admin in environ.get('ADMINS', '634637418').split()
]  # Space-separated Telegram user IDs of bot admins

auth_users = [
    int(user) if id_pattern.search(user) else user
    for user in environ.get('AUTH_USERS', '').split()
]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []

PREMIUM_USER = [
    int(user) if id_pattern.search(user) else user
    for user in environ.get('PREMIUM_USER', '').split()
]  # Hardcoded premium users (space-separated IDs)


# ═══════════════════════════════════════════════════════════
#  4. CHANNELS & GROUPS
#     All IDs must start with -100 (e.g. -1001234567890)
#     Bot must be admin in all these channels/groups.
# ═══════════════════════════════════════════════════════════
CHANNELS = [
    int(ch) if id_pattern.search(ch) else ch
    for ch in environ.get('CHANNELS', '-100').split()
]  # Source channels — files are auto-indexed from here

LOG_CHANNEL    = int(environ.get('LOG_CHANNEL', '-100'))    # Bot activity log channel
BIN_CHANNEL    = int(environ.get('BIN_CHANNEL', '-100'))    # File storage channel (keep private)
PREMIUM_LOGS   = int(environ.get('PREMIUM_LOGS', '-100'))   # Premium purchase log channel

DELETE_CHANNELS = [
    int(dch) if id_pattern.search(dch) else dch
    for dch in environ.get('DELETE_CHANNELS', '-100').split()
]  # Files deleted from these channels are also deleted from bot DB

INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))  # Channel for index requests

support_chat_id  = environ.get('SUPPORT_CHAT_ID', '-100')
reqst_channel    = environ.get('REQST_CHANNEL_ID', '-100')

SUPPORT_CHAT    = environ.get('SUPPORT_CHAT', 'https://t.me/')       # Support group public link
SUPPORT_CHAT_ID = int(support_chat_id) if support_chat_id and id_pattern.search(support_chat_id) else None
REQST_CHANNEL   = int(reqst_channel) if reqst_channel and id_pattern.search(reqst_channel) else None


# ═══════════════════════════════════════════════════════════
#  5. FORCE SUBSCRIBE (FSUB)
#     Users must join these channels to use the bot.
#     Bot must be admin with invite link permission.
# ═══════════════════════════════════════════════════════════
auth_req_channels = environ.get('AUTH_REQ_CHANNELS', '-100')  # Request-to-join channels (restricted)
auth_channels     = environ.get('AUTH_CHANNELS', '-100')       # Normal force-sub channels

AUTH_REQ_CHANNELS = [int(ch) for ch in auth_req_channels.split() if ch and id_pattern.match(ch)]
AUTH_CHANNELS     = [int(ch) for ch in auth_channels.split() if ch and id_pattern.match(ch)]

FSUB_PICS = environ.get(
    'FSUB_PICS',
    'https://graph.org/file/7478ff3eac37f4329c3d8.jpg https://graph.org/file/56b5deb73f3b132e2bb73.jpg'
).split()  # Images shown in force-sub prompt (space-separated URLs)


# ═══════════════════════════════════════════════════════════
#  6. LINKS — Update these with your own!
# ═══════════════════════════════════════════════════════════
GRP_LNK        = environ.get('GRP_LNK', 'https://t.me/')          # Your support group link
OWNER_LNK      = environ.get('OWNER_LNK', 'https://t.me/')        # Your Telegram profile link
UPDATE_CHNL_LNK = environ.get('UPDATE_CHNL_LNK', 'https://t.me/') # Your update channel link


# ═══════════════════════════════════════════════════════════
#  7. IMAGES & MEDIA
#     Replace these URLs with your own images.
# ═══════════════════════════════════════════════════════════
PICS_URL     = environ.get('PICS', 'https://api.aniwallpaper.workers.dev/random?type=girl').split()
PICS         = environ.get('PICS', 'https://graph.org/file/56b5deb73f3b132e2bb73.jpg').split()
NOR_IMG      = environ.get('NOR_IMG',      'https://graph.org/file/e20b5fdaf217252964202.jpg')  # Normal search result image
MELCOW_PHOTO = environ.get('MELCOW_PHOTO', 'https://graph.org/file/56b5deb73f3b132e2bb73.jpg')  # Welcome photo for new users
SPELL_IMG    = environ.get('SPELL_IMG',    'https://graph.org/file/13702ae26fb05df52667c.jpg')   # Spell-check suggestion image
SUBSCRIPTION = environ.get('SUBSCRIPTION', 'https://graph.org/file/242b7f1b52743938d81f1.jpg')  # Subscription/premium image
VERIFY_IMG   = environ.get('VERIFY_IMG',   'https://telegra.ph/file/9ecc5d6e4df5b83424896.jpg') # Verification image


# ═══════════════════════════════════════════════════════════
#  8. STREAM / DOWNLOAD SERVER
#     Set FQDN to your Render/VPS/Heroku domain.
#     Example: mai-fuyuki-hwnb.onrender.com
# ═══════════════════════════════════════════════════════════
PORT           = int(environ.get('PORT', '8080'))
NO_PORT        = is_enabled(environ.get('NO_PORT', 'True'), True)   # Set True for Render/Heroku (no port in URL)
BIND_ADRESS    = str(getenv('WEB_SERVER_BIND_ADDRESS', '0.0.0.0'))
HAS_SSL        = is_enabled(getenv('HAS_SSL', 'True'), True)        # Set True if your domain has HTTPS

APP_NAME = None
if 'DYNO' in environ:
    ON_HEROKU = True
    APP_NAME  = str(getenv('APP_NAME'))
else:
    ON_HEROKU = False

# Priority: FQDN env var → Heroku APP_NAME → Render default
FQDN = (
    getenv('FQDN')
    or (APP_NAME + '.herokuapp.com' if ON_HEROKU and APP_NAME else None)
    or 'mai-fuyuki-qvti.onrender.com'  # your Render domain
)

if HAS_SSL:
    URL = "https://{}/".format(FQDN)
else:
    URL = "http://{}/".format(FQDN)

STREAM_MODE         = is_enabled(environ.get('STREAM_MODE', 'True'), True)   # Enable watch/download links
PREMIUM_STREAM_MODE = is_enabled(environ.get('PREMIUM_STREAM_MODE', 'False'), False)  # Restrict stream to premium users only

SLEEP_THRESHOLD = int(environ.get('SLEEP_THRESHOLD', '60'))
WORKERS         = int(environ.get('WORKERS', '4'))
PING_INTERVAL   = int(environ.get('PING_INTERVAL', '1200'))  # Keep-alive ping interval in seconds
SESSION_NAME    = str(environ.get('SESSION_NAME', 'Mai_Fuyuki'))
MULTI_CLIENT    = False
name            = str(environ.get('name', 'Mai_Fuyuki'))


# ═══════════════════════════════════════════════════════════
#  9. TMDB / IMDB INTEGRATION
#     Get your TMDB API key: https://www.themoviedb.org/settings/api
# ═══════════════════════════════════════════════════════════
TMDB_API_KEY      = environ.get('TMDB_API_KEY', '')                      # Your TMDB API key (recommended)
DREAMXBOTZ_IMAGE_FETCH = is_enabled(environ.get('DREAMXBOTZ_IMAGE_FETCH', 'True'), True)  # Fetch posters from TMDB
TMDB_POSTER       = is_enabled(environ.get('TMDB_POSTER', 'True'), True)       # Show TMDB poster in notifications
LANDSCAPE_POSTER  = is_enabled(environ.get('LANDSCAPE_POSTER', 'True'), True)  # Use landscape (wide) poster
IMDB              = is_enabled(environ.get('IMDB', 'True'), False)              # Show IMDB info on search
TMDB_ON_SEARCH    = is_enabled(environ.get('TMDB_ON_SEARCH', 'False'), False)  # Use TMDB poster in search results
LONG_IMDB_DESCRIPTION = is_enabled(environ.get('LONG_IMDB_DESCRIPTION', 'False'), False)  # Full plot or short summary
IMDB_TEMPLATE     = environ.get('IMDB_TEMPLATE', f"{script.IMDB_TEMPLATE_TXT}")


# ═══════════════════════════════════════════════════════════
#  10. MOVIE NOTIFICATIONS
# ═══════════════════════════════════════════════════════════
MOVIE_UPDATE_NOTIFICATION = is_enabled(environ.get('MOVIE_UPDATE_NOTIFICATION', 'False'), False)  # Notify channel when new file is indexed
MOVIE_UPDATE_CHANNEL      = int(environ.get('MOVIE_UPDATE_CHANNEL', '-100'))   # Channel to post notifications
LINK_PREVIEW              = is_enabled(environ.get('LINK_PREVIEW', 'False'), False)   # Show link preview in notification
ABOVE_PREVIEW             = is_enabled(environ.get('ABOVE_PREVIEW', 'True'), True)    # Preview above or below text


# ═══════════════════════════════════════════════════════════
#  11. VERIFICATION (SHORTENER LINKS)
#     Set IS_VERIFY = True to force users to complete a shortener link before getting files.
# ═══════════════════════════════════════════════════════════
IS_VERIFY = is_enabled(environ.get('IS_VERIFY', 'False'), False)   # Enable/disable link verification

LOG_VR_CHANNEL  = int(environ.get('LOG_VR_CHANNEL', '-100'))   # Verification log channel ID
LOG_API_CHANNEL = int(environ.get('LOG_API_CHANNEL', '-100'))  # API usage log channel ID

TUTORIAL   = environ.get('TUTORIAL',   'https://t.me/')  # Tutorial link shown to users
TUTORIAL_2 = environ.get('TUTORIAL_2', 'https://t.me/')
TUTORIAL_3 = environ.get('TUTORIAL_3', 'https://t.me/')

# Shortener 1
SHORTENER_API     = environ.get('SHORTENER_API', '')
SHORTENER_WEBSITE = environ.get('SHORTENER_WEBSITE', 'omegalinks.in')

# Shortener 2
SHORTENER_API2     = environ.get('SHORTENER_API2', '')
SHORTENER_WEBSITE2 = environ.get('SHORTENER_WEBSITE2', 'omegalinks.in')

# Shortener 3
SHORTENER_API3     = environ.get('SHORTENER_API3', '')
SHORTENER_WEBSITE3 = environ.get('SHORTENER_WEBSITE3', 'omegalinks.in')

TWO_VERIFY_GAP   = int(environ.get('TWO_VERIFY_GAP', '1200'))   # Seconds between first and second verification
THREE_VERIFY_GAP = int(environ.get('THREE_VERIFY_GAP', '54000')) # Seconds between second and third verification


# ═══════════════════════════════════════════════════════════
#  12. PAYMENT / PREMIUM
# ═══════════════════════════════════════════════════════════
QR_CODE      = environ.get('QR_CODE', 'https://graph.org/file/e419f801841c2ee3db0fc.jpg')  # UPI QR code image
OWNER_UPI_ID = environ.get('OWNER_UPI_ID', '')  # Your UPI ID for payments

STAR_PREMIUM_PLANS = {
    10: "7day",
    20: "15day",
    40: "1month",
    55: "45day",
    75: "60day",
}  # Telegram Stars → duration mapping


# ═══════════════════════════════════════════════════════════
#  13. BOT BEHAVIOUR & FEATURES
# ═══════════════════════════════════════════════════════════
AUTO_FFILTER    = is_enabled(environ.get('AUTO_FFILTER', 'True'), True)     # Auto-filter files in groups
AUTO_DELETE     = is_enabled(environ.get('AUTO_DELETE', 'True'), True)      # Auto-delete bot messages after timeout
DELETE_TIME     = int(environ.get('DELETE_TIME', '300'))                     # Auto-delete delay in seconds (default: 5 min)

SPELL_CHECK_REPLY = is_enabled(environ.get('SPELL_CHECK_REPLY', 'True'), True)  # Suggest correct spelling if no results
MELCOW_NEW_USERS  = is_enabled(environ.get('MELCOW_NEW_USERS', 'False'), False) # Welcome message for new users
PROTECT_CONTENT   = is_enabled(environ.get('PROTECT_CONTENT', 'False'), False)  # Prevent forwarding of bot messages
PM_SEARCH         = is_enabled(environ.get('PM_SEARCH', 'True'), True)          # Allow search in bot DM
EMOJI_MODE        = is_enabled(environ.get('EMOJI_MODE', 'True'), True)         # React with emoji on /start
MAINTENANCE       = is_enabled(environ.get('MAINTENANCE', 'False'), False)      # Enable maintenance mode (blocks all users)

ULTRA_FAST_MODE = is_enabled(environ.get('ULTRA_FAST_MODE', 'False'), True)  # Faster search (may affect accuracy)
CACHE_TIME      = int(environ.get('CACHE_TIME', 300))                         # Inline query cache time in seconds

USE_CAPTION_FILTER = is_enabled(environ.get('USE_CAPTION_FILTER', 'True'), True)  # Search by file caption too
INDEX_CAPTION      = is_enabled(environ.get('SAVE_CAPTION', 'True'), True)        # Save caption when indexing (disable to save DB space)
COVERX             = is_enabled(environ.get('COVERX', 'True'), True)              # Use file thumbnail/cover art

MAX_B_TN  = environ.get('MAX_B_TN', '5')                                    # Max buttons per row in results
MAX_BTN   = is_enabled(environ.get('MAX_BTN', 'True'), True)                 # Show all result buttons
MAX_LIST_ELM = int(environ.get('MAX_LIST_ELM') or 10) or None                # Max items in dropdown lists (0 = unlimited)

P_TTI_SHOW_OFF  = is_enabled(environ.get('P_TTI_SHOW_OFF', 'False'), False)  # Redirect group users to PM instead of sending file
BUTTON_MODE     = is_enabled(environ.get('BUTTON_MODE', 'False'), False)      # Combine filename + size into one button
NO_RESULTS_MSG  = is_enabled(environ.get('NO_RESULTS_MSG', 'True'), True)    # Log "no results" events to LOG_CHANNEL

MSG_ALRT           = environ.get('MSG_ALRT', '')                              # Small alert text shown below file buttons
CUSTOM_FILE_CAPTION = environ.get('CUSTOM_FILE_CAPTION', f"{script.CAPTION}") # Caption template for sent files
BATCH_FILE_CAPTION  = environ.get('BATCH_FILE_CAPTION', CUSTOM_FILE_CAPTION)  # Caption template for batch files


# ═══════════════════════════════════════════════════════════
#  14. STATIC DATA (no need to change)
# ═══════════════════════════════════════════════════════════
LANGUAGES = {
    "Malayalam": "mal", "Tamil": "tam", "English": "eng",
    "Hindi": "hin",     "Telugu": "tel", "Kannada": "kan",
    "Gujarati": "guj",  "Marathi": "mar", "Punjabi": "pun"
}

QUALITIES    = ["360P", "480P", "720P", "1080P", "1440P", "2160P", "4K"]
SEASON_COUNT = 12
SEASONS      = [f"S{str(i).zfill(2)}" for i in range(1, SEASON_COUNT + 1)]

REACTIONS = [
    "🤝","😇","🤗","😍","👍","🎅","😐","🥰","🤩","😱",
    "🤣","😘","👏","😛","😈","🎉","⚡️","🫡","🤓","😎",
    "🏆","🔥","🤭","🌚","🆒","👻","😁"
]

BAD_WORDS = {
    "PrivateMovieZ","toonworld4all","themoviesboss","1tamilmv",
    "tamilblasters","1tamilblasters","skymovieshd","extraflix",
    "hdm2","moviesmod","hdhub4u","mkvcinemas","primefix",
    "join","www","villa","tg","original"
}  # Watermark/spam words stripped from file names

Bot_cmds = {
    "start":          "Start the bot",
    "stats":          "Bot statistics",
    "alive":          "Check if bot is online",
    "settings":       "Change group settings",
    "id":             "Get Telegram ID",
    "info":           "Get user info",
    "del_msg":        "Remove file from notifications",
    "movie_update":   "Toggle movie notifications",
    "pm_search":      "Toggle PM search",
    "trendlist":      "Top trending searches",
    "broadcast":      "Broadcast to all users (admin)",
    "grp_broadcast":  "Broadcast to all groups (admin)",
    "send":           "Send message to a user (admin)",
    "add_premium":    "Add premium user (admin)",
    "remove_premium": "Remove premium user (admin)",
    "premium_users":  "List premium users (admin)",
    "restart":        "Restart the bot (admin)",
    "group_cmd":      "Group command list",
    "admin_cmd":      "Admin command list",
    "reset_group":    "Reset group to default settings",
    "trial_reset":    "Reset user trial (admin)",
    "remove_fsub":    "Remove force-sub for group (group admin)",
    "maintenance":    "Toggle maintenance mode (admin)",
}


# ═══════════════════════════════════════════════════════════
#  15. STARTUP LOG
# ═══════════════════════════════════════════════════════════
LOG_STR  = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
LOG_STR += " Bot Configuration Summary\n"
LOG_STR += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
LOG_STR += f" IMDB          : {'ON' if IMDB else 'OFF'}\n"
LOG_STR += f" Auto Filter   : {'ON' if AUTO_FFILTER else 'OFF'}\n"
LOG_STR += f" Auto Delete   : {'ON' if AUTO_DELETE else 'OFF'} ({DELETE_TIME}s)\n"
LOG_STR += f" Stream Mode   : {'ON' if STREAM_MODE else 'OFF'}\n"
LOG_STR += f" Spell Check   : {'ON' if SPELL_CHECK_REPLY else 'OFF'}\n"
LOG_STR += f" Verification  : {'ON' if IS_VERIFY else 'OFF'}\n"
LOG_STR += f" Protect Msg   : {'ON' if PROTECT_CONTENT else 'OFF'}\n"
LOG_STR += f" Maintenance   : {'ON' if MAINTENANCE else 'OFF'}\n"
LOG_STR += f" Server URL    : {URL}\n"
LOG_STR += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
