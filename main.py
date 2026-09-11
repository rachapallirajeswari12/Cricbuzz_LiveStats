import streamlit as st
from datetime import datetime
import pandas as pd

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
        "📈 Analytics",
        "👤 Top Player Stats",
        "🛠️ CRUD Operations",
        "📚 SQL Analytics"
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
# DATABASE HELPER
# ============================================================

def execute_select(query, params=None):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        return cursor.fetchall()

    except Exception as e:
        raise e

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def execute_action(query, params=None):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        cursor = connection.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        connection.commit()

        return True, "Operation completed successfully."

    except Exception as e:

        if connection:
            connection.rollback()

        return False, str(e)

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# DATABASE COUNTS
# ============================================================

def get_counts():

    try:

        rows = execute_select(
            """
            SELECT
                (SELECT COUNT(*) FROM matches) AS matches,
                (SELECT COUNT(*) FROM players) AS players,
                (SELECT COUNT(*) FROM teams) AS teams,
                (SELECT COUNT(*) FROM venues) AS venues
            """
        )

        if rows:
            return rows[0]

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


# ============================================================
# RECENT MATCHES
# ============================================================

def get_recent_matches():

    try:

        return execute_select(
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

    except Exception as e:

        st.warning(
            f"Unable to load recent matches: {e}"
        )

        return []


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

    st.subheader("📋 Recent Matches")

    recent_matches = get_recent_matches()

    if recent_matches:

        df = pd.DataFrame(recent_matches)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv_data = df.to_csv(
            index=False
        )

        st.download_button(
            "⬇️ Download Recent Matches CSV",
            csv_data,
            "recent_matches.csv",
            "text/csv"
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

        df = pd.DataFrame(recent_matches)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv_data = df.to_csv(
            index=False
        )

        st.download_button(
            "⬇️ Download CSV",
            csv_data,
            "recent_matches.csv",
            "text/csv"
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

        st.subheader("🏏 Batting")

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

        st.subheader("🎯 Bowling")

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

        last_wicket = mini.get(
            "lastWicket",
            ""
        )

        if last_wicket:

            st.subheader("🔴 Last Wicket")

            st.warning(
                last_wicket
            )

        recent_overs = mini.get(
            "recentOvsStats",
            ""
        )

        if recent_overs:

            st.divider()

            st.subheader("🏏 Recent Overs")

            st.write(
                recent_overs
            )

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
        pd.DataFrame(innings_rows),
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
# CRUD - GET PLAYERS
# ============================================================

def get_players():

    try:

        return execute_select(
            """
            SELECT
                p.player_id,
                p.full_name,
                p.role_id,
                r.role_name,
                p.national_team_id,
                t.team_name AS national_team,
                p.batting_style,
                p.bowling_style,
                p.api_player_id,
                p.is_active
            FROM players p
            LEFT JOIN roles r
                ON p.role_id = r.role_id
            LEFT JOIN teams t
                ON p.national_team_id = t.team_id
            ORDER BY p.player_id
            """
        )

    except Exception as e:

        st.error(
            f"Unable to load players: {e}"
        )

        return []


# ============================================================
# CRUD - GET ROLES
# ============================================================

def get_roles():

    try:

        return execute_select(
            """
            SELECT
                role_id,
                role_name
            FROM roles
            ORDER BY role_name
            """
        )

    except Exception as e:

        st.error(
            f"Unable to load roles: {e}"
        )

        return []


# ============================================================
# CRUD - GET TEAMS
# ============================================================

def get_teams():

    try:

        return execute_select(
            """
            SELECT
                team_id,
                team_name
            FROM teams
            ORDER BY team_name
            """
        )

    except Exception as e:

        st.error(
            f"Unable to load teams: {e}"
        )

        return []


# ============================================================
# CRUD - CREATE PLAYER
# ============================================================

def create_player(
    full_name,
    role_id,
    national_team_id,
    batting_style,
    bowling_style,
    api_player_id,
    is_active
):

    return execute_action(
        """
        INSERT INTO players
        (
            full_name,
            role_id,
            national_team_id,
            batting_style,
            bowling_style,
            api_player_id,
            is_active
        )
        VALUES
        (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            full_name,
            role_id,
            national_team_id,
            batting_style,
            bowling_style,
            api_player_id,
            is_active
        )
    )


# ============================================================
# CRUD - UPDATE PLAYER
# ============================================================

def update_player(
    player_id,
    full_name,
    role_id,
    national_team_id,
    batting_style,
    bowling_style,
    api_player_id,
    is_active
):

    return execute_action(
        """
        UPDATE players
        SET
            full_name = %s,
            role_id = %s,
            national_team_id = %s,
            batting_style = %s,
            bowling_style = %s,
            api_player_id = %s,
            is_active = %s
        WHERE player_id = %s
        """,
        (
            full_name,
            role_id,
            national_team_id,
            batting_style,
            bowling_style,
            api_player_id,
            is_active,
            player_id
        )
    )


# ============================================================
# CRUD - DELETE PLAYER
# ============================================================

def delete_player(player_id):

    return execute_action(
        """
        DELETE FROM players
        WHERE player_id = %s
        """,
        (player_id,)
    )


# ============================================================
# CRUD PAGE
# ============================================================

def show_crud_page():

    st.markdown(
        '<div class="title-bar">'
        '🛠️ CRUD Operations'
        '</div>',
        unsafe_allow_html=True
    )

    st.info(
        "CRUD operations are currently available for the players table."
    )

    crud_operation = st.radio(
        "Choose Operation",
        [
            "➕ Create Player",
            "👀 Read Players",
            "✏️ Update Player",
            "🗑️ Delete Player"
        ],
        horizontal=True
    )

    roles = get_roles()
    teams = get_teams()

    role_map = {
        role["role_name"]: role["role_id"]
        for role in roles
    }

    team_map = {
        team["team_name"]: team["team_id"]
        for team in teams
    }

    # ========================================================
    # CREATE
    # ========================================================

    if crud_operation == "➕ Create Player":

        st.subheader("➕ Add New Player")

        with st.form("create_player_form"):

            full_name = st.text_input(
                "Full Name"
            )

            role_name = st.selectbox(
                "Role",
                list(role_map.keys())
                if role_map
                else ["No roles available"]
            )

            team_name = st.selectbox(
                "National Team",
                ["None"] + list(team_map.keys())
            )

            batting_style = st.text_input(
                "Batting Style"
            )

            bowling_style = st.text_input(
                "Bowling Style"
            )

            api_player_id = st.text_input(
                "API Player ID"
            )

            is_active = st.checkbox(
                "Active Player",
                value=True
            )

            submitted = st.form_submit_button(
                "Create Player"
            )

        if submitted:

            if not full_name.strip():

                st.error(
                    "Full Name is required."
                )

            else:

                selected_role_id = role_map.get(
                    role_name
                )

                selected_team_id = team_map.get(
                    team_name
                )

                success, message = create_player(
                    full_name.strip(),
                    selected_role_id,
                    selected_team_id,
                    batting_style.strip() or None,
                    bowling_style.strip() or None,
                    api_player_id.strip() or None,
                    is_active
                )

                if success:

                    st.success(
                        "✅ Player created successfully."
                    )

                else:

                    st.error(
                        f"Create failed: {message}"
                    )

    # ========================================================
    # READ
    # ========================================================

    elif crud_operation == "👀 Read Players":

        st.subheader("👀 Players")

        players = get_players()

        if players:

            df = pd.DataFrame(players)

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            st.success(
                f"{len(players)} player records found."
            )

            csv_data = df.to_csv(
                index=False
            )

            st.download_button(
                "⬇️ Download Players CSV",
                csv_data,
                "players.csv",
                "text/csv"
            )

        else:

            st.info(
                "No player records found."
            )

    # ========================================================
    # UPDATE
    # ========================================================

    elif crud_operation == "✏️ Update Player":

        st.subheader("✏️ Update Player")

        players = get_players()

        if not players:

            st.info(
                "No players available for update."
            )

        else:

            player_map = {
                f"{p['player_id']} - {p['full_name']}":
                p
                for p in players
            }

            selected_player_label = st.selectbox(
                "Select Player",
                list(player_map.keys())
            )

            selected_player = player_map[
                selected_player_label
            ]

            role_names = list(
                role_map.keys()
            )

            current_role = selected_player.get(
                "role_name"
            )

            if (
                current_role
                and current_role not in role_names
            ):

                role_names.insert(
                    0,
                    current_role
                )

            team_names = list(
                team_map.keys()
            )

            current_team = selected_player.get(
                "national_team"
            )

            if (
                current_team
                and current_team not in team_names
            ):

                team_names.insert(
                    0,
                    current_team
                )

            with st.form("update_player_form"):

                full_name = st.text_input(
                    "Full Name",
                    value=selected_player.get(
                        "full_name"
                    ) or ""
                )

                role_name = st.selectbox(
                    "Role",
                    role_names
                    if role_names
                    else ["No roles available"],
                    index=(
                        role_names.index(
                            current_role
                        )
                        if current_role in role_names
                        else 0
                    )
                )

                team_options = [
                    "None"
                ] + team_names

                current_team_option = (
                    current_team
                    if current_team in team_names
                    else "None"
                )

                team_name = st.selectbox(
                    "National Team",
                    team_options,
                    index=team_options.index(
                        current_team_option
                    )
                )

                batting_style = st.text_input(
                    "Batting Style",
                    value=selected_player.get(
                        "batting_style"
                    ) or ""
                )

                bowling_style = st.text_input(
                    "Bowling Style",
                    value=selected_player.get(
                        "bowling_style"
                    ) or ""
                )

                api_player_id = st.text_input(
                    "API Player ID",
                    value=str(
                        selected_player.get(
                            "api_player_id"
                        ) or ""
                    )
                )

                is_active = st.checkbox(
                    "Active Player",
                    value=bool(
                        selected_player.get(
                            "is_active"
                        )
                    )
                )

                submitted = st.form_submit_button(
                    "Update Player"
                )

            if submitted:

                selected_role_id = role_map.get(
                    role_name
                )

                selected_team_id = team_map.get(
                    team_name
                )

                success, message = update_player(
                    selected_player["player_id"],
                    full_name.strip(),
                    selected_role_id,
                    selected_team_id,
                    batting_style.strip() or None,
                    bowling_style.strip() or None,
                    api_player_id.strip() or None,
                    is_active
                )

                if success:

                    st.success(
                        "✅ Player updated successfully."
                    )

                else:

                    st.error(
                        f"Update failed: {message}"
                    )

    # ========================================================
    # DELETE
    # ========================================================

    elif crud_operation == "🗑️ Delete Player":

        st.subheader("🗑️ Delete Player")

        players = get_players()

        if not players:

            st.info(
                "No players available for deletion."
            )

        else:

            player_map = {
                f"{p['player_id']} - {p['full_name']}":
                p["player_id"]
                for p in players
            }

            selected_label = st.selectbox(
                "Select Player",
                list(player_map.keys())
            )

            selected_player_id = player_map[
                selected_label
            ]

            confirm_delete = st.checkbox(
                "I understand that this will permanently delete the player record."
            )

            if st.button(
                "🗑️ Delete Player",
                type="secondary"
            ):

                if not confirm_delete:

                    st.warning(
                        "Please confirm deletion first."
                    )

                else:

                    success, message = delete_player(
                        selected_player_id
                    )

                    if success:

                        st.success(
                            "✅ Player deleted successfully."
                        )

                    else:

                        st.error(
                            f"Delete failed: {message}"
                        )


# ============================================================
# TOP PLAYER STATS
# ============================================================

def show_top_player_stats():

    st.markdown(
        '<div class="title-bar">'
        '👤 Top Player Stats'
        '</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Player statistics are calculated from the MySQL performance tables."
    )

    connection = None
    cursor = None

    try:

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        # ----------------------------------------------------
        # TOP RUN SCORERS
        # ----------------------------------------------------

        st.subheader(
            "🏏 Top Run Scorers"
        )

        try:

            cursor.execute(
                """
                SELECT
                    p.player_id,
                    p.full_name,
                    COUNT(*) AS innings_played,
                    COALESCE(SUM(bp.runs), 0) AS total_runs,
                    COALESCE(MAX(bp.runs), 0) AS highest_score,
                    COALESCE(
                        ROUND(AVG(bp.runs), 2),
                        0
                    ) AS average_runs
                FROM players p
                JOIN batting_performance bp
                    ON p.player_id = bp.player_id
                GROUP BY
                    p.player_id,
                    p.full_name
                ORDER BY total_runs DESC
                LIMIT 10
                """
            )

            top_batsmen = cursor.fetchall()

            if top_batsmen:

                st.dataframe(
                    pd.DataFrame(top_batsmen),
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info(
                    "No batting performance data available."
                )

        except Exception as e:

            st.warning(
                f"Batting statistics unavailable: {e}"
            )

        st.divider()

        # ----------------------------------------------------
        # TOP WICKET TAKERS
        # ----------------------------------------------------

        st.subheader(
            "🎯 Top Wicket Takers"
        )

        try:

            cursor.execute(
                """
                SELECT
                    p.player_id,
                    p.full_name,
                    COALESCE(
                        SUM(bp.wickets),
                        0
                    ) AS total_wickets,
                    COALESCE(
                        SUM(bp.runs_conceded),
                        0
                    ) AS runs_conceded
                FROM players p
                JOIN bowling_performance bp
                    ON p.player_id = bp.player_id
                GROUP BY
                    p.player_id,
                    p.full_name
                ORDER BY total_wickets DESC
                LIMIT 10
                """
            )

            top_bowlers = cursor.fetchall()

            if top_bowlers:

                st.dataframe(
                    pd.DataFrame(top_bowlers),
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info(
                    "No bowling performance data available."
                )

        except Exception as e:

            st.warning(
                f"Bowling statistics unavailable: {e}"
            )

    except Exception as e:

        st.error(
            f"Unable to connect to database: {e}"
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# 25 SQL ANALYTICS QUERIES
# ============================================================

SQL_QUERIES = {

    "1. All Players":
    """
    SELECT
        player_id,
        full_name,
        batting_style,
        bowling_style,
        is_active
    FROM players
    ORDER BY full_name;
    """,

    "2. Active Players":
    """
    SELECT
        player_id,
        full_name
    FROM players
    WHERE is_active = 1
    ORDER BY full_name;
    """,

    "3. Players by Role":
    """
    SELECT
        r.role_name,
        COUNT(p.player_id) AS player_count
    FROM roles r
    LEFT JOIN players p
        ON r.role_id = p.role_id
    GROUP BY
        r.role_id,
        r.role_name
    ORDER BY player_count DESC;
    """,

    "4. Players by National Team":
    """
    SELECT
        t.team_name,
        COUNT(p.player_id) AS player_count
    FROM teams t
    LEFT JOIN players p
        ON t.team_id = p.national_team_id
    GROUP BY
        t.team_id,
        t.team_name
    ORDER BY player_count DESC;
    """,

    "5. Team List":
    """
    SELECT
        team_id,
        team_name,
        team_type,
        country_id
    FROM teams
    ORDER BY team_name;
    """,

    "6. Venue List":
    """
    SELECT
        venue_id,
        venue_name,
        city,
        capacity
    FROM venues
    ORDER BY venue_name;
    """,

    "7. Match List":
    """
    SELECT
        match_id,
        description,
        match_date,
        status,
        api_match_id
    FROM matches
    ORDER BY match_date DESC;
    """,

    "8. Completed Matches":
    """
    SELECT
        match_id,
        description,
        match_date,
        winner_team_id
    FROM matches
    WHERE status = 'Completed'
    ORDER BY match_date DESC;
    """,

    "9. Live Matches":
    """
    SELECT
        match_id,
        description,
        match_date,
        status
    FROM matches
    WHERE status = 'Live'
    ORDER BY match_date DESC;
    """,

    "10. Matches by Format":
    """
    SELECT
        f.format_name,
        COUNT(m.match_id) AS match_count
    FROM formats f
    LEFT JOIN matches m
        ON f.format_id = m.format_id
    GROUP BY
        f.format_id,
        f.format_name
    ORDER BY match_count DESC;
    """,

    "11. Matches by Venue":
    """
    SELECT
        v.venue_name,
        COUNT(m.match_id) AS match_count
    FROM venues v
    LEFT JOIN matches m
        ON v.venue_id = m.venue_id
    GROUP BY
        v.venue_id,
        v.venue_name
    ORDER BY match_count DESC;
    """,

    "12. Matches by Year":
    """
    SELECT
        YEAR(match_date) AS match_year,
        COUNT(*) AS match_count
    FROM matches
    WHERE match_date IS NOT NULL
    GROUP BY YEAR(match_date)
    ORDER BY match_year;
    """,

    "13. Top Run Scorers":
    """
    SELECT
        p.full_name,
        SUM(bp.runs) AS total_runs
    FROM players p
    JOIN batting_performance bp
        ON p.player_id = bp.player_id
    GROUP BY
        p.player_id,
        p.full_name
    ORDER BY total_runs DESC
    LIMIT 10;
    """,

    "14. Highest Individual Scores":
    """
    SELECT
        p.full_name,
        MAX(bp.runs) AS highest_score
    FROM players p
    JOIN batting_performance bp
        ON p.player_id = bp.player_id
    GROUP BY
        p.player_id,
        p.full_name
    ORDER BY highest_score DESC
    LIMIT 10;
    """,

    "15. Top Wicket Takers":
    """
    SELECT
        p.full_name,
        SUM(bp.wickets) AS total_wickets
    FROM players p
    JOIN bowling_performance bp
        ON p.player_id = bp.player_id
    GROUP BY
        p.player_id,
        p.full_name
    ORDER BY total_wickets DESC
    LIMIT 10;
    """,

    "16. Bowling Economy":
    """
    SELECT
        p.full_name,
        SUM(bp.runs_conceded) AS runs_conceded,
        SUM(bp.overs) AS overs_bowled,
        CASE
            WHEN SUM(bp.overs) > 0
            THEN ROUND(
                SUM(bp.runs_conceded) /
                SUM(bp.overs),
                2
            )
            ELSE 0
        END AS economy
    FROM players p
    JOIN bowling_performance bp
        ON p.player_id = bp.player_id
    GROUP BY
        p.player_id,
        p.full_name
    ORDER BY economy ASC;
    """,

    "17. All-Round Players":
    """
    SELECT
        p.full_name,
        COALESCE(
            bat.total_runs,
            0
        ) AS total_runs,
        COALESCE(
            bowl.total_wickets,
            0
        ) AS total_wickets
    FROM players p
    LEFT JOIN (
        SELECT
            player_id,
            SUM(runs) AS total_runs
        FROM batting_performance
        GROUP BY player_id
    ) bat
        ON p.player_id = bat.player_id
    LEFT JOIN (
        SELECT
            player_id,
            SUM(wickets) AS total_wickets
        FROM bowling_performance
        GROUP BY player_id
    ) bowl
        ON p.player_id = bowl.player_id
    WHERE
        COALESCE(bat.total_runs, 0) > 0
        AND COALESCE(bowl.total_wickets, 0) > 0
    ORDER BY
        total_runs DESC,
        total_wickets DESC;
    """,

    "18. Match Winners":
    """
    SELECT
        m.match_id,
        m.description,
        t.team_name AS winning_team,
        m.match_date
    FROM matches m
    LEFT JOIN teams t
        ON m.winner_team_id = t.team_id
    WHERE m.winner_team_id IS NOT NULL
    ORDER BY m.match_date DESC;
    """,

    "19. Toss Winners":
    """
    SELECT
        m.match_id,
        m.description,
        t.team_name AS toss_winner,
        m.toss_decision,
        m.match_date
    FROM matches m
    LEFT JOIN teams t
        ON m.toss_winner_team_id = t.team_id
    WHERE m.toss_winner_team_id IS NOT NULL
    ORDER BY m.match_date DESC;
    """,

    "20. Toss Winner Also Won Match":
    """
    SELECT
        COUNT(*) AS toss_and_match_wins
    FROM matches
    WHERE
        toss_winner_team_id IS NOT NULL
        AND winner_team_id IS NOT NULL
        AND toss_winner_team_id = winner_team_id;
    """,

    "21. Close Matches":
    """
    SELECT
        match_id,
        description,
        match_date,
        winner_team_id,
        win_margin_runs,
        win_margin_wickets
    FROM matches
    WHERE
        (
            win_margin_runs IS NOT NULL
            AND win_margin_runs <= 20
        )
        OR
        (
            win_margin_wickets IS NOT NULL
            AND win_margin_wickets <= 3
        )
    ORDER BY match_date DESC;
    """,

    "22. Partnerships":
    """
    SELECT
        p.full_name AS player_one,
        p2.full_name AS player_two,
        SUM(pa.runs) AS partnership_runs
    FROM partnerships pa
    JOIN players p
        ON pa.player1_id = p.player_id
    JOIN players p2
        ON pa.player2_id = p2.player_id
    GROUP BY
        pa.player1_id,
        pa.player2_id,
        p.full_name,
        p2.full_name
    ORDER BY partnership_runs DESC
    LIMIT 10;
    """,

    "23. Head to Head Matches":
    """
    SELECT
        mt1.team_id AS team_one_id,
        mt2.team_id AS team_two_id,
        COUNT(*) AS matches_played
    FROM match_teams mt1
    JOIN match_teams mt2
        ON mt1.match_id = mt2.match_id
        AND mt1.team_id < mt2.team_id
    GROUP BY
        mt1.team_id,
        mt2.team_id
    ORDER BY matches_played DESC;
    """,

    "24. Player Batting Consistency":
    """
    SELECT
        p.full_name,
        COUNT(bp.batting_id) AS innings,
        ROUND(
            AVG(bp.runs),
            2
        ) AS average_runs,
        ROUND(
            STDDEV_POP(bp.runs),
            2
        ) AS run_stddev
    FROM players p
    JOIN batting_performance bp
        ON p.player_id = bp.player_id
    GROUP BY
        p.player_id,
        p.full_name
    HAVING COUNT(bp.batting_id) >= 2
    ORDER BY run_stddev ASC;
    """,

    "25. Recent Player Form":
    """
    SELECT
        p.full_name,
        bp.match_id,
        bp.runs,
        bp.balls,
        bp.fours,
        bp.sixes
    FROM batting_performance bp
    JOIN players p
        ON bp.player_id = p.player_id
    ORDER BY bp.match_id DESC
    LIMIT 20;
    """
}


# ============================================================
# SQL ANALYTICS PAGE
# ============================================================

def show_sql_analytics_page():

    st.markdown(
        '<div class="title-bar">'
        '📚 SQL Analytics - 25 Queries'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "25 SQL queries covering players, teams, matches, "
        "batting, bowling, venues, partnerships and "
        "advanced cricket analytics."
    )

    selected_query_name = st.selectbox(
        "Choose SQL Query",
        list(SQL_QUERIES.keys())
    )

    selected_query = SQL_QUERIES[
        selected_query_name
    ]

    st.subheader(
        f"🔎 {selected_query_name}"
    )

    st.code(
        selected_query,
        language="sql"
    )

    if st.button(
        "▶️ Run SQL Query",
        type="primary"
    ):

        connection = None
        cursor = None

        try:

            connection = get_connection()

            cursor = connection.cursor(
                dictionary=True
            )

            cursor.execute(
                selected_query
            )

            rows = cursor.fetchall()

            if rows:

                df = pd.DataFrame(rows)

                st.success(
                    f"Query executed successfully. "
                    f"{len(df)} row(s) returned."
                )

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )

                csv_data = df.to_csv(
                    index=False
                )

                st.download_button(
                    "⬇️ Download Query Result CSV",
                    csv_data,
                    "sql_query_result.csv",
                    "text/csv"
                )

            else:

                st.info(
                    "Query executed successfully, "
                    "but returned no rows."
                )

        except Exception as e:

            st.error(
                f"SQL query failed: {e}"
            )

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()


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

    elif selected_section == "👤 Top Player Stats":

        show_top_player_stats()

    elif selected_section == "🛠️ CRUD Operations":

        show_crud_page()

    elif selected_section == "📚 SQL Analytics":

        show_sql_analytics_page()


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