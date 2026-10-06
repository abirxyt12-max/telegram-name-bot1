import os
import random

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ==============================
# USA STYLE FEMALE FIRST NAMES
# ==============================

FIRST_NAMES = [
    "Madison", "Brianna", "Camila", "Kennedy", "Peyton",
    "Skylar", "Savannah", "Aaliyah", "Allison", "Kayla",
    "Mackenzie", "Kylie", "Aubree", "Sienna", "Luna",
    "Violet", "Hazel", "Aurora", "Willow", "Layla",
    "Chloe", "Riley", "Zoey", "Nora", "Ellie",
    "Addison", "Avery", "Harper", "Aria", "Scarlett",
    "Grace", "Lily", "Evelyn", "Abigail", "Emily",
    "Elizabeth", "Sofia", "Ella", "Mia", "Amelia",
    "Isabella", "Olivia", "Emma", "Sophia", "Charlotte",
    "Victoria", "Natalie", "Hannah", "Brooklyn", "Leah",
    "Paisley", "Emery", "Piper", "Naomi", "Ivy",
    "Delilah", "Serenity", "Claire", "Vivian", "Madeline",
    "Ruby", "Alice", "Autumn", "Sadie", "Quinn",
    "Adeline", "Lydia", "Jade", "Parker", "Athena",
    "Elliana", "Raelynn", "Melanie", "Reagan", "Everly",
    "Cora", "Kaylee", "Maria", "Natalia", "Valentina",
    "Clara", "Eliana", "Elena", "Maya", "Valerie",
    "Isla", "Brielle", "Lyla", "Reese", "Eliza",
    "Molly", "Faith", "Rose", "Ariana", "Jasmine",
    "Katherine", "Alexandra", "Ashley", "Taylor", "Jessica",
    "Jennifer", "Lauren", "Samantha", "Morgan", "Sydney",
    "Hailey", "Bailey", "Kendall", "Jordyn", "Jocelyn",
    "Julianna", "Melody", "Andrea", "Trinity", "Adalyn",
    "Arya", "Vivienne", "Josephine", "Emilia", "Daisy",
    "Margaret", "Iris", "Eleanor", "Londyn", "Blakely",
    "Alaina", "Laila", "Lola", "Alana", "Finley",
    "Aspen", "Cecilia", "Juliette", "June", "Kinsley",
    "Georgia", "Genevieve", "Harmony", "Teagan", "Presley",
    "Rylee", "Lilliana", "Arianna", "Eloise", "Brooke",
    "Arabella", "London", "Hope", "Ayla", "Norah",
    "Lila", "Gracie", "Saylor", "Mila", "Camille",
    "Phoebe", "Makayla", "Veronica", "Isabelle", "Marley",
    "Diana", "Lena", "Melissa", "Gabriella", "Lana",
    "Nicole", "Serena", "Alexis", "Tessa", "Catherine",
    "Caitlyn", "Cameron", "Jenna", "Megan", "Rachel",
    "Brittany", "Danielle", "Destiny", "Kiara", "Erin",
    "Kelsey", "Katie", "Paige", "Shelby", "Stephanie",
    "Vanessa", "Whitney", "Jillian", "Alyssa", "Kaylie",
    "Kaitlyn", "Leilani", "Adriana", "Sage", "Wren",
    "Brynlee", "Dahlia", "Mabel", "Maeve", "Elsie",
    "Freya", "Lennon", "Rosalie", "Amara", "Lennox",
    "Kira", "Alina", "Sabrina", "Nina", "Liana",
    "Lucia", "Miriam", "Annie", "Laura", "Amy",
    "Angela", "Christine", "Demi", "Fiona", "Gabrielle",
    "Giselle", "Heidi", "Jane", "Joanna", "Joy",
    "Julia", "Karen", "Lilly", "Linda", "Lisa",
    "Lucy", "Marissa", "Mary", "Michelle", "Monica",
    "Olive", "Raven", "Regina", "Rosa", "Sasha",
    "Sierra", "Summer", "Talia", "Tamara", "Teresa",
    "Valeria", "Wendy", "Yasmin"
]

# ==============================
# USA STYLE LAST NAMES
# ==============================

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones",
    "Miller", "Davis", "Wilson", "Anderson", "Thomas",
    "Taylor", "Moore", "Jackson", "Martin", "Lee",
    "Thompson", "White", "Harris", "Clark", "Lewis",
    "Robinson", "Walker", "Young", "Allen", "King",
    "Wright", "Scott", "Hill", "Green", "Adams",
    "Nelson", "Baker", "Hall", "Campbell", "Mitchell",
    "Carter", "Roberts", "Phillips", "Evans", "Turner",
    "Parker", "Collins", "Edwards", "Stewart", "Morris",
    "Murphy", "Cook", "Rogers", "Morgan", "Cooper",
    "Peterson", "Bailey", "Reed", "Kelly", "Howard",
    "Cox", "Ward", "Richardson", "Watson", "Brooks",
    "Wood", "James", "Bennett", "Gray", "Hughes",
    "Price", "Myers", "Long", "Ross", "Foster",
    "Powell", "Jenkins", "Perry", "Russell", "Sullivan",
    "Bell", "Coleman", "Butler", "Henderson", "Barnes",
    "Fisher", "Simmons", "Jordan", "Patterson", "Alexander",
    "Hamilton", "Graham", "Reynolds", "Griffin", "Wallace",
    "West", "Cole", "Hayes", "Bryant", "Gibson",
    "Ellis", "Stevens", "Murray", "Ford", "Marshall",
    "Owens", "Harrison", "Woods", "Kennedy", "Wells",
    "Henry", "Freeman", "Webb", "Tucker", "Burns",
    "Crawford", "Olson", "Simpson", "Porter", "Hunter",
    "Gordon", "Shaw", "Snyder", "Mason", "Dixon",
    "Hunt", "Hicks", "Holmes", "Palmer", "Wagner",
    "Black", "Robertson", "Boyd", "Stone", "Fox",
    "Warren", "Mills", "Meyer", "Rice", "Daniels",
    "Ferguson", "Nichols", "Stephens", "Weaver", "Ryan",
    "Gardner", "Payne", "Grant", "Dunn", "Spencer",
    "Hawkins", "Arnold", "Pierce", "Hansen", "Peters",
    "Hart", "Bradley", "Knight", "Elliott", "Cunningham",
    "Duncan", "Lane", "Carroll", "Lynch", "Bishop",
    "Hoffman", "Fleming", "Harper", "Fowler", "Watkins",
    "Briggs", "Bates", "Doyle", "Keller", "Casey",
    "Bowers", "Massey", "Rowe", "McKenzie", "Brennan",
    "Vance", "Conley", "Kane", "Nash", "Sherman",
    "Holloway", "Duffy", "Frost", "Larsen", "Morrison",
    "McKay", "McLean", "Farley", "Herman"
]

# Each user's used names
used_names = {}


def generate_name(user_id):
    if user_id not in used_names:
        used_names[user_id] = set()

    for _ in range(500):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        name = f"{first} {last}"

        if name not in used_names[user_id]:
            used_names[user_id].add(name)
            return name

    return "No more unique names available."


def buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "➡️ Next Name",
                callback_data="next"
            )
        ],
        [
            InlineKeyboardButton(
                "📋 Copy Name",
                callback_data="copy"
            )
        ]
    ])


def message_text(name):
    return (
        "🇺🇸 <b>USA Girl Name Generator</b>\n\n"
        f"👤 <code>{name}</code>\n\n"
        "Choose an option below:"
    )


# ==============================
# /START
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    name = generate_name(user_id)

    await update.message.reply_text(
        message_text(name),
        parse_mode="HTML",
        reply_markup=buttons()
    )


# ==============================
# BUTTONS
# ==============================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # NEXT
    if query.data == "next":

        name = generate_name(user_id)

        await query.edit_message_text(
            message_text(name),
            parse_mode="HTML",
            reply_markup=buttons()
        )

    # COPY
    elif query.data == "copy":

        text = query.message.text

        # Get the name from the message
        name = text.split("👤 ")[1].split("\n")[0]

        await query.message.reply_text(
            f"📋 Copy this name:\n\n<code>{name}</code>",
            parse_mode="HTML"
        )


# ==============================
# MAIN
# ==============================

def main():

    token = os.getenv("BOT_TOKEN")

    if not token:
        print("ERROR: BOT_TOKEN is not set!")
        return

    app = Application.builder().token(token).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
