import streamlit as st
from datetime import datetime

from utils.cricbuzz_api import (
    get_match_commentary,
    get_cricbuzz_matches
)

from utils.db_connection import get_connection


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .sub-title {
        font-size: 18px;
        margin-bottom: 20px;
        opacity: 0.80;
    }

    .title-bar {
        padding: 12px 16px;
        border-radius: 10px;
        font-size: 23px;
        font-weight: 700;
        margin-top: 12px;
        margin-bottom: 18px;
        border: 1px solid rgba(128,128,128,0.25);
    }

    .creator-box {
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid rgba(128,128,128,0.25);
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .small-note {
        font-size: 13px;
        opacity: 0.75;
    }

    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(128,128,128,0.20);
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"] {
        gap: 5px;
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"] label {
        padding: 10px 12px;
        border-radius: 9px;
        cursor: pointer;
        font-size: 15px;
        font-weight: 600;
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"] label:hover {
        background-color: rgba(128,128,128,0.15);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🏏 Cricbuzz LiveStats")
st.sidebar.markdown("---")
st.sidebar.header("📊 Dashboard")

selected_section = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Dashboard Overview",
        "🏏 Live Match Center",
        "📋 Recent Matches",
        "💬 Commentary",
        "📊 Innings Summary",
        "🎯 Bowling",
        "📈 Analytics"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.header("👩‍💻 Created By")
st.sidebar.success("Rajeswari Rachapalli")
st.sidebar.markdown("---")
st.sidebar.caption(
    "Real-Time Cricket Insights & SQL-Based Analytics"
)


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🏏 Cricbuzz LiveStats</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Real-Time Cricket Insights & SQL-Based Analytics'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# DATABASE FUNCTIONS
# ============================================================

def get_counts():

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM matches"
        )
        matches = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM players"
        )
        players = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM teams"
        )
        teams = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM venues"
        )
        venues = cursor.fetchone()[0]

        return {
            "matches": matches,
            "players": players,
            "teams": teams,
            "venues": venues
        }

    except Exception as e:

        st.warning(
            f"Database connection error: {e}"
        )

        return {
            "matches": 0,
            "players": 0,
            "teams": 0,
            "venues": 0
        }

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


def get_recent_matches():

    connection = None
    cursor = None

    try:
        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                m.match_id,
                m.description,
                m.match_date,
                m.status,
                m.api_match_id
            FROM matches m
            ORDER BY m.match_date DESC
            LIMIT 10
            """
        )

        return cursor.fetchall()

    except Exception as e:

        st.warning(
            f"Unable to load recent matches: {e}"
        )

        return []

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# CRICBUZZ - GET MATCH DATA
# ============================================================

def get_match_score(match_id):

    data = get_match_commentary(match_id)

    mini = data.get(
        "miniscore",
        {}
    )

    header = data.get(
        "matchHeader",
        {}
    )

    return data, mini, header


# ============================================================
# TEAM NAME
# ============================================================

def get_team_name(team_data):

    if not team_data:
        return "Unknown"

    return (
        team_data.get("name")
        or team_data.get("shortName")
        or team_data.get("teamName")
        or team_data.get("teamSName")
        or str(team_data.get("id", "Unknown"))
    )


# ============================================================
# CRICBUZZ MATCH SELECTOR
# ============================================================

def get_selected_match():

    try:

        matches = get_cricbuzz_matches()

    except Exception as e:

        st.warning(
            f"Unable to load Cricbuzz matches: {e}"
        )

        return None

    if not matches:

        st.warning(
            "No Cricbuzz matches found."
        )

        return None

    match_options = {}

    for match in matches:

        label = (
            f"{match['title']} "
            f"({match['match_id']})"
        )

        match_options[label] = match["match_id"]

    selected_label = st.selectbox(
        "Choose a match",
        list(match_options.keys())
    )

    return match_options[selected_label]


# ============================================================
# DASHBOARD OVERVIEW
# ============================================================

def show_dashboard():

    st.markdown(
        '<div class="title-bar">'
        '📊 Dashboard Overview'
        '</div>',
        unsafe_allow_html=True
    )

    counts = get_counts()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🏏 Total Matches",
            counts["matches"]
        )

    with col2:

        st.metric(
            "👤 Total Players",
            counts["players"]
        )

    with col3:

        st.metric(
            "🏆 Total Teams",
            counts["teams"]
        )

    with col4:

        st.metric(
            "🏟️ Total Venues",
            counts["venues"]
        )

    st.divider()

    st.subheader(
        "📋 Recent Matches"
    )

    recent_matches = get_recent_matches()

    if recent_matches:

        st.dataframe(
            recent_matches,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No database match data available."
        )


# ============================================================
# RECENT MATCHES
# ============================================================

def show_recent_matches():

    st.markdown(
        '<div class="title-bar">'
        '📋 Recent Matches'
        '</div>',
        unsafe_allow_html=True
    )

    recent_matches = get_recent_matches()

    if recent_matches:

        st.dataframe(
            recent_matches,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No recent match data available."
        )


# ============================================================
# LIVE MATCH CENTER
# ============================================================

def show_live_match():

    st.markdown(
        '<div class="title-bar">'
        '🏏 Live Match Center'
        '</div>',
        unsafe_allow_html=True
    )

    selected_match_id = get_selected_match()

    if not selected_match_id:
        return

    try:

        data, mini, header = get_match_score(
            selected_match_id
        )

        if not mini:

            st.warning(
                "No score data available."
            )

            return

        team1 = header.get(
            "team1",
            {}
        )

        team2 = header.get(
            "team2",
            {}
        )

        team1_name = get_team_name(team1)
        team2_name = get_team_name(team2)

        st.markdown(
            f"### 🏏 {team1_name} vs {team2_name}"
        )

        status = (
            mini.get("status")
            or header.get("status")
            or "Status unavailable"
        )

        match_score_details = mini.get(
            "matchScoreDetails",
            {}
        )

        match_state = str(
            match_score_details.get(
                "state",
                header.get("state", "")
            )
        ).lower()

        if match_state == "complete":

            st.success(
                f"✅ COMPLETED — {status}"
            )

        elif "live" in status.lower():

            st.error("🔴 LIVE")
            st.info(status)

        else:

            st.info(
                f"📢 {status}"
            )

        st.divider()

        # ----------------------------------------------------
        # SCORE
        # ----------------------------------------------------

        bat_team = mini.get(
            "batTeam",
            {}
        )

        score = (
            f"{bat_team.get('teamScore', 0)}"
            f"/"
            f"{bat_team.get('teamWkts', 0)}"
        )

        overs = mini.get(
            "overs",
            0
        )

        run_rate = mini.get(
            "currentRunRate",
            0
        )

        # ----------------------------------------------------
        # BATTING TEAM DETECTION
        # ----------------------------------------------------

        bat_team_score_obj = mini.get(
            "batTeamScoreObj",
            {}
        )

        batting_team = (
            bat_team_score_obj.get("teamName")
            or bat_team_score_obj.get("teamSName")
            or bat_team.get("teamName")
            or bat_team.get("shortName")
            or bat_team.get("teamSName")
            or "Unknown"
        )

        if batting_team == "Unknown":

            bat_team_id = (
                bat_team.get("teamId")
                or bat_team.get("id")
                or bat_team_score_obj.get("teamId")
                or bat_team_score_obj.get("id")
            )

            team1_id = (
                team1.get("id")
                or team1.get("teamId")
            )

            team2_id = (
                team2.get("id")
                or team2.get("teamId")
            )

            if (
                bat_team_id
                and str(bat_team_id) == str(team1_id)
            ):

                batting_team = team1_name

            elif (
                bat_team_id
                and str(bat_team_id) == str(team2_id)
            ):

                batting_team = team2_name

            elif bat_team_id:

                batting_team = f"Team {bat_team_id}"

        # ----------------------------------------------------
        # SCORE CARDS
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Current Score",
                score
            )

        with col2:

            st.metric(
                "Overs",
                overs
            )

        with col3:

            st.metric(
                "Run Rate",
                run_rate
            )

        with col4:

            st.metric(
                "Batting Team",
                batting_team
            )

        st.divider()

        # ----------------------------------------------------
        # BATTING
        # ----------------------------------------------------

        st.subheader(
            "🏏 Batting"
        )

        striker = mini.get(
            "batsmanStriker",
            {}
        )

        non_striker = mini.get(
            "batsmanNonStriker",
            {}
        )

        bat_col1, bat_col2 = st.columns(2)

        with bat_col1:

            st.write(
                f"**⭐ {striker.get('name', 'N/A')}**"
            )

            st.write(
                f"Runs: **{striker.get('runs', 0)}**"
            )

            st.write(
                f"Balls: **{striker.get('balls', 0)}**"
            )

            st.write(
                f"4s: **{striker.get('fours', 0)}** | "
                f"6s: **{striker.get('sixes', 0)}** | "
                f"SR: **{striker.get('strikeRate', '0.00')}**"
            )

        with bat_col2:

            if non_striker.get("name"):

                st.write(
                    f"**{non_striker.get('name')}**"
                )

                st.write(
                    f"Runs: **{non_striker.get('runs', 0)}**"
                )

                st.write(
                    f"Balls: **{non_striker.get('balls', 0)}**"
                )

                st.write(
                    f"4s: **{non_striker.get('fours', 0)}** | "
                    f"6s: **{non_striker.get('sixes', 0)}** | "
                    f"SR: **{non_striker.get('strikeRate', '0.00')}**"
                )

            else:

                st.info(
                    "Non-striker information unavailable."
                )

        st.divider()

        # ----------------------------------------------------
        # BOWLING
        # ----------------------------------------------------

        st.subheader(
            "🎯 Bowling"
        )

        bowler = mini.get(
            "bowlerStriker",
            {}
        )

        bowl_col1, bowl_col2 = st.columns(2)

        with bowl_col1:

            st.write(
                f"**{bowler.get('name', 'N/A')}**"
            )

            st.write(
                f"Overs: **{bowler.get('overs', 0)}**"
            )

            st.write(
                f"Runs: **{bowler.get('runs', 0)}**"
            )

        with bowl_col2:

            st.write(
                f"Wickets: **{bowler.get('wickets', 0)}**"
            )

            st.write(
                f"Maidens: **{bowler.get('maidens', 0)}**"
            )

            st.write(
                f"Economy: **{bowler.get('economy', 0)}**"
            )

        st.divider()

        show_innings_summary(mini)

        st.divider()

        show_analytics(mini)

        st.divider()

        show_commentary(data)

        st.divider()

        # ----------------------------------------------------
        # LAST WICKET
        # ----------------------------------------------------

        last_wicket = mini.get(
            "lastWicket",
            ""
        )

        if last_wicket:

            st.subheader(
                "🔴 Last Wicket"
            )

            st.warning(
                last_wicket
            )

        st.divider()

        # ----------------------------------------------------
        # RECENT OVERS
        # ----------------------------------------------------

        recent_overs = mini.get(
            "recentOvsStats",
            ""
        )

        if recent_overs:

            st.subheader(
                "🏏 Recent Overs"
            )

            st.write(
                recent_overs
            )

        st.divider()

        refresh_time = datetime.now().strftime(
            "%H:%M:%S"
        )

        st.caption(
            "🔄 Refresh manually to get latest data"
            f" | Last refresh: {refresh_time}"
        )

    except Exception as e:

        st.error(
            f"Unable to fetch Cricbuzz score: {e}"
        )


# ============================================================
# INNINGS SUMMARY
# ============================================================

def show_innings_summary(mini):

    st.markdown(
        '<div class="title-bar">'
        '📊 Innings Summary'
        '</div>',
        unsafe_allow_html=True
    )

    match_score_details = mini.get(
        "matchScoreDetails",
        {}
    )

    innings_list = match_score_details.get(
        "inningsScoreList",
        []
    )

    if not innings_list:

        st.info(
            "Innings information unavailable."
        )

        return

    innings_rows = []

    for innings in innings_list:

        innings_rows.append(
            {
                "Innings": innings.get(
                    "inningsId",
                    ""
                ),

                "Team": innings.get(
                    "batTeamName",
                    ""
                ),

                "Score": (
                    f"{innings.get('score', 0)}"
                    f"/"
                    f"{innings.get('wickets', 0)}"
                ),

                "Overs": innings.get(
                    "overs",
                    0
                ),

                "Declared": (
                    "Yes"
                    if innings.get(
                        "isDeclared",
                        False
                    )
                    else "No"
                ),

                "Follow-On": (
                    "Yes"
                    if innings.get(
                        "isFollowOn",
                        False
                    )
                    else "No"
                )
            }
        )

    st.dataframe(
        innings_rows,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# COMMENTARY
# ============================================================

def show_commentary(data):

    st.markdown(
        '<div class="title-bar">'
        '💬 Latest Commentary'
        '</div>',
        unsafe_allow_html=True
    )

    commentary_items = data.get(
        "matchCommentary",
        {}
    )

    commentary_list = []

    if isinstance(commentary_items, dict):

        commentary_values = commentary_items.values()

    elif isinstance(commentary_items, list):

        commentary_values = commentary_items

    else:

        commentary_values = []

    for item in commentary_values:

        if (
            isinstance(item, dict)
            and item.get("commType") == "commentary"
            and item.get("commText")
        ):

            commentary_list.append(item)

    commentary_list.sort(
        key=lambda x: x.get(
            "timestamp",
            0
        ),
        reverse=True
    )

    if not commentary_list:

        st.info(
            "No commentary available."
        )

        return

    for item in commentary_list[:10]:

        team_name = item.get(
            "teamName",
            ""
        )

        innings_id = item.get(
            "inningsId",
            ""
        )

        text = item.get(
            "commText",
            ""
        )

        prefix = ""

        if team_name:

            prefix += f"**{team_name}** "

        if innings_id:

            prefix += f"(Innings {innings_id}) "

        st.write(
            f"• {prefix}{text}"
        )


# ============================================================
# BOWLING PAGE
# ============================================================

def show_bowling_page():

    st.markdown(
        '<div class="title-bar">'
        '🎯 Bowling'
        '</div>',
        unsafe_allow_html=True
    )

    selected_match_id = get_selected_match()

    if not selected_match_id:
        return

    try:

        data, mini, header = get_match_score(
            selected_match_id
        )

        st.subheader(
            "🎯 Current Bowler"
        )

        bowler = mini.get(
            "bowlerStriker",
            {}
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Bowler",
                bowler.get(
                    "name",
                    "N/A"
                )
            )

        with col2:

            st.metric(
                "Overs",
                bowler.get(
                    "overs",
                    0
                )
            )

        with col3:

            st.metric(
                "Runs",
                bowler.get(
                    "runs",
                    0
                )
            )

        with col4:

            st.metric(
                "Wickets",
                bowler.get(
                    "wickets",
                    0
                )
            )

        st.divider()

        st.write(
            f"**Maidens:** "
            f"{bowler.get('maidens', 0)}"
        )

        st.write(
            f"**Economy:** "
            f"{bowler.get('economy', 0)}"
        )

    except Exception as e:

        st.error(
            f"Unable to load bowling data: {e}"
        )


# ============================================================
# COMMENTARY PAGE
# ============================================================

def show_commentary_page():

    st.markdown(
        '<div class="title-bar">'
        '💬 Commentary'
        '</div>',
        unsafe_allow_html=True
    )

    selected_match_id = get_selected_match()

    if not selected_match_id:
        return

    try:

        data, mini, header = get_match_score(
            selected_match_id
        )

        show_commentary(data)

    except Exception as e:

        st.error(
            f"Unable to load commentary: {e}"
        )


# ============================================================
# INNINGS PAGE
# ============================================================

def show_innings_page():

    st.markdown(
        '<div class="title-bar">'
        '📊 Innings Summary'
        '</div>',
        unsafe_allow_html=True
    )

    selected_match_id = get_selected_match()

    if not selected_match_id:
        return

    try:

        data, mini, header = get_match_score(
            selected_match_id
        )

        show_innings_summary(mini)

    except Exception as e:

        st.error(
            f"Unable to load innings data: {e}"
        )


# ============================================================
# ANALYTICS
# ============================================================

def show_analytics(mini):

    st.markdown(
        '<div class="title-bar">'
        '📈 Match Analytics'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Current Run Rate",
            mini.get(
                "currentRunRate",
                0
            )
        )

    with col2:

        partnership = mini.get(
            "partnerShip",
            {}
        )

        st.metric(
            "Partnership Runs",
            partnership.get(
                "runs",
                0
            )
        )

    with col3:

        st.metric(
            "Partnership Balls",
            partnership.get(
                "balls",
                0
            )
        )

    match_score_details = mini.get(
        "matchScoreDetails",
        {}
    )

    innings_list = match_score_details.get(
        "inningsScoreList",
        []
    )

    if innings_list:

        chart_data = {}

        for innings in innings_list:

            team = innings.get(
                "batTeamName",
                "Unknown"
            )

            score = innings.get(
                "score",
                0
            )

            innings_id = innings.get(
                "inningsId",
                ""
            )

            chart_data[
                f"{team} - Innings {innings_id}"
            ] = score

        if chart_data:

            st.subheader(
                "📊 Runs by Innings"
            )

            st.bar_chart(
                chart_data
            )

    st.subheader(
        "🏏 Batsman Comparison"
    )

    striker = mini.get(
        "batsmanStriker",
        {}
    )

    non_striker = mini.get(
        "batsmanNonStriker",
        {}
    )

    batsman_chart = {}

    striker_name = striker.get(
        "name",
        ""
    )

    non_striker_name = non_striker.get(
        "name",
        ""
    )

    if striker_name:

        batsman_chart[striker_name] = striker.get(
            "runs",
            0
        )

    if non_striker_name:

        batsman_chart[non_striker_name] = non_striker.get(
            "runs",
            0
        )

    if batsman_chart:

        st.bar_chart(
            batsman_chart
        )


# ============================================================
# ANALYTICS PAGE
# ============================================================

def show_analytics_page():

    st.markdown(
        '<div class="title-bar">'
        '📈 Analytics'
        '</div>',
        unsafe_allow_html=True
    )

    selected_match_id = get_selected_match()

    if not selected_match_id:
        return

    try:

        data, mini, header = get_match_score(
            selected_match_id
        )

        show_analytics(mini)

    except Exception as e:

        st.error(
            f"Unable to load analytics: {e}"
        )


# ============================================================
# PAGE NAVIGATION
# ============================================================

try:

    if selected_section == "🏠 Dashboard Overview":

        show_dashboard()

    elif selected_section == "🏏 Live Match Center":

        show_live_match()

    elif selected_section == "📋 Recent Matches":

        show_recent_matches()

    elif selected_section == "💬 Commentary":

        show_commentary_page()

    elif selected_section == "📊 Innings Summary":

        show_innings_page()

    elif selected_section == "🎯 Bowling":

        show_bowling_page()

    elif selected_section == "📈 Analytics":

        show_analytics_page()

except Exception as e:

    st.error(
        f"Application error: {e}"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="creator-box">
    🏏 <b>Cricbuzz LiveStats</b><br>
    Real-Time Cricket Insights & SQL-Based Analytics<br><br>
    👩‍💻 Created by <b>Rajeswari Rachapalli</b><br><br>
    <span class="small-note">
    MySQL • Python • Streamlit • Cricbuzz API
    </span>
    </div>
    """,
    unsafe_allow_html=True
)