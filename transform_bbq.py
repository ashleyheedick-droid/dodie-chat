#!/usr/bin/env python3
"""Transform Dodie's Cajun Diner into Pit Happens BBQ variant."""
import os, re, shutil

SRC = '/home/user/dodie-chat'
DST = '/home/user/dodie-chat/bbq-variant'

# Files to process: source_name -> dest_name
FILES = {
    'index.html': 'index.html',
    'customer.html': 'customer.html',
    'dodies-ai-chat.html': 'pit-ai-chat.html',
    'waitlist-guest-form.html': 'waitlist-guest-form.html',
    'waitlist-host-view.html': 'waitlist-host-view.html',
    'live-update-inventory.html': 'live-update-inventory.html',
    'daily-specials.html': 'daily-specials.html',
    'manager-dashboard.html': 'manager-dashboard.html',
    'customer-feedback.html': 'customer-feedback.html',
    'staff-shoutout.html': 'staff-shoutout.html',
    'dodies-complete-demo.html': 'pit-control-center.html',
    'test-data.html': 'test-data.html',
    'privacy.html': 'privacy.html',
    'terms.html': 'terms.html',
    'google-apps-script-additions.js': 'google-apps-script-additions.js',
}

def replace_hex_ci(content, old_hex, new_hex):
    """Replace hex color case-insensitively."""
    return re.sub(re.escape(old_hex), new_hex, content, flags=re.IGNORECASE)

def transform(content):
    # =====================================================================
    # STEP 0: Protect external URLs from modification
    # =====================================================================
    content = content.replace('webhook/dodie-chat', '___WEBHOOK_SAFE___')
    content = content.replace('dodie-chat/', '___GHPAGES_SAFE___')
    content = content.replace('dodie-chat', '___GHREPO_SAFE___')

    # =====================================================================
    # STEP 1: Internal file references
    # =====================================================================
    content = content.replace('dodies-ai-chat.html', 'pit-ai-chat.html')
    content = content.replace('dodies-complete-demo.html', 'pit-control-center.html')

    # =====================================================================
    # STEP 2: Hex color replacements
    # BBQ palette: smoky amber, fire orange, deep hickory, warm charcoal
    # =====================================================================
    # Primary brand colors
    content = replace_hex_ci(content, '#8B1A1A', '#8B4513')   # cajun-red -> saddle-brown (smoky wood)
    content = replace_hex_ci(content, '#5A0E0E', '#3E1A00')   # deep-maroon -> deep-hickory
    content = replace_hex_ci(content, '#C41E3A', '#E25822')   # bright-red -> fire-orange
    content = replace_hex_ci(content, '#D4AF37', '#DAA520')   # gold -> goldenrod
    content = replace_hex_ci(content, '#F0D878', '#F0C050')   # gold-light -> warm-honey
    content = replace_hex_ci(content, '#B8860B', '#B8860B')   # gold-dark -> keep (already warm)
    content = replace_hex_ci(content, '#8B0000', '#6B3000')   # dark-red -> deep-ember
    content = replace_hex_ci(content, '#e85d75', '#e8935d')   # pink accent -> warm peach accent

    # Dark background colors (red-tinted -> warm brown-tinted)
    content = replace_hex_ci(content, '#0d0606', '#0d0806')   # dark bg
    content = replace_hex_ci(content, '#1a0e0e', '#1a120e')   # dark card
    content = replace_hex_ci(content, '#0b0505', '#0b0805')   # host view dark
    content = replace_hex_ci(content, '#120808', '#120e08')   # host view card
    content = replace_hex_ci(content, '#1a0a0a', '#1a0e0a')   # control center dark
    content = replace_hex_ci(content, '#2a1515', '#2a1f15')   # control center dark-card
    content = replace_hex_ci(content, '#3a2b12', '#3a2b12')   # host view border (already warm)
    content = replace_hex_ci(content, '#221414', '#221a14')   # hover dark

    # =====================================================================
    # STEP 3: RGBA color replacements
    # =====================================================================
    content = content.replace('139,26,26', '139,69,19')       # cajun-red rgba -> saddle brown
    content = content.replace('90,14,14', '62,26,0')          # deep-maroon rgba -> deep hickory
    content = content.replace('196,30,58', '226,88,34')       # bright-red rgba -> fire orange
    content = content.replace('212,175,55', '218,165,32')     # gold -> goldenrod rgba
    content = content.replace('26,14,14', '26,18,14')         # dark-card rgba
    content = content.replace('26,10,10', '26,14,10')         # control center variant rgba

    # =====================================================================
    # STEP 4: Restaurant name & branding (most specific first)
    # =====================================================================
    # Full formal names
    content = content.replace("Dodie\\'s Cajun Diner", "Pit Happens BBQ")
    content = content.replace("Dodie&#39;s Cajun Diner", "Pit Happens BBQ")
    content = content.replace("Dodie\u2019s Cajun Diner", "Pit Happens BBQ")
    content = content.replace("Dodie's Cajun Diner", "Pit Happens BBQ")

    # Medium-length branded phrases
    content = content.replace("Dodie\u2019s Digital Experience Platform", "Pit Happens Digital Experience Platform")
    content = content.replace("Dodie's Digital Experience Platform", "Pit Happens Digital Experience Platform")
    content = content.replace("Dodie\u2019s Digital Experience", "Pit Happens Digital Experience")
    content = content.replace("Dodie's Digital Experience", "Pit Happens Digital Experience")
    content = content.replace("Dodie\u2019s AI Seafood Concierge", "Pit Happens AI Pitmaster")
    content = content.replace("Dodie's AI Seafood Concierge", "Pit Happens AI Pitmaster")
    content = content.replace("Dodie\u2019s AI Concierge", "Pit Happens AI Pitmaster")
    content = content.replace("Dodie's AI Concierge", "Pit Happens AI Pitmaster")
    content = content.replace("Dodie\u2019s Host View", "Pit Happens Host View")
    content = content.replace("Dodie's Host View", "Pit Happens Host View")
    content = content.replace("Dodie\u2019s Control Center", "Pit Happens Control Center")
    content = content.replace("Dodie's Control Center", "Pit Happens Control Center")

    # Short possessives (catch remaining)
    content = content.replace("Dodie\\'s", "Pit Happens")
    content = content.replace("Dodie&#39;s", "Pit Happens")
    content = content.replace("Dodie\u2019s", "Pit Happens")
    content = content.replace("Dodie's", "Pit Happens")

    # Just "Dodie" alone (without possessive)
    content = content.replace("Dodie ", "Pit Happens ")

    # =====================================================================
    # STEP 5: Taglines and slogans
    # =====================================================================
    content = content.replace("Laissez les bons temps rouler!", "Low & Slow, That's How We Roll")
    content = content.replace("Let the good times roll!", "Smoke 'em if you got 'em!")
    content = content.replace("Technology as Bold as Your Flavors", "Technology as Bold as Your Bark")
    content = content.replace("How Y'all Doin'?", "Welcome to the Pit")
    content = content.replace("How Y&#39;all Doin&#39;?", "Welcome to the Pit")
    content = content.replace("Your Cajun Seafood Concierge", "Your BBQ Pitmaster's Assistant")
    content = content.replace("Your Personal Seafood Expert", "Your Personal BBQ Expert")
    content = content.replace("Good vibes only, cher!", "Where there's smoke, there's flavor!")
    content = content.replace("Welcome, Cher!", "Welcome to the Pit!")
    content = content.replace("The Intel TOAST Can\\'t Give You", "Intelligence, Smoked to Perfection")
    content = content.replace("The Intel TOAST Can't Give You", "Intelligence, Smoked to Perfection")
    content = content.replace("The Intel TOAST Can\u2019t Give You", "Intelligence, Smoked to Perfection")
    content = content.replace("Fresh Deals, Hot Off the Stove", "Fresh Deals, Hot Off the Smoker")
    content = content.replace("We take every word to heart", "Your feedback fuels our fire")
    content = content.replace("Straight from the Gulf to Your Table", "From the Pit to Your Plate")
    content = content.replace("Authentic Louisiana Technology", "Pit-Forged Technology")
    content = content.replace("Fresh Gulf seafood, bold Cajun flavors, and good times. Everything you need is right here.",
                              "Slow-smoked brisket, hand-pulled pork, and legendary burnt ends. Everything you need is right here.")
    content = content.replace("Market-fresh seafood, bayou chowder, and oysters Rockefeller. Everything you need is right here.",
                              "Slow-smoked brisket, hand-pulled pork, and legendary burnt ends. Everything you need is right here.")

    # AI Chat specific
    content = content.replace("I know everything about our fresh seafood, today's prices, wait times, wine pairings, and more. Ask me anything!",
                              "I know everything about what's on the smoker, today's prices, wait times, beer pairings, and more. Ask me anything!")
    content = content.replace("What seafood do you have available right now?",
                              "What meats do you have on the smoker right now?")
    content = content.replace("What's fresh today?", "What's on the smoker?")
    content = content.replace("Live availability &amp; prices", "Live smoker status &amp; prices")
    content = content.replace("Live availability & prices", "Live smoker status & prices")
    content = content.replace("What wine or beer pairs best with your chargrilled oysters?",
                              "What beer pairs best with your brisket?")

    # =====================================================================
    # STEP 6: Cuisine-specific terms
    # =====================================================================
    # Board/feature names
    content = content.replace("Live Seafood Market Board", "Smoker Status Board")
    content = content.replace("Live Seafood Board", "Smoker Status Board")
    content = content.replace("Fresh Seafood Market", "Live Smoker Status")
    content = content.replace("Live Market Prices", "Live Smoker Status")
    content = content.replace("AI Seafood Concierge", "AI Pitmaster")

    # Cajun → BBQ in cuisine context
    content = content.replace("Cajun Boil", "Low & Slow Smoke")
    content = content.replace("Cajun Sampler", "Pitmaster Sampler")
    content = content.replace("Cajun Hurricane cocktail", "Smoky Old Fashioned cocktail")
    content = content.replace("Cajun blackening", "pit smoking")
    content = content.replace("Cajun spice blend", "house dry rub blend")
    content = content.replace("Cajun spice", "dry rub seasoning")
    content = content.replace("Cajun wings", "smoked wings")
    content = content.replace("Cajun country", "BBQ country")
    content = content.replace("Chef's Cajun", "Pitmaster's")
    content = content.replace("house Cajun", "house dry rub")
    content = content.replace("secret Cajun spice", "signature dry rub")
    content = content.replace("Cajun Diner", "BBQ")
    content = content.replace("Cajun cooking", "BBQ smoking")
    content = content.replace("Cajun seasoning", "dry rub seasoning")

    # Menu item transformations (most specific first)
    content = content.replace("Crawfish \u00c9touff\u00e9e", "Beef Brisket")
    content = content.replace("Crawfish Étouffée", "Beef Brisket")
    content = content.replace("Crawfish Etouffee", "Beef Brisket")
    content = content.replace("Crawfish Boil", "Brisket Plate")
    content = content.replace("crawfish boil", "brisket plate")
    content = content.replace("Peel & Eat Shrimp", "Pulled Pork Sandwich")
    content = content.replace("Peel &amp; Eat Shrimp", "Pulled Pork Sandwich")
    content = content.replace("peel and eat shrimp", "pulled pork sandwich")
    content = content.replace("Peel and eat shrimp", "Pulled Pork Sandwich")
    content = content.replace("Snow Crab Legs", "Smoked Turkey Breast")
    content = content.replace("Snow Crab", "Smoked Turkey")
    content = content.replace("snow crab", "smoked turkey")
    content = content.replace("Snow crab", "Smoked turkey")
    content = content.replace("Chargrilled Oysters", "St. Louis Ribs")
    content = content.replace("chargrilled oysters", "smoked ribs")
    content = content.replace("Baked Oysters Rockefeller", "Smoked Baby Back Ribs")
    content = content.replace("baked oysters Rockefeller", "smoked baby back ribs")
    content = content.replace("Oysters Rockefeller", "Smoked Baby Back Ribs")
    content = content.replace("Raw Oysters", "Burnt Ends")
    content = content.replace("raw oysters", "burnt ends")
    content = content.replace("Gulf Oysters on the Half Shell", "House Burnt Ends")
    content = content.replace("gulf oysters", "burnt ends")
    content = content.replace("Crawfish", "Brisket")
    content = content.replace("crawfish", "brisket")

    # Seafood → BBQ general terms
    content = content.replace("Seafood Chowder Bowl", "Loaded Baked Potato")
    content = content.replace("Seafood Chowder", "Loaded Baked Potato")
    content = content.replace("seafood chowder", "loaded baked potato")
    content = content.replace("Market Shrimp Platter", "Pulled Pork Platter")
    content = content.replace("market shrimp platter", "pulled pork platter")
    content = content.replace("Blue Crab Cakes", "Smoked Sausage Links")
    content = content.replace("blue crab", "smoked sausage")
    content = content.replace("Blue crab", "Smoked sausage")
    content = content.replace("See Live Seafood Market", "See Live Smoker Status")

    # General seafood → smoked meats (careful with context)
    content = content.replace("fresh seafood", "smoked meats")
    content = content.replace("Fresh seafood", "Smoked meats")
    content = content.replace("Never Miss Fresh Seafood", "Never Miss Fresh BBQ")
    content = content.replace("Never Miss Fresh Smoked meats", "Never Miss Fresh BBQ")
    content = content.replace("seafood alerts", "BBQ alerts")
    content = content.replace("fresh seafood drops", "fresh BBQ drops")
    content = content.replace("fresh smoked meats drops", "fresh BBQ drops")
    content = content.replace("seafood options", "BBQ options")

    # Sourcing descriptions
    content = content.replace("Louisiana Bayou", "Texas Ranchers")
    content = content.replace("Wild-caught crawfish from the Atchafalaya Basin, the heart of Cajun country",
                              "USDA Prime beef from family ranches across the Texas Hill Country")
    content = content.replace("Wild-caught Louisiana brisket, boiled fresh with our signature dry rub seasoning blend.",
                              "USDA Prime brisket, smoked low and slow for 14 hours with post oak and our signature dry rub.")
    content = content.replace("Gulf Coast Reefs", "Heritage Pork Farms")
    content = content.replace("Premium oysters harvested from pristine Gulf waters off the Louisiana coast",
                              "Heritage breed pork from small farms, hand-pulled and smoked with hickory")
    content = content.replace("Alaska & Pacific", "Local Poultry")
    content = content.replace("Premium smoked turkey sourced from sustainable fisheries in the cold Pacific waters",
                              "Free-range turkey breast, dry-brined and smoked to juicy perfection")
    content = content.replace("Gulf Shrimp Boats", "House-Made Sausage")
    content = content.replace("Wild-caught Gulf shrimp from local fishing families we've partnered with for years",
                              "Handmade sausage links using our family recipe, smoked with pecan wood daily")

    # Preparation styles
    content = content.replace("Classic Louisiana boil with corn, potatoes & our secret spice blend",
                              "14-hour smoke with post oak at 225\u00b0F for the perfect smoke ring")
    content = content.replace("Flame-kissed with garlic butter, parmesan & fresh herbs",
                              "Hot and fast over mesquite for a crispy char and smoky flavor")
    content = content.replace("Fresh shucked on the half shell with mignonette & cocktail sauce",
                              "Hand-chopped and tossed with our signature sauce and pickles")
    content = content.replace("Light cornmeal batter, golden fried to crispy perfection",
                              "Smoked first, then flash-fried for the ultimate crispy bark")
    content = content.replace("Smothered in rich, dark roux with the holy trinity of BBQ smoking",
                              "Thin-sliced against the grain for maximum tenderness and flavor")
    content = content.replace("Cast-iron seared with our house dry rub blackening spice",
                              "Cubed point brisket, re-smoked and glazed with sweet heat sauce")

    # Preparation style names
    content = content.replace("Low & Slow Smoke", "Low & Slow")
    content = content.replace("Chargrilled", "Direct Heat")
    content = content.replace("Raw Bar", "Chopped")
    content = content.replace(">Fried<", ">Smoked & Fried<")
    content = content.replace("\u00c9touff\u00e9e", "Sliced")
    content = content.replace("Étouffée", "Sliced")
    content = content.replace("Blackened", "Burnt Ends")

    # Source badges
    content = content.replace("Wild Caught", "Prime Beef")
    content = content.replace("Reef Harvested", "Heritage Breed")
    content = content.replace(">Sustainable<", ">Free Range<")
    content = content.replace("Local Partners", "House Made")

    # =====================================================================
    # STEP 7: Staff names (Texas BBQ crew)
    # =====================================================================
    content = content.replace('data-staff="Brooke"', 'data-staff="Buck"')
    content = content.replace('>Brooke<', '>Buck<')
    content = content.replace('data-staff="Liv"', 'data-staff="Jolene"')
    content = content.replace('>Liv<', '>Jolene<')
    content = content.replace('data-staff="Ashley"', 'data-staff="Hank"')
    content = content.replace('>Ashley<', '>Hank<')
    content = content.replace('data-staff="Marcus"', 'data-staff="Big Earl"')
    content = content.replace('>Marcus<', '>Big Earl<')
    content = content.replace('data-staff="Tyler"', 'data-staff="Dusty"')
    content = content.replace('>Tyler<', '>Dusty<')
    content = content.replace('data-staff="The Whole Team"', 'data-staff="The Whole Crew"')
    content = content.replace('>Whole Team<', '>Whole Crew<')

    # Staff roles
    content = content.replace('>Chef<', '>Pitmaster<')

    # Staff avatars (BBQ-themed)
    content = content.replace('\U0001f469</div>\n            <div class="staff-name">Buck',
                              '\U0001f920</div>\n            <div class="staff-name">Buck')
    content = content.replace('\U0001f478</div>\n            <div class="staff-name">Jolene',
                              '\U0001f469</div>\n            <div class="staff-name">Jolene')
    content = content.replace('\U0001f481</div>\n            <div class="staff-name">Hank',
                              '\U0001f468</div>\n            <div class="staff-name">Hank')
    content = content.replace('\U0001f468\u200d\U0001f373</div>\n            <div class="staff-name">Big Earl',
                              '\U0001f9d4</div>\n            <div class="staff-name">Big Earl')
    content = content.replace('\U0001f9d1</div>\n            <div class="staff-name">Dusty',
                              '\U0001f468\u200d\U0001f33e</div>\n            <div class="staff-name">Dusty')

    # =====================================================================
    # STEP 8: Waitlist preference items (seafood → meats)
    # =====================================================================
    content = content.replace('data-pref="Crawfish"', 'data-pref="Brisket"')
    content = content.replace('data-pref="Oysters"', 'data-pref="Ribs"')
    content = content.replace('data-pref="Snow Crab"', 'data-pref="Pulled Pork"')
    content = content.replace('data-pref="Shrimp"', 'data-pref="Sausage"')
    content = content.replace('data-pref="Catfish"', 'data-pref="Turkey"')
    content = content.replace('data-pref="Non-Seafood"', 'data-pref="Sides Only"')

    # Preference labels
    content = content.replace('>Crab<', '>Pulled Pork<')
    content = content.replace('>Shrimp<', '>Sausage<')
    content = content.replace('>Catfish<', '>Turkey<')
    content = content.replace('>Not Fish<', '>Sides Only<')
    content = content.replace('>Oysters<', '>Ribs<')

    # Preference section header
    content = content.replace("What Are You Craving?", "What Meat Are You Craving?")

    # =====================================================================
    # STEP 9: PIN and localStorage keys
    # =====================================================================
    content = content.replace("dodie2026", "pitbbq2026")
    content = content.replace("dodie_chat_logs", "pitbbq_chat_logs")
    content = content.replace("dodie_shoutouts", "pitbbq_shoutouts")
    content = content.replace("dodie_feedback", "pitbbq_feedback")
    content = content.replace("dodie_vips", "pitbbq_vips")

    # =====================================================================
    # STEP 10: Emoji swaps
    # =====================================================================
    content = content.replace('\U0001F99E', '\U0001F969')  # 🦞 → 🥩
    content = content.replace('\U0001F336\uFE0F', '\U0001F4A8')  # 🌶️ → 💨 (smoke)
    content = content.replace('\U0001F9AA', '\U0001F356')  # 🦪 → 🍖
    content = content.replace('\U0001F980', '\U0001F357')  # 🦀 → 🍗
    content = content.replace('\U0001F364', '\U0001F33D')  # 🍤 → 🌽
    content = content.replace('\U0001F41F', '\U0001F983')  # 🐟 → 🦃

    # Additional seafood board context emojis
    content = content.replace('See what\'s fresh, what\'s hot, and current market prices',
                              'See what\'s on the smoker, what\'s running low, and current prices')
    content = content.replace("See what&#39;s fresh, what&#39;s hot, and current market prices",
                              "See what&#39;s on the smoker, what&#39;s running low, and current prices")

    # =====================================================================
    # STEP 11: Additional BBQ-specific content
    # =====================================================================
    # Notification text
    content = content.replace("We'll text you when fresh seafood drops",
                              "We'll text you when fresh BBQ is ready")
    content = content.replace("We'll text you when fresh smoked meats drops",
                              "We'll text you when fresh BBQ is ready")
    content = content.replace("Get instant text alerts when your favorite items are back in stock",
                              "Get instant text alerts when your favorite meats are on the smoker")
    content = content.replace("plus exclusive first-catch pricing before it hits the public board",
                              "plus exclusive early-bird pricing before it hits the public board")
    content = content.replace("You're signed up for seafood alerts",
                              "You're signed up for BBQ alerts")
    content = content.replace("You're signed up for smoked meats alerts",
                              "You're signed up for BBQ alerts")

    # Sourcing section
    content = content.replace("Our seafood is delivered fresh daily from Louisiana's finest Gulf Coast waters.",
                              "All our meats are hand-selected and smoked in-house daily with Texas post oak and hickory.")
    content = content.replace("Real-time availability, market pricing, and sourcing transparency.",
                              "Real-time smoker status, market pricing, and sourcing transparency.")
    content = content.replace("Delivered this morning from the Gulf Coast",
                              "Smoked fresh in-house starting at 3am")
    content = content.replace("Today's Fresh Catch", "Fresh Off the Smoker")
    content = content.replace("Freshly Delivered", "Just Off the Smoker")
    content = content.replace("Arrived Today", "Smoking Since 3am")
    content = content.replace("Market Price", "Pit Price")

    # Live board descriptions
    content = content.replace("Where We Source", "Our Smoking Woods")
    content = content.replace("Preparation Styles", "How We Smoke It")

    # Quick action buttons in chat
    content = content.replace("What's fresh", "What's smoking")
    content = content.replace("Pairings", "Beer Pairings")

    # Meta description
    content = content.replace("Real-time fresh seafood availability, market prices, and sourcing info from Pit Happens BBQ. Gulf Coast brisket, smoked ribs, smoked turkey, and pulled pork sandwich updated live.",
                              "Real-time smoker status, market prices, and sourcing info from Pit Happens BBQ. Brisket, ribs, turkey, and pulled pork updated live.")
    content = content.replace("Real-time fresh smoked meats availability",
                              "Real-time smoker status")

    # CSS variable names (visual only, doesn't affect functionality)
    content = content.replace('--cajun-red:', '--smoke-brown:')
    content = content.replace('var(--cajun-red)', 'var(--smoke-brown)')
    content = content.replace('--deep-maroon:', '--deep-hickory:')
    content = content.replace('var(--deep-maroon)', 'var(--deep-hickory)')
    content = content.replace('--bright-red:', '--fire-orange:')
    content = content.replace('var(--bright-red)', 'var(--fire-orange)')

    # Title tags
    content = content.replace('<title>Live Smoked meats Market', '<title>Live Smoker Status')
    content = content.replace('<title>Live Seafood Market', '<title>Live Smoker Status')
    content = content.replace('Pit Happens AI Pitmaster', "Pit Happens AI Pitmaster's Assistant")

    # =====================================================================
    # STEP 12: Restore protected URLs
    # =====================================================================
    content = content.replace('___WEBHOOK_SAFE___', 'webhook/dodie-chat')
    content = content.replace('___GHPAGES_SAFE___', 'dodie-chat/')
    content = content.replace('___GHREPO_SAFE___', 'dodie-chat')

    return content


def main():
    os.makedirs(DST, exist_ok=True)

    for src_name, dst_name in FILES.items():
        src_path = os.path.join(SRC, src_name)
        dst_path = os.path.join(DST, dst_name)

        if not os.path.exists(src_path):
            print(f"SKIP (not found): {src_name}")
            continue

        with open(src_path, 'r', encoding='utf-8') as f:
            content = f.read()

        content = transform(content)

        with open(dst_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"OK: {src_name} -> {dst_name}")

    print(f"\nDone! {len(FILES)} files processed into {DST}")


if __name__ == '__main__':
    main()
