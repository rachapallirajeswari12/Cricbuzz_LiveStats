import streamlit as st
from datetime import datetime

from utils.db_connection import get_connection
from utils.cricbuzz_api import (
    get_match_commentary,
    get_cricbuzz_matches
)


# ============================================================
# PAGE CONFIGURATION
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
        }

        .title-bar {
            padding: 10px 14px;
            border-radius: 10px;
            font-size: 23px;
            font-weight: 700;
            margin-top: 12px;
            margin-bottom: 15px;
            border: 1px solid rgba(128, 128, 128, 0.25);
        }

        .creator-box {
            padding: 18px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid rgba(128, 128, 128, 0.25);
            margin-top: 20px;
            margin-bottom: 10px;
        }

        .small-note {
            font-size: 13px;
            opacity: 0.75;
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
st.sidebar.markdown("🏏 **Live Match Center**")
st.sidebar.markdown("📋 **Recent Matches**")
st.sidebar.markdown("💬 **Commentary**")
st.sidebar.markdown("📊 **Innings Summary**")
st.sidebar.markdown("🎯 **Bowling**")
st.sidebar.markdown("📈 **Analytics**")

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
# MYSQL - GET DASHBOARD COUNTS
# ============================================================

def get_counts():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    queries = {
        "matches": "SELECT COUNT(*) AS total FROM matches",
        "players": "SELECT COUNT(*) AS total FROM players",
        "teams": "SELECT COUNT(*) AS total FROM teams",
        "venues": "SELECT COUNT(*) AS total FROM venues"
    }

    results = {}

    try:
        for key, query in queries.items():
            cursor.execute(query)
            row = cursor.fetchone()
            results[key] = row["total"] if row else 0

    finally:
        cursor.close()
        conn.close()

    return results


# ============================================================
# MYSQL - GET RECENT MATCHES
# ============================================================

def get_recent_matches():
    conn = get_connection()

    query = """
        SELECT
            m.match_id,
            m.description,
            m.match_date,
            m.status,
            w.team_name AS winner
        FROM matches m
        LEFT JOIN teams w
            ON m.winner_team_id = w.team_id
        ORDER BY m.match_date DESC
    """

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query)
        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


# ============================================================
# CRICBUZZ - GET SELECTED MATCH DATA
# ============================================================

def get_match_score(api_match_id):
    data = get_match_commentary(api_match_id)

    mini = data.get("miniscore", {})
    header = data.get("matchHeader", {})

    return data, mini, header


# ============================================================
# TEAM NAME HELPER
# ============================================================

def get_team_name(team_data):

    if not team_data:
        return "Unknown"

    return (
        team_data.get("name")
        or team_data.get("shortName")
        or team_data.get("teamName")
        or str(team_data.get("id", "Unknown"))
    )


# ============================================================
# MAIN DASHBOARD
# ============================================================

try:

    # ========================================================
    # DASHBOARD OVERVIEW
    # ========================================================

    st.markdown(
        '<div class="title-bar">📊 Dashboard Overview</div>',
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


    # ========================================================
    # RECENT MATCHES
    # ========================================================

    st.markdown(
        '<div class="title-bar">📋 Recent Matches</div>',
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
        st.info("No match data available.")


    st.divider()


    # ========================================================
    # CRICBUZZ MATCH CENTER
    # ========================================================

    st.markdown(
        '<div class="title-bar">🌐 Cricbuzz Match Center</div>',
        unsafe_allow_html=True
    )

    try:
        cricbuzz_matches = get_cricbuzz_matches()

    except Exception as e:
        cricbuzz_matches = []
        st.warning(
            f"Unable to load Cricbuzz matches: {e}"
        )


    if not cricbuzz_matches:

        st.warning("No Cricbuzz matches found.")

    else:

        match_options = {}

        for match in cricbuzz_matches:

            label = (
                f"{match['title']} "
                f"({match['match_id']})"
            )

            match_options[label] = match["match_id"]


        selected_label = st.selectbox(
            "Choose a match",
            list(match_options.keys())
        )

        selected_match_id = match_options[
            selected_label
        ]


        st.divider()


        # ====================================================
        # AUTO REFRESH MATCH SECTION
        # ====================================================

        @st.fragment(run_every="10s")
        def show_live_match():

            st.markdown(
                '<div class="title-bar">'
                '🏏 Selected Match Score'
                '</div>',
                unsafe_allow_html=True
            )

            try:

                data, mini, header = get_match_score(
                    selected_match_id
                )

                if not mini:
                    st.warning(
                        "No score data available for this match."
                    )
                    return


                # =================================================
                # TEAM INFORMATION
                # =================================================

                team1 = header.get(
                    "team1",
                    {}
                )

                team2 = header.get(
                    "team2",
                    {}
                )

                team1_name = get_team_name(
                    team1
                )

                team2_name = get_team_name(
                    team2
                )


                # =================================================
                # MATCH TITLE
                # =================================================

                st.markdown(
                    f"### 🏏 {team1_name} vs {team2_name}"
                )


                # =================================================
                # MATCH STATUS
                # =================================================

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


                # =================================================
                # CURRENT SCORE
                # =================================================

                bat_team = mini.get(
                    "batTeam",
                    {}
                )

                current_score = (
                    f"{bat_team.get('teamScore', 0)}"
                    f"/"
                    f"{bat_team.get('teamWkts', 0)}"
                )

                current_overs = mini.get(
                    "overs",
                    0
                )

                current_run_rate = mini.get(
                    "currentRunRate",
                    0
                )


                # =================================================
                # BATTING TEAM NAME
                # =================================================

                batting_team_name = (
                    bat_team.get("teamName")
                    or bat_team.get("shortName")
                )


                if not batting_team_name:

                    bat_team_id = bat_team.get(
                        "teamId",
                        ""
                    )

                    if str(bat_team_id) == str(
                        team1.get("id", "")
                    ):

                        batting_team_name = team1_name

                    elif str(bat_team_id) == str(
                        team2.get("id", "")
                    ):

                        batting_team_name = team2_name

                    else:

                        batting_team_name = (
                            f"Team {bat_team_id}"
                        )


                # =================================================
                # SCORE CARDS
                # =================================================

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Current Score",
                        current_score
                    )

                with col2:
                    st.metric(
                        "Overs",
                        current_overs
                    )

                with col3:
                    st.metric(
                        "Run Rate",
                        current_run_rate
                    )

                with col4:
                    st.metric(
                        "Batting Team",
                        batting_team_name
                    )


                st.divider()


                # =================================================
                # BATTING
                # =================================================

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

                        st.caption(
                            "Non-striker information unavailable."
                        )


                st.divider()


                # =================================================
                # BOWLING
                # =================================================

                st.subheader("🎯 Bowling")

                bowler = mini.get(
                    "bowlerStriker",
                    {}
                )

                bowler_col1, bowler_col2 = st.columns(2)

                with bowler_col1:

                    st.write(
                        f"**{bowler.get('name', 'N/A')}**"
                    )

                    st.write(
                        f"Overs: **{bowler.get('overs', 0)}**"
                    )

                    st.write(
                        f"Runs: **{bowler.get('runs', 0)}**"
                    )


                with bowler_col2:

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


                # =================================================
                # INNINGS SUMMARY
                # =================================================

                st.subheader("📊 Innings Summary")

                innings_list = match_score_details.get(
                    "inningsScoreList",
                    []
                )


                if innings_list:

                    innings_rows = []

                    for innings in innings_list:

                        innings_rows.append(
                            {
                                "Innings":
                                    innings.get(
                                        "inningsId",
                                        ""
                                    ),

                                "Team":
                                    innings.get(
                                        "batTeamName",
                                        ""
                                    ),

                                "Score":
                                    (
                                        f"{innings.get('score', 0)}"
                                        f"/"
                                        f"{innings.get('wickets', 0)}"
                                    ),

                                "Overs":
                                    innings.get(
                                        "overs",
                                        0
                                    ),

                                "Declared":
                                    (
                                        "Yes"
                                        if innings.get(
                                            "isDeclared",
                                            False
                                        )
                                        else "No"
                                    ),

                                "Follow-On":
                                    (
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

                else:

                    st.info(
                        "Innings information unavailable."
                    )


                st.divider()
                # =================================================
                # ANALYTICS
                # =================================================

                st.divider()

                st.markdown(
                    '<div class="title-bar">'
                    '📈 Match Analytics'
                    '</div>',
                    unsafe_allow_html=True
                )

                # ---------------------------------------------
                # Basic match analytics
                # ---------------------------------------------

                analytics_col1, analytics_col2, analytics_col3 = st.columns(3)

                with analytics_col1:
                    st.metric(
                        "Current Run Rate",
                        mini.get("currentRunRate", 0)
                    )

                with analytics_col2:
                    st.metric(
                        "Partnership Runs",
                        mini.get("partnerShip", {}).get("runs", 0)
                    )

                with analytics_col3:
                    st.metric(
                        "Partnership Balls",
                        mini.get("partnerShip", {}).get("balls", 0)
                    )


                # ---------------------------------------------
                # INNINGS SCORE CHART
                # ---------------------------------------------

                if innings_list:

                    chart_data = {}

                    for innings in innings_list:

                        team = innings.get(
                            "batTeamName",
                            f"Innings {innings.get('inningsId', '')}"
                        )

                        score = innings.get(
                            "score",
                            0
                        )

                        chart_data[
                            f"{team} - Innings {innings.get('inningsId', '')}"
                        ] = score


                    if chart_data:

                        st.subheader(
                            "📊 Runs by Innings"
                        )

                        st.bar_chart(
                            chart_data
                        )


                # ---------------------------------------------
                # BATSMAN COMPARISON
                # ---------------------------------------------

                st.subheader(
                    "🏏 Batsman Comparison"
                )

                striker_runs = striker.get(
                    "runs",
                    0
                )

                non_striker_runs = non_striker.get(
                    "runs",
                    0
                )

                batsman_chart = {
                    striker.get(
                        "name",
                        "Striker"
                    ): striker_runs,

                    non_striker.get(
                        "name",
                        "Non-Striker"
                    ): non_striker_runs
                }

                # Remove blank player names
                batsman_chart = {
                    name: runs
                    for name, runs in batsman_chart.items()
                    if name and name != "N/A"
                }

                if batsman_chart:

                    st.bar_chart(
                        batsman_chart
                    )



                # =================================================
                # LATEST COMMENTARY
                # =================================================

                st.subheader(
                    "💬 Latest Commentary"
                )

                commentary_items = data.get(
                    "matchCommentary",
                    {}
                )

                commentary_list = [
                    item
                    for item in commentary_items.values()
                    if item.get("commType") == "commentary"
                    and item.get("commText")
                ]


                commentary_list.sort(
                    key=lambda x: x.get(
                        "timestamp",
                        0
                    ),
                    reverse=True
                )


                if commentary_list:

                    for item in commentary_list[:5]:

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
                            prefix += (
                                f"**{team_name}** "
                            )

                        if innings_id:
                            prefix += (
                                f"(Innings {innings_id}) "
                            )

                        st.write(
                            f"• {prefix}{text}",
                            unsafe_allow_html=True
                        )

                else:

                    st.info(
                        "No commentary available."
                    )


                st.divider()


                # =================================================
                # LAST WICKET
                # =================================================

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


                # =================================================
                # RECENT OVERS
                # =================================================

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


                # =================================================
                # LAST REFRESH
                # =================================================

                refresh_time = datetime.now().strftime(
                    "%H:%M:%S"
                )

                st.caption(
                    f"🔄 Auto-refresh every 10 seconds"
                    f" | Last refresh: {refresh_time}"
                )


            except Exception as e:

                st.error(
                    f"Unable to fetch Cricbuzz score: {e}"
                )


        # ========================================================
        # RUN LIVE MATCH COMPONENT
        # ========================================================

        show_live_match()

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