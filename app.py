import streamlit as st
import pandas as pd
import numpy as np

# Set page config
st.set_page_config(
    page_title="Atlanta Braves Draft Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .header-main {
        background: linear-gradient(135deg, #003366 0%, #00A3E0 100%);
        color: white;
        padding: 30px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 20px;
    }
    .header-main h1 {
        font-size: 40px;
        margin-bottom: 10px;
        font-weight: bold;
    }
    .stat-box {
        background: white;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #00A3E0;
        margin: 10px 0;
    }
    .section-title {
        background: #FF5910;
        color: white;
        padding: 12px 15px;
        border-radius: 4px;
        font-weight: bold;
        margin: 20px 0 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-main">
    <h1>🐢 Atlanta Braves 2026 Draft Dashboard</h1>
    <p>Interactive Draft Management Tool</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'picks' not in st.session_state:
    st.session_state.picks = {
        9: {'player': '', 'bonus': 0},
        26: {'player': '', 'bonus': 0},
        48: {'player': '', 'bonus': 0}
    }

if 'wishlists' not in st.session_state:
    st.session_state.wishlists = {
        9: [],
        26: [],
        48: []
    }

if 'player_statuses' not in st.session_state:
    st.session_state.player_statuses = {}

# All players
all_players = [
    'Jackson Flora', 'Justin Lebron', 'Ryder Helfrick', 'Hunter Dietz', 'Tegan Kuhns',
    'Landon Thome', 'Kaden Waechter', 'Jarren Advincula', 'Jacob Lombard', 'Cameron Flukey',
    'Tyler Bell', 'Ligan Schmidt', 'Caden Sorrell', 'Daniel Jackson', 'Logan Hughes',
    'Drew Burress', 'Chris Hacopian', 'Eric Becker', 'Mason Edwards', 'Aiden Ruiz',
    'Blake Bowen', 'Will Brick', 'Wes Mendes', 'Eric Booth Jr', 'Gio Rojas',
    'Brody Bumila', 'Coleman Borthwick', 'Zion Rose', 'Jack Radel', 'Ben Blair'
]

# Slot values
slot_values = {
    9: 6675300,
    26: 3578800,
    48: 2081900
}

total_pool = 15870800

# Sidebar - File upload and settings
st.sidebar.header("📤 Settings")
program_name = st.sidebar.text_input("Program Name", value="Atlanta Braves")

st.sidebar.markdown("---")
st.sidebar.info("""
**How to Use:**
1. Enter player names for each pick
2. Enter signing bonus amounts
3. Track budget allocation
4. Build your wishlist for each pick
""")

# Main layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<div class='section-title'>💰 BUDGET TRACKER</div>", unsafe_allow_html=True)
    
    # Calculate totals
    total_spent = sum([st.session_state.picks[pick]['bonus'] for pick in st.session_state.picks])
    remaining = total_pool - total_spent
    
    # Display stats in columns
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    with stat_col1:
        st.metric("Total Pool", f"${total_pool:,.0f}")
    with stat_col2:
        st.metric("Total Spent", f"${total_spent:,.0f}")
    with stat_col3:
        st.metric("Remaining", f"${remaining:,.0f}")
    with stat_col4:
        st.metric("Picks Left", f"{3 - len([p for p in st.session_state.picks.values() if p['player']])}")

with col2:
    st.markdown("<div class='section-title'>📊 VARIANCE BY PICK</div>", unsafe_allow_html=True)
    
    for pick in [9, 26, 48]:
        bonus = st.session_state.picks[pick]['bonus']
        slot = slot_values[pick]
        variance = bonus - slot
        
        if variance < 0:
            st.success(f"**Pick {pick}:** 💰 ${abs(variance):,.0f} UNDER (saved)")
        elif variance > 0:
            st.warning(f"**Pick {pick}:** ⚠️ ${variance:,.0f} OVER")
        else:
            st.info(f"**Pick {pick}:** ✅ At Slot Value")

# Pick sections
st.markdown("<div class='section-title'>📍 DRAFT PICKS</div>", unsafe_allow_html=True)

for pick in [9, 26, 48]:
    with st.expander(f"**Pick {pick}** - Slot: ${slot_values[pick]:,.0f}", expanded=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            player_name = st.text_input(
                f"Player Name (Pick {pick})",
                value=st.session_state.picks[pick]['player'],
                key=f"player_{pick}"
            )
            st.session_state.picks[pick]['player'] = player_name
        
        with col2:
            bonus = st.number_input(
                f"Signing Bonus (Pick {pick})",
                value=st.session_state.picks[pick]['bonus'],
                step=100000,
                key=f"bonus_{pick}"
            )
            st.session_state.picks[pick]['bonus'] = bonus
        
        if st.button(f"💾 Save Pick {pick}", key=f"save_{pick}"):
            st.success(f"Pick {pick} saved!")
        
        # Variance for this pick
        variance = bonus - slot_values[pick]
        pct = (bonus / slot_values[pick] - 1) * 100
        
        st.metric(
            f"Variance",
            f"${variance:,.0f}",
            f"{pct:+.1f}%"
        )

# Wishlist section
st.markdown("<div class='section-title'>⭐ WISHLIST BY PICK</div>", unsafe_allow_html=True)

for pick in [9, 26, 48]:
    with st.expander(f"**Pick {pick} Wishlist**"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            player_input = st.selectbox(
                f"Add player to Pick {pick} wishlist",
                all_players,
                key=f"wishlist_select_{pick}"
            )
        
        with col2:
            if st.button("➕ Add", key=f"wishlist_add_{pick}"):
                if player_input not in st.session_state.wishlists[pick]:
                    st.session_state.wishlists[pick].append(player_input)
                    st.success(f"{player_input} added!")
        
        if st.session_state.wishlists[pick]:
            st.write("**Your Ranked Wishlist:**")
            for i, player in enumerate(st.session_state.wishlists[pick], 1):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"{i}. **{player}**")
                with col2:
                    if st.button("🗑️", key=f"remove_{pick}_{i}"):
                        st.session_state.wishlists[pick].remove(player)
                        st.rerun()
        else:
            st.info("No players ranked yet")

# Available players section
st.markdown("<div class='section-title'>👥 AVAILABLE PLAYERS</div>", unsafe_allow_html=True)

search_term = st.text_input("🔍 Search players...")

picked_players = [st.session_state.picks[pick]['player'] for pick in st.session_state.picks if st.session_state.picks[pick]['player']]
available = [p for p in all_players if p not in picked_players]

if search_term:
    available = [p for p in available if search_term.lower() in p.lower()]

# Display available players in grid
col_width = 3
cols = st.columns(col_width)

for idx, player in enumerate(available):
    with cols[idx % col_width]:
        st.info(f"**{player}**")

# Draft log
st.markdown("<div class='section-title'>📋 DRAFT LOG</div>", unsafe_allow_html=True)

picks_made = [(pick, st.session_state.picks[pick]) for pick in [9, 26, 48] if st.session_state.picks[pick]['player']]

if picks_made:
    for pick, pick_data in picks_made:
        variance = pick_data['bonus'] - slot_values[pick]
        variance_text = f"(💰 {abs(variance):,.0f} under)" if variance < 0 else f"(⚠️ {variance:,.0f} over)" if variance > 0 else "(at slot)"
        st.write(f"**Pick {pick}:** {pick_data['player']} - ${pick_data['bonus']:,.0f} {variance_text}")
else:
    st.info("No picks recorded yet")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #999; font-size: 12px;'>"
    f"<p>{program_name} | 2026 Draft Management Tool</p>"
    "</div>",
    unsafe_allow_html=True
)
