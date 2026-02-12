#!/usr/bin/env python3
"""Transform Dodie's Cajun Diner into Cypress Bayou Kitchen & Market variant."""
import os, re, shutil

SRC = '/home/user/dodie-chat'
DST = '/home/user/dodie-chat/bayou-variant'

# Files to process: source_name -> dest_name
FILES = {
    'index.html': 'index.html',
    'customer.html': 'customer.html',
    'dodies-ai-chat.html': 'bayou-ai-chat.html',
    'waitlist-guest-form.html': 'waitlist-guest-form.html',
    'waitlist-host-view.html': 'waitlist-host-view.html',
    'live-update-inventory.html': 'live-update-inventory.html',
    'daily-specials.html': 'daily-specials.html',
    'manager-dashboard.html': 'manager-dashboard.html',
    'customer-feedback.html': 'customer-feedback.html',
    'staff-shoutout.html': 'staff-shoutout.html',
    'dodies-complete-demo.html': 'bayou-control-center.html',
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
    # Protect the n8n webhook URL
    content = content.replace('webhook/dodie-chat', '___WEBHOOK_SAFE___')
    # Protect the GitHub pages URL
    content = content.replace('dodie-chat/', '___GHPAGES_SAFE___')
    content = content.replace('dodie-chat', '___GHREPO_SAFE___')

    # =====================================================================
    # STEP 1: Internal file references
    # =====================================================================
    content = content.replace('dodies-ai-chat.html', 'bayou-ai-chat.html')
    content = content.replace('dodies-complete-demo.html', 'bayou-control-center.html')

    # =====================================================================
    # STEP 2: Hex color replacements (themed colors)
    # =====================================================================
    # Primary brand colors
    content = replace_hex_ci(content, '#8B1A1A', '#1B5E5E')   # cajun-red -> bayou-teal
    content = replace_hex_ci(content, '#5A0E0E', '#0D3B3B')   # deep-maroon -> deep-cypress
    content = replace_hex_ci(content, '#C41E3A', '#2AA198')   # bright-red -> bright-teal
    content = replace_hex_ci(content, '#D4AF37', '#CD7F32')   # gold -> copper
    content = replace_hex_ci(content, '#F0D878', '#DDA15E')   # gold-light -> copper-light
    content = replace_hex_ci(content, '#B8860B', '#8B6914')   # gold-dark -> copper-dark
    content = replace_hex_ci(content, '#8B0000', '#006B6B')   # dark-red -> dark-teal
    content = replace_hex_ci(content, '#e85d75', '#5de8d9')   # pink accent -> teal accent

    # Dark background colors (red-tinted -> teal-tinted)
    content = replace_hex_ci(content, '#0d0606', '#060D0D')   # dark bg
    content = replace_hex_ci(content, '#1a0e0e', '#0E1A1A')   # dark card
    content = replace_hex_ci(content, '#0b0505', '#050B0B')   # host view dark
    content = replace_hex_ci(content, '#120808', '#081212')   # host view card
    content = replace_hex_ci(content, '#1a0a0a', '#0A1A1A')   # control center dark
    content = replace_hex_ci(content, '#2a1515', '#152A2A')   # control center dark-card
    content = replace_hex_ci(content, '#3a2b12', '#122B3A')   # host view border
    content = replace_hex_ci(content, '#221414', '#142222')   # hover dark

    # =====================================================================
    # STEP 3: RGBA color replacements
    # =====================================================================
    content = content.replace('139,26,26', '27,94,94')     # cajun-red rgba
    content = content.replace('90,14,14', '13,59,59')      # deep-maroon rgba
    content = content.replace('196,30,58', '42,161,152')   # bright-red rgba
    content = content.replace('212,175,55', '205,127,50')  # gold -> copper rgba
    content = content.replace('26,14,14', '14,26,26')      # dark-card rgba
    content = content.replace('26,10,10', '10,26,26')      # control center variant rgba

    # =====================================================================
    # STEP 4: Restaurant name & branding (most specific first)
    # =====================================================================
    # Full formal names
    content = content.replace("Dodie\\'s Cajun Diner", "Cypress Bayou Kitchen")
    content = content.replace("Dodie&#39;s Cajun Diner", "Cypress Bayou Kitchen")
    content = content.replace("Dodie\u2019s Cajun Diner", "Cypress Bayou Kitchen")
    content = content.replace("Dodie's Cajun Diner", "Cypress Bayou Kitchen")

    # Medium-length branded phrases
    content = content.replace("Dodie\u2019s Digital Experience Platform", "Cypress Bayou Digital Experience Platform")
    content = content.replace("Dodie's Digital Experience Platform", "Cypress Bayou Digital Experience Platform")
    content = content.replace("Dodie\u2019s Digital Experience", "Cypress Bayou Digital Experience")
    content = content.replace("Dodie's Digital Experience", "Cypress Bayou Digital Experience")
    content = content.replace("Dodie\u2019s AI Seafood Concierge", "Cypress Bayou AI Concierge")
    content = content.replace("Dodie's AI Seafood Concierge", "Cypress Bayou AI Concierge")
    content = content.replace("Dodie\u2019s AI Concierge", "Cypress Bayou AI Concierge")
    content = content.replace("Dodie's AI Concierge", "Cypress Bayou AI Concierge")
    content = content.replace("Dodie\u2019s Host View", "Cypress Bayou Host View")
    content = content.replace("Dodie's Host View", "Cypress Bayou Host View")
    content = content.replace("Dodie\u2019s Control Center", "Cypress Bayou Control Center")
    content = content.replace("Dodie's Control Center", "Cypress Bayou Control Center")

    # Short possessives (catch remaining)
    content = content.replace("Dodie\\'s", "Cypress Bayou")
    content = content.replace("Dodie&#39;s", "Cypress Bayou")
    content = content.replace("Dodie\u2019s", "Cypress Bayou")
    content = content.replace("Dodie's", "Cypress Bayou")

    # Just "Dodie" alone (without possessive)
    content = content.replace("Dodie ", "Cypress Bayou ")

    # =====================================================================
    # STEP 5: Taglines and slogans
    # =====================================================================
    content = content.replace("Laissez les bons temps rouler!", "Where the Bayou Meets Your Table")
    content = content.replace("Let the good times roll!", "Fresh catch, bold flavors!")
    content = content.replace("Technology as Bold as Your Flavors", "Technology as Fresh as Your Catch")
    content = content.replace("How Y'all Doin'?", "Welcome to the Bayou")
    content = content.replace("How Y&#39;all Doin&#39;?", "Welcome to the Bayou")
    content = content.replace("Your Cajun Seafood Concierge", "Your Bayou Seafood Concierge")
    content = content.replace("Your Personal Seafood Expert", "Your Bayou Seafood Guide")
    content = content.replace("Good vibes only, cher!", "Fresh from the water, made with love")
    content = content.replace("Welcome, Cher!", "Welcome to Cypress Bayou!")
    content = content.replace("The Intel TOAST Can\\'t Give You", "Intelligence, Served Fresh")
    content = content.replace("The Intel TOAST Can't Give You", "Intelligence, Served Fresh")
    content = content.replace("The Intel TOAST Can\u2019t Give You", "Intelligence, Served Fresh")
    content = content.replace("Fresh Deals, Hot Off the Stove", "Fresh Deals, Straight from the Bayou")
    content = content.replace("We take every word to heart", "Your voice shapes our table")
    content = content.replace("Straight from the Gulf to Your Table", "Fresh from the Bayou to Your Plate")
    content = content.replace("Authentic Louisiana Technology", "Bayou-Crafted Technology")
    content = content.replace("Fresh Gulf seafood, bold Cajun flavors, and good times. Everything you need is right here.",
                              "Market-fresh seafood, bayou chowder, and oysters Rockefeller. Everything you need is right here.")

    # =====================================================================
    # STEP 6: Cuisine-specific terms
    # =====================================================================
    # Cajun → Bayou in cuisine context (but not CSS/code identifiers)
    content = content.replace("Cajun Boil", "Bayou Boil")
    content = content.replace("Cajun Sampler", "Bayou Sampler")
    content = content.replace("Cajun Hurricane cocktail", "Bayou Sunset cocktail")
    content = content.replace("Cajun blackening", "bayou blackening")
    content = content.replace("Cajun spice blend", "bayou seasoning blend")
    content = content.replace("Cajun spice", "bayou seasoning")
    content = content.replace("Cajun wings", "bayou wings")
    content = content.replace("Cajun country", "bayou country")
    content = content.replace("Chef's Cajun", "Chef's Bayou")
    content = content.replace("house Cajun", "house bayou")
    content = content.replace("secret Cajun spice", "signature bayou seasoning")
    content = content.replace("Cajun Diner", "Kitchen & Market")

    # Menu item transformations
    content = content.replace("Crawfish \u00c9touff\u00e9e", "Oysters Rockefeller")
    content = content.replace("Crawfish Étouffée", "Oysters Rockefeller")
    content = content.replace("Crawfish Etouffee", "Oysters Rockefeller")
    content = content.replace("Crawfish Boil", "Seafood Chowder Bowl")
    content = content.replace("crawfish boil", "seafood chowder")
    content = content.replace("Peel & Eat Shrimp", "Market Shrimp Platter")
    content = content.replace("Peel &amp; Eat Shrimp", "Market Shrimp Platter")
    content = content.replace("peel and eat shrimp", "market shrimp platter")
    content = content.replace("Peel and eat shrimp", "Market Shrimp Platter")
    content = content.replace("Snow Crab Legs", "Blue Crab Cakes")
    content = content.replace("snow crab", "blue crab")
    content = content.replace("Snow crab", "Blue crab")
    content = content.replace("Chargrilled Oysters", "Baked Oysters Rockefeller")
    content = content.replace("chargrilled oysters", "baked oysters Rockefeller")
    content = content.replace("Raw Oysters", "Gulf Oysters on the Half Shell")
    content = content.replace("raw oysters", "gulf oysters")
    content = content.replace("Crawfish", "Seafood Chowder")
    content = content.replace("crawfish", "chowder")
    content = content.replace("Best chowder in Dallas!", "Best seafood chowder in town!")
    content = content.replace("Best chowder in town!", "Best seafood chowder in town!")
    content = content.replace("etouffee", "chowder")
    content = content.replace("\u00e9touff\u00e9e", "chowder")
    content = content.replace("étouffée", "chowder")

    # =====================================================================
    # STEP 7: PIN and localStorage keys
    # =====================================================================
    content = content.replace("dodie2026", "bayou2026")
    content = content.replace("dodie_chat_logs", "cypress_chat_logs")
    content = content.replace("dodie_shoutouts", "cypress_shoutouts")
    content = content.replace("dodie_feedback", "cypress_feedback")
    content = content.replace("dodie_vips", "cypress_vips")

    # =====================================================================
    # STEP 8: Emoji swaps
    # =====================================================================
    content = content.replace('\U0001F99E', '\U0001F9AA')  # 🦞 → 🦪
    content = content.replace('\U0001F336\uFE0F', '\U0001F33F')  # 🌶️ → 🌿

    # =====================================================================
    # STEP 9: Restore protected URLs
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
