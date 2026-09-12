import re
from datetime import datetime

import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup

from utils.cricbuzz_api import get_match_commentary, get_cricbuzz_matches
from utils.db_connection import get_connection


st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
    .main-title{
        font-size:42px;
        font-weight:800;
        margin-bottom:5px
    }

    .sub-title{
        font-size:18px;
        margin-bottom:20px;
        opacity:.8
    }

    .title-bar{
        padding:12px 16px;
        border-radius:10px;
        font-size:23px;
        font-weight:700;
        margin:12px 0 18px;
        border:1px solid rgba(128,128,128,.25)
    }

    .creator-box{
        padding:18px;
        border-radius:12px;
        text-align:center;
        border:1px solid rgba(128,128,128,.25);
        margin-top:20px;
        margin-bottom:10px
    }

    .small-note{
        font-size:13px;
        opacity:.75
    }

    section[data-testid="stSidebar"]{
        border-right:1px solid rgba(128,128,128,.20)
    }

    section[data-testid="stSidebar"] div[role="radiogroup"]{
        gap:5px
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label{
        padding:10px 12px;
        border-radius:9px;
        cursor:pointer;
        font-size:15px;
        font-weight:600
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover{
        background-color:rgba(128,128,128,.15)
    }

    .sql-query-number{
        font-size:18px;
        font-weight:700;
        margin-top:10px;
        margin-bottom:8px
    }
    </style>
    """,
    unsafe_allow_html=True,
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
        "📚 SQL Analytics",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.header("👩‍💻 Created By")
st.sidebar.success("Rajeswari Rachapalli")
st.sidebar.markdown("---")
st.sidebar.caption("Real-Time Cricket Insights & SQL-Based Analytics")


st.markdown(
    '<div class="main-title">🏏 Cricbuzz LiveStats</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="sub-title">Real-Time Cricket Insights & SQL-Based Analytics</div>',
    unsafe_allow_html=True,
)


# ============================================================
# DATABASE HELPERS
# ============================================================

def execute_select(query, params=None):
    connection = cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def execute_action(query, params=None):
    connection = cursor = None

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

        return {
            "matches": 0,
            "players": 0,
            "teams": 0,
            "venues": 0,
        }

    except Exception as e:

        st.warning(f"Database connection error: {e}")

        return {
            "matches": 0,
            "players": 0,
            "teams": 0,
            "venues": 0,
        }


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

        st.warning(f"Unable to load recent matches: {e}")

        return []


# ============================================================
# CRICBUZZ HELPERS
# ============================================================

def get_match_score(match_id):

    data = get_match_commentary(match_id)

    return (
        data,
        data.get("miniscore", {}),
        data.get("matchHeader", {}),
    )


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


def get_selected_match():

    try:

        matches = get_cricbuzz_matches()

    except Exception as e:

        st.warning(f"Unable to load Cricbuzz matches: {e}")

        return None

    if not matches:

        st.warning("No Cricbuzz matches found.")

        return None

    options = {
        f"{m['title']} ({m['match_id']})": m["match_id"]
        for m in matches
    }

    label = st.selectbox(
        "Choose a match",
        list(options.keys()),
    )

    return options[label]


# ============================================================
# COMMON UI HELPERS
# ============================================================

def page_title(title):

    st.markdown(
        f'<div class="title-bar">{title}</div>',
        unsafe_allow_html=True,
    )


def clean_commentary(text):

    if not text:
        return ""

    text = BeautifulSoup(
        str(text),
        "html.parser",
    ).get_text(
        " ",
        strip=True,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    ).strip()

    return text


# ============================================================
# DASHBOARD
# ============================================================

def show_dashboard():

    page_title("📊 Dashboard Overview")

    counts = get_counts()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "🏏 Total Matches",
        counts["matches"],
    )

    c2.metric(
        "👤 Total Players",
        counts["players"],
    )

    c3.metric(
        "🏆 Total Teams",
        counts["teams"],
    )

    c4.metric(
        "🏟️ Total Venues",
        counts["venues"],
    )

    st.divider()

    st.subheader("📋 Recent Matches")

    rows = get_recent_matches()

    if rows:

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "⬇️ Download Recent Matches CSV",
            df.to_csv(index=False),
            "recent_matches.csv",
            "text/csv",
        )

    else:

        st.info(
            "No database match data available."
        )


# ============================================================
# RECENT MATCHES
# ============================================================

def show_recent_matches():

    page_title("📋 Recent Matches")

    rows = get_recent_matches()

    if rows:

        df = pd.DataFrame(rows)

        rename_map = {
            "match_id": "Match ID",
            "description": "Match",
            "match_date": "Date",
            "status": "Status",
            "api_match_id": "Cricbuzz ID",
        }

        df = df.rename(
            columns=rename_map
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "⬇️ Download CSV",
            df.to_csv(index=False),
            "recent_matches.csv",
            "text/csv",
        )

    else:

        st.info(
            "No recent match data available."
        )


# ============================================================
# INNINGS SUMMARY
# ============================================================

def show_innings_summary(mini):

    page_title("📊 Innings Summary")

    innings_list = (
        mini
        .get("matchScoreDetails", {})
        .get("inningsScoreList", [])
    )

    if not innings_list:

        st.info(
            "Innings information unavailable."
        )

        return

    rows = []

    for x in innings_list:

        team_name = (
            x.get("batTeamName")
            or x.get("teamName")
            or x.get("batTeamSName")
            or "Unknown"
        )

        rows.append(
            {
                "Innings": x.get(
                    "inningsId",
                    "",
                ),
                "Team": team_name,
                "Score": (
                    f"{x.get('score', 0)}/"
                    f"{x.get('wickets', 0)}"
                ),
                "Overs": x.get(
                    "overs",
                    0,
                ),
                "Declared": (
                    "Yes"
                    if x.get(
                        "isDeclared",
                        False,
                    )
                    else "No"
                ),
                "Follow-On": (
                    "Yes"
                    if x.get(
                        "isFollowOn",
                        False,
                    )
                    else "No"
                ),
            }
        )

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# MATCH ANALYTICS
# ============================================================

def show_analytics(mini):

    page_title("📈 Match Analytics")

    partnership = mini.get(
        "partnerShip",
        {},
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Current Run Rate",
        mini.get(
            "currentRunRate",
            0,
        ),
    )

    c2.metric(
        "Partnership Runs",
        partnership.get(
            "runs",
            0,
        ),
    )

    c3.metric(
        "Partnership Balls",
        partnership.get(
            "balls",
            0,
        ),
    )

    innings_list = (
        mini
        .get("matchScoreDetails", {})
        .get("inningsScoreList", [])
    )

    if innings_list:

        rows = []

        for x in innings_list:

            rows.append(
                {
                    "Team":
                        x.get(
                            "batTeamName",
                            "Unknown",
                        ),
                    "Innings":
                        x.get(
                            "inningsId",
                            "",
                        ),
                    "Runs":
                        x.get(
                            "score",
                            0,
                        ),
                    "Wickets":
                        x.get(
                            "wickets",
                            0,
                        ),
                    "Overs":
                        x.get(
                            "overs",
                            0,
                        ),
                }
            )

        innings_df = pd.DataFrame(rows)

        if not innings_df.empty:

            st.subheader(
                "📊 Runs by Innings"
            )

            st.dataframe(
                innings_df,
                use_container_width=True,
                hide_index=True,
            )

    striker = mini.get(
        "batsmanStriker",
        {},
    )

    non_striker = mini.get(
        "batsmanNonStriker",
        {},
    )

    batsmen = []

    if striker.get("name"):

        batsmen.append(
            {
                "Batsman":
                    striker.get(
                        "name"
                    ),
                "Runs":
                    striker.get(
                        "runs",
                        0,
                    ),
                "Balls":
                    striker.get(
                        "balls",
                        0,
                    ),
                "4s":
                    striker.get(
                        "fours",
                        0,
                    ),
                "6s":
                    striker.get(
                        "sixes",
                        0,
                    ),
            }
        )

    if non_striker.get("name"):

        batsmen.append(
            {
                "Batsman":
                    non_striker.get(
                        "name"
                    ),
                "Runs":
                    non_striker.get(
                        "runs",
                        0,
                    ),
                "Balls":
                    non_striker.get(
                        "balls",
                        0,
                    ),
                "4s":
                    non_striker.get(
                        "fours",
                        0,
                    ),
                "6s":
                    non_striker.get(
                        "sixes",
                        0,
                    ),
            }
        )

    if batsmen:

        st.subheader(
            "🏏 Batsman Comparison"
        )

        st.dataframe(
            pd.DataFrame(batsmen),
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# COMMENTARY
# ============================================================

def show_commentary(data):

    page_title(
        "💬 Latest Commentary"
    )

    items = data.get(
        "matchCommentary",
        {},
    )

    if isinstance(items, dict):

        values = items.values()

    elif isinstance(items, list):

        values = items

    else:

        values = []

    commentary = [
        x
        for x in values
        if (
            isinstance(x, dict)
            and x.get("commType")
            == "commentary"
            and x.get("commText")
        )
    ]

    commentary.sort(
        key=lambda x: x.get(
            "timestamp",
            0,
        ),
        reverse=True,
    )

    if not commentary:

        st.info(
            "No commentary available."
        )

        return

    for item in commentary[:10]:

        team = item.get(
            "teamName",
            "",
        )

        innings = item.get(
            "inningsId",
            "",
        )

        text = clean_commentary(
            item.get(
                "commText",
                "",
            )
        )

        prefix = (
            f"**{team}** "
            if team
            else ""
        )

        if innings:

            prefix += (
                f"(Innings {innings}) "
            )

        st.markdown(
            f"• {prefix}{text}"
        )


# ============================================================
# LIVE MATCH CENTER
# ============================================================

def show_live_match():

    page_title(
        "🏏 Live Match Center"
    )

    match_id = get_selected_match()

    if not match_id:

        return

    try:

        data, mini, header = (
            get_match_score(
                match_id
            )
        )

        if not mini:

            st.warning(
                "No score data available."
            )

            return

        team1 = header.get(
            "team1",
            {},
        )

        team2 = header.get(
            "team2",
            {},
        )

        team1_name = get_team_name(
            team1
        )

        team2_name = get_team_name(
            team2
        )

        st.markdown(
            f"### 🏏 {team1_name} vs {team2_name}"
        )

        status = (
            mini.get("status")
            or header.get("status")
            or "Status unavailable"
        )

        state = str(
            mini
            .get(
                "matchScoreDetails",
                {},
            )
            .get(
                "state",
                header.get(
                    "state",
                    "",
                ),
            )
        ).lower()

        if state == "complete":

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

        bat_team = mini.get(
            "batTeam",
            {},
        )

        score = (
            f"{bat_team.get('teamScore', 0)}/"
            f"{bat_team.get('teamWkts', 0)}"
        )

        bat_obj = mini.get(
            "batTeamScoreObj",
            {},
        )

        batting_team = (
            bat_obj.get(
                "teamName"
            )
            or bat_obj.get(
                "teamSName"
            )
            or bat_team.get(
                "teamName"
            )
            or bat_team.get(
                "shortName"
            )
            or bat_team.get(
                "teamSName"
            )
            or "Unknown"
        )

        if batting_team == "Unknown":

            bat_id = (
                bat_team.get(
                    "teamId"
                )
                or bat_team.get(
                    "id"
                )
                or bat_obj.get(
                    "teamId"
                )
                or bat_obj.get(
                    "id"
                )
            )

            id1 = (
                team1.get("id")
                or team1.get("teamId")
            )

            id2 = (
                team2.get("id")
                or team2.get("teamId")
            )

            if bat_id and str(bat_id) == str(id1):

                batting_team = team1_name

            elif bat_id and str(bat_id) == str(id2):

                batting_team = team2_name

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Current Score",
            score,
        )

        c2.metric(
            "Overs",
            mini.get(
                "overs",
                0,
            ),
        )

        c3.metric(
            "Run Rate",
            mini.get(
                "currentRunRate",
                0,
            ),
        )

        c4.metric(
            "Batting Team",
            batting_team,
        )

        # ----------------------------------------------------
        # BATTING
        # ----------------------------------------------------

        st.subheader("🏏 Batting")

        striker = mini.get(
            "batsmanStriker",
            {},
        )

        non = mini.get(
            "batsmanNonStriker",
            {},
        )

        b1, b2 = st.columns(2)

        with b1:

            st.write(
                f"**⭐ {striker.get('name', 'N/A')}**"
            )

            st.write(
                f"Runs: **{striker.get('runs', 0)}** | "
                f"Balls: **{striker.get('balls', 0)}**"
            )

            st.write(
                f"4s: **{striker.get('fours', 0)}** | "
                f"6s: **{striker.get('sixes', 0)}** | "
                f"SR: **{striker.get('strikeRate', '0.00')}**"
            )

        with b2:

            # Non-striker information is displayed
            # only when Cricbuzz supplies it.
            if non.get("name"):

                st.write(
                    f"**{non['name']}**"
                )

                st.write(
                    f"Runs: **{non.get('runs', 0)}** | "
                    f"Balls: **{non.get('balls', 0)}**"
                )

                st.write(
                    f"4s: **{non.get('fours', 0)}** | "
                    f"6s: **{non.get('sixes', 0)}** | "
                    f"SR: **{non.get('strikeRate', '0.00')}**"
                )

            else:

                # No message is displayed when
                # Cricbuzz does not provide non-striker data.
                pass

        # ----------------------------------------------------
        # BOWLING
        # ----------------------------------------------------

        st.subheader("🎯 Bowling")

        bowler = mini.get(
            "bowlerStriker",
            {},
        )

        q1, q2, q3, q4 = st.columns(4)

        q1.metric(
            "Bowler",
            bowler.get(
                "name",
                "N/A",
            ),
        )

        q2.metric(
            "Overs",
            bowler.get(
                "overs",
                0,
            ),
        )

        q3.metric(
            "Runs",
            bowler.get(
                "runs",
                0,
            ),
        )

        q4.metric(
            "Wickets",
            bowler.get(
                "wickets",
                0,
            ),
        )

        st.write(
            f"**Maidens:** {bowler.get('maidens', 0)}"
            f"   |   "
            f"**Economy:** {bowler.get('economy', 0)}"
        )

        # ----------------------------------------------------
        # OTHER SECTIONS
        # ----------------------------------------------------

        show_innings_summary(
            mini
        )

        show_analytics(
            mini
        )

        show_commentary(
            data
        )

        last_wicket = mini.get(
            "lastWicket",
            "",
        )

        if last_wicket:

            st.subheader(
                "🔴 Last Wicket"
            )

            st.warning(
                clean_commentary(
                    last_wicket
                )
            )

        recent_overs = mini.get(
            "recentOvsStats",
            "",
        )

        if recent_overs:

            st.subheader(
                "🏏 Recent Overs"
            )

            st.write(
                clean_commentary(
                    recent_overs
                )
            )

        st.caption(
            "🔄 Refresh manually to get latest data | "
            f"Last refresh: {datetime.now().strftime('%H:%M:%S')}"
        )

    except Exception as e:

        st.error(
            f"Unable to fetch Cricbuzz score: {e}"
        )


# ============================================================
# COMMENTARY PAGE
# ============================================================

def show_commentary_page():

    page_title("💬 Commentary")

    match_id = get_selected_match()

    if match_id:

        try:

            data, _, _ = get_match_score(
                match_id
            )

            show_commentary(
                data
            )

        except Exception as e:

            st.error(
                f"Unable to load commentary: {e}"
            )


# ============================================================
# INNINGS PAGE
# ============================================================

def show_innings_page():

    page_title(
        "📊 Innings Summary"
    )

    match_id = get_selected_match()

    if match_id:

        try:

            _, mini, _ = get_match_score(
                match_id
            )

            show_innings_summary(
                mini
            )

        except Exception as e:

            st.error(
                f"Unable to load innings data: {e}"
            )


# ============================================================
# BOWLING PAGE
# ============================================================

def show_bowling_page():

    page_title(
        "🎯 Bowling"
    )

    match_id = get_selected_match()

    if not match_id:

        return

    try:

        _, mini, _ = get_match_score(
            match_id
        )

        bowler = mini.get(
            "bowlerStriker",
            {},
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Bowler",
            bowler.get(
                "name",
                "N/A",
            ),
        )

        c2.metric(
            "Overs",
            bowler.get(
                "overs",
                0,
            ),
        )

        c3.metric(
            "Runs",
            bowler.get(
                "runs",
                0,
            ),
        )

        c4.metric(
            "Wickets",
            bowler.get(
                "wickets",
                0,
            ),
        )

        c1, c2 = st.columns(2)

        c1.metric(
            "Maidens",
            bowler.get(
                "maidens",
                0,
            ),
        )

        c2.metric(
            "Economy",
            bowler.get(
                "economy",
                0,
            ),
        )

    except Exception as e:

        st.error(
            f"Unable to load bowling data: {e}"
        )


# ============================================================
# ANALYTICS PAGE
# ============================================================

def show_analytics_page():

    page_title(
        "📈 Analytics"
    )

    match_id = get_selected_match()

    if match_id:

        try:

            _, mini, _ = get_match_score(
                match_id
            )

            show_analytics(
                mini
            )

        except Exception as e:

            st.error(
                f"Unable to load analytics: {e}"
            )


# ============================================================
# CRUD HELPERS
# ============================================================

def get_players():

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


def get_roles():

    return execute_select(
        """
        SELECT
            role_id,
            role_name
        FROM roles
        ORDER BY role_name
        """
    )


def get_teams():

    return execute_select(
        """
        SELECT
            team_id,
            team_name
        FROM teams
        ORDER BY team_name
        """
    )


def create_player(
    full_name,
    role_id,
    team_id,
    batting,
    bowling,
    api_id,
    active,
):

    return execute_action(
        """
        INSERT INTO players(
            full_name,
            role_id,
            national_team_id,
            batting_style,
            bowling_style,
            api_player_id,
            is_active
        )
        VALUES(%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            full_name,
            role_id,
            team_id,
            batting,
            bowling,
            api_id,
            active,
        ),
    )


def update_player(
    player_id,
    full_name,
    role_id,
    team_id,
    batting,
    bowling,
    api_id,
    active,
):

    return execute_action(
        """
        UPDATE players
        SET
            full_name=%s,
            role_id=%s,
            national_team_id=%s,
            batting_style=%s,
            bowling_style=%s,
            api_player_id=%s,
            is_active=%s
        WHERE player_id=%s
        """,
        (
            full_name,
            role_id,
            team_id,
            batting,
            bowling,
            api_id,
            active,
            player_id,
        ),
    )


def delete_player(player_id):

    return execute_action(
        """
        DELETE FROM players
        WHERE player_id=%s
        """,
        (player_id,),
    )


# ============================================================
# CRUD PAGE
# ============================================================

def show_crud_page():

    page_title(
        "🛠️ CRUD Operations"
    )

    st.info(
        "CRUD operations are currently available "
        "for the players table."
    )

    op = st.radio(
        "Choose Operation",
        [
            "➕ Create Player",
            "👀 Read Players",
            "✏️ Update Player",
            "🗑️ Delete Player",
        ],
        horizontal=True,
    )

    try:

        roles = get_roles()
        teams = get_teams()

    except Exception as e:

        st.error(
            f"Unable to load CRUD data: {e}"
        )

        return

    role_map = {
        r["role_name"]: r["role_id"]
        for r in roles
    }

    team_map = {
        t["team_name"]: t["team_id"]
        for t in teams
    }

    # --------------------------------------------------------
    # CREATE
    # --------------------------------------------------------

    if op == "➕ Create Player":

        st.subheader(
            "➕ Add New Player"
        )

        with st.form(
            "create_player_form"
        ):

            name = st.text_input(
                "Full Name"
            )

            role = st.selectbox(
                "Role",
                list(role_map)
                or ["No roles available"],
            )

            team = st.selectbox(
                "National Team",
                ["None"]
                + list(team_map),
            )

            batting = st.text_input(
                "Batting Style"
            )

            bowling = st.text_input(
                "Bowling Style"
            )

            api_id = st.text_input(
                "API Player ID"
            )

            active = st.checkbox(
                "Active Player",
                True,
            )

            submitted = (
                st.form_submit_button(
                    "Create Player"
                )
            )

        if submitted:

            if not name.strip():

                st.error(
                    "Full Name is required."
                )

            else:

                ok, msg = create_player(
                    name.strip(),
                    role_map.get(role),
                    team_map.get(team),
                    batting.strip()
                    or None,
                    bowling.strip()
                    or None,
                    api_id.strip()
                    or None,
                    active,
                )

                if ok:

                    st.success(
                        "✅ Player created successfully."
                    )

                else:

                    st.error(
                        f"Create failed: {msg}"
                    )

    # --------------------------------------------------------
    # READ
    # --------------------------------------------------------

    elif op == "👀 Read Players":

        st.subheader(
            "👀 Players"
        )

        try:

            rows = get_players()

        except Exception as e:

            st.error(
                f"Unable to load players: {e}"
            )

            return

        if rows:

            df = pd.DataFrame(rows)

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
            )

            st.success(
                f"{len(rows)} player records found."
            )

            st.download_button(
                "⬇️ Download Players CSV",
                df.to_csv(index=False),
                "players.csv",
                "text/csv",
            )

        else:

            st.info(
                "No player records found."
            )

    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------

    elif op == "✏️ Update Player":

        st.subheader(
            "✏️ Update Player"
        )

        try:

            players = get_players()

        except Exception as e:

            st.error(
                f"Unable to load players: {e}"
            )

            return

        if not players:

            st.info(
                "No players available for update."
            )

            return

        pmap = {
            f"{p['player_id']} - {p['full_name']}": p
            for p in players
        }

        label = st.selectbox(
            "Select Player",
            list(pmap),
        )

        p = pmap[label]

        role_names = list(role_map)

        if (
            p.get("role_name")
            and p["role_name"]
            not in role_names
        ):

            role_names.insert(
                0,
                p["role_name"],
            )

        team_names = list(team_map)

        if (
            p.get("national_team")
            and p["national_team"]
            not in team_names
        ):

            team_names.insert(
                0,
                p["national_team"],
            )

        with st.form(
            "update_player_form"
        ):

            name = st.text_input(
                "Full Name",
                p.get(
                    "full_name"
                )
                or "",
            )

            role = st.selectbox(
                "Role",
                role_names
                or ["No roles available"],
                index=(
                    role_names.index(
                        p.get("role_name")
                    )
                    if p.get(
                        "role_name"
                    )
                    in role_names
                    else 0
                ),
            )

            opts = [
                "None"
            ] + team_names

            current_team = (
                p.get("national_team")
                if p.get(
                    "national_team"
                )
                in team_names
                else "None"
            )

            team = st.selectbox(
                "National Team",
                opts,
                index=opts.index(
                    current_team
                ),
            )

            batting = st.text_input(
                "Batting Style",
                p.get(
                    "batting_style"
                )
                or "",
            )

            bowling = st.text_input(
                "Bowling Style",
                p.get(
                    "bowling_style"
                )
                or "",
            )

            api_id = st.text_input(
                "API Player ID",
                str(
                    p.get(
                        "api_player_id"
                    )
                    or ""
                ),
            )

            active = st.checkbox(
                "Active Player",
                bool(
                    p.get(
                        "is_active"
                    )
                ),
            )

            submitted = (
                st.form_submit_button(
                    "Update Player"
                )
            )

        if submitted:

            ok, msg = update_player(
                p["player_id"],
                name.strip(),
                role_map.get(role),
                team_map.get(team),
                batting.strip()
                or None,
                bowling.strip()
                or None,
                api_id.strip()
                or None,
                active,
            )

            if ok:

                st.success(
                    "✅ Player updated successfully."
                )

            else:

                st.error(
                    f"Update failed: {msg}"
                )

    # --------------------------------------------------------
    # DELETE
    # --------------------------------------------------------

    else:

        st.subheader(
            "🗑️ Delete Player"
        )

        try:

            players = get_players()

        except Exception as e:

            st.error(
                f"Unable to load players: {e}"
            )

            return

        if not players:

            st.info(
                "No players available for deletion."
            )

            return

        pmap = {
            f"{p['player_id']} - {p['full_name']}":
                p["player_id"]
            for p in players
        }

        label = st.selectbox(
            "Select Player",
            list(pmap),
        )

        confirm = st.checkbox(
            "I understand that this will permanently "
            "delete the player record."
        )

        if st.button(
            "🗑️ Delete Player",
            type="secondary",
        ):

            if not confirm:

                st.warning(
                    "Please confirm deletion first."
                )

            else:

                ok, msg = delete_player(
                    pmap[label]
                )

                if ok:

                    st.success(
                        "✅ Player deleted successfully."
                    )

                else:

                    st.error(
                        f"Delete failed: {msg}"
                    )


# ============================================================
# TOP PLAYER STATS
# ============================================================

def show_top_player_stats():

    page_title(
        "👤 Top Player Stats"
    )

    st.info(
        "Player statistics are calculated "
        "from the MySQL performance tables."
    )

    connection = cursor = None

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

        cursor.execute(
            """
            SELECT
                p.player_id,
                p.full_name,
                COUNT(*) AS innings_played,
                COALESCE(
                    SUM(bp.runs),
                    0
                ) AS total_runs,
                COALESCE(
                    MAX(bp.runs),
                    0
                ) AS highest_score,
                COALESCE(
                    ROUND(
                        AVG(bp.runs),
                        2
                    ),
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

        rows = cursor.fetchall()

        if rows:

            df = pd.DataFrame(rows)

            df = df.rename(
                columns={
                    "player_id": "Player ID",
                    "full_name": "Player",
                    "innings_played": "Innings",
                    "total_runs": "Total Runs",
                    "highest_score": "Highest Score",
                    "average_runs": "Average Runs",
                }
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "No batting performance data available."
            )

        st.divider()

        # ----------------------------------------------------
        # TOP WICKET TAKERS
        # ----------------------------------------------------

        st.subheader(
            "🎯 Top Wicket Takers"
        )

        cursor.execute(
            """
            SELECT
                p.player_id,
                p.full_name,
                COALESCE(
                    SUM(bw.wickets),
                    0
                ) AS total_wickets,
                COALESCE(
                    SUM(bw.runs_conceded),
                    0
                ) AS runs_conceded
            FROM players p
            JOIN bowling_performance bw
                ON p.player_id = bw.player_id
            GROUP BY
                p.player_id,
                p.full_name
            ORDER BY total_wickets DESC
            LIMIT 10
            """
        )

        rows = cursor.fetchall()

        if rows:

            df = pd.DataFrame(rows)

            df = df.rename(
                columns={
                    "player_id": "Player ID",
                    "full_name": "Player",
                    "total_wickets": "Total Wickets",
                    "runs_conceded": "Runs Conceded",
                }
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "No bowling performance data available."
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
            SUM(bw.wickets) AS total_wickets
        FROM players p
        JOIN bowling_performance bw
            ON p.player_id = bw.player_id
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
            SUM(bw.runs_conceded) AS runs_conceded,
            ROUND(
                SUM(bw.balls_bowled) / 6,
                2
            ) AS overs_bowled,
            CASE
                WHEN SUM(bw.balls_bowled) > 0
                THEN ROUND(
                    SUM(bw.runs_conceded) * 6.0
                    / SUM(bw.balls_bowled),
                    2
                )
                ELSE 0
            END AS economy
        FROM players p
        JOIN bowling_performance bw
            ON p.player_id = bw.player_id
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
            COALESCE(
                bat.total_runs,
                0
            ) > 0
            AND COALESCE(
                bowl.total_wickets,
                0
            ) > 0
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
            AND toss_winner_team_id =
                winner_team_id;
        """,

    "21. Close Matches":
        """
        SELECT
            match_id,
            description,
            match_date,
            winner_team_id,
            win_margin_value,
            win_margin_type
        FROM matches
        WHERE
            (
                win_margin_type = 'Runs'
                AND win_margin_value <= 20
            )
            OR
            (
                win_margin_type = 'Wickets'
                AND win_margin_value <= 3
            )
        ORDER BY match_date DESC;
        """,

    "22. Partnerships":
        """
        SELECT
            p.full_name AS player_one,
            p2.full_name AS player_two,
            SUM(
                pa.partnership_runs
            ) AS partnership_runs
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
            t1.team_name AS team_one,
            t2.team_name AS team_two,
            COUNT(*) AS matches_played
        FROM match_teams mt1
        JOIN match_teams mt2
            ON mt1.match_id = mt2.match_id
            AND mt1.team_id < mt2.team_id
        JOIN teams t1
            ON mt1.team_id = t1.team_id
        JOIN teams t2
            ON mt2.team_id = t2.team_id
        GROUP BY
            mt1.team_id,
            mt2.team_id,
            t1.team_name,
            t2.team_name
        ORDER BY matches_played DESC;
        """,

    "24. Player Batting Consistency":
        """
        SELECT
            p.full_name,
            COUNT(*) AS innings,
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
        HAVING COUNT(*) >= 2
        ORDER BY run_stddev ASC;
        """,

    "25. Recent Player Form":
        """
        SELECT
            p.full_name,
            i.match_id,
            bp.runs,
            bp.balls_faced,
            bp.fours,
            bp.sixes
        FROM batting_performance bp
        JOIN players p
            ON bp.player_id = p.player_id
        JOIN innings i
            ON bp.innings_id = i.innings_id
        ORDER BY
            i.match_id DESC,
            p.full_name
        LIMIT 20;
        """,
}


# ============================================================
# SQL ANALYTICS PAGE
# ============================================================

def show_sql_analytics_page():

    page_title(
        "📚 SQL Analytics - 25 Queries"
    )

    st.write(
        "25 SQL queries covering players, teams, "
        "matches, batting, bowling, venues, "
        "partnerships and advanced cricket analytics."
    )

    st.subheader(
        "🔎 Select SQL Query"
    )

    query_names = list(
        SQL_QUERIES.keys()
    )

    # --------------------------------------------------------
    # IMPORTANT:
    # Instead of selectbox, all 25 queries are displayed
    # vertically as a step-by-step numbered list.
    # --------------------------------------------------------

    selected_query = st.radio(
        "Choose one query to execute:",
        query_names,
        index=0,
        label_visibility="visible",
    )

    st.divider()

    query = SQL_QUERIES[
        selected_query
    ]

    st.markdown(
        f"""
        <div class="sql-query-number">
            🔎 {selected_query}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.code(
        query.strip(),
        language="sql",
    )

    st.caption(
        "Review the SQL query above and click "
        "'Run SQL Query' to execute it."
    )

    if st.button(
        "▶️ Run SQL Query",
        type="primary",
        key="run_sql_query_button",
    ):

        try:

            rows = execute_select(
                query
            )

            if rows:

                df = pd.DataFrame(
                    rows
                )

                st.success(
                    "Query executed successfully. "
                    f"{len(df)} row(s) returned."
                )

                st.subheader(
                    "📊 Query Result"
                )

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                )

                st.download_button(
                    "⬇️ Download Query Result CSV",
                    df.to_csv(
                        index=False
                    ),
                    "sql_query_result.csv",
                    "text/csv",
                    key="download_sql_result",
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
    unsafe_allow_html=True,
)