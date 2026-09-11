import sys
from datetime import datetime

from utils.cricbuzz_api import get_match_commentary
from utils.db_connection import get_connection


# ============================================================
# HELPER - CONVERT API STATUS TO MYSQL STATUS
# ============================================================

def convert_status(api_state):
    state = str(api_state or "").lower()

    if state == "complete":
        return "Completed"

    if state in ("in progress", "live"):
        return "Live"

    if state in ("scheduled", "preview"):
        return "Scheduled"

    return "Live"


# ============================================================
# HELPER - CONVERT OVERS TO BALLS
# Example:
# 33.4 -> 33 overs + 4 balls = 202 balls
# ============================================================

def overs_to_balls(overs):
    if overs is None:
        return 0

    try:
        value = float(overs)

        completed_overs = int(value)
        balls = round((value - completed_overs) * 10)

        if balls < 0:
            balls = 0

        if balls > 5:
            balls = 0

        return completed_overs * 6 + balls

    except (TypeError, ValueError):
        return 0


# ============================================================
# FIND INTERNAL MYSQL TEAM ID USING TEAM NAME
# ============================================================

def get_team_id(cursor, team_name):

    if not team_name:
        return None

    cursor.execute(
        """
        SELECT team_id
        FROM teams
        WHERE team_name = %s
        LIMIT 1
        """,
        (team_name,)
    )

    row = cursor.fetchone()

    if row:
        return row[0]

    return None


# ============================================================
# FIND INTERNAL MYSQL MATCH ID
# ============================================================

def get_mysql_match_id(cursor, api_match_id):

    cursor.execute(
        """
        SELECT match_id
        FROM matches
        WHERE api_match_id = %s
        LIMIT 1
        """,
        (str(api_match_id),)
    )

    row = cursor.fetchone()

    if row:
        return row[0]

    return None


# ============================================================
# UPDATE MATCH BASIC INFORMATION
# ============================================================

def sync_match_header(
    cursor,
    mysql_match_id,
    header
):

    status = convert_status(
        header.get("state")
    )

    toss = header.get(
        "tossResults",
        {}
    )

    toss_winner_name = toss.get(
        "tossWinnerName"
    )

    toss_decision_api = str(
        toss.get("decision", "")
    ).lower()

    toss_decision = None

    if toss_decision_api == "batting":
        toss_decision = "Bat"

    elif toss_decision_api == "bowling":
        toss_decision = "Field"

    toss_winner_id = get_team_id(
        cursor,
        toss_winner_name
    )

    winner_name = (
        header.get("result", {})
        .get("winningTeam")
    )

    winner_team_id = get_team_id(
        cursor,
        winner_name
    )

    result = header.get(
        "result",
        {}
    )

    margin_value = None
    margin_type = None

    if result.get("winByRuns"):
        margin_value = result.get(
            "winningMargin"
        )
        margin_type = "Runs"

    elif result.get("winByWickets"):
        margin_value = result.get(
            "winningMargin"
        )
        margin_type = "Wickets"

    cursor.execute(
        """
        UPDATE matches
        SET
            status = %s,
            toss_winner_team_id = %s,
            toss_decision = %s,
            winner_team_id = %s,
            win_margin_value = %s,
            win_margin_type = %s
        WHERE match_id = %s
        """,
        (
            status,
            toss_winner_id,
            toss_decision,
            winner_team_id,
            margin_value,
            margin_type,
            mysql_match_id
        )
    )


# ============================================================
# SYNC MATCH TEAMS
# ============================================================

def sync_match_teams(
    cursor,
    mysql_match_id,
    header,
    innings_list
):

    team1 = header.get(
        "team1",
        {}
    )

    team2 = header.get(
        "team2",
        {}
    )

    team1_name = (
        team1.get("name")
        or team1.get("shortName")
    )

    team2_name = (
        team2.get("name")
        or team2.get("shortName")
    )

    team1_id = get_team_id(
        cursor,
        team1_name
    )

    team2_id = get_team_id(
        cursor,
        team2_name
    )

    if not team1_id or not team2_id:
        print(
            "Warning: one or both teams "
            "are missing in MySQL."
        )
        return


    # --------------------------------------------------------
    # Determine batting-first team
    # --------------------------------------------------------

    batting_first_team_id = None

    if innings_list:

        first_innings = innings_list[0]

        first_batting_api_name = (
            first_innings.get(
                "batTeamName"
            )
        )

        if first_batting_api_name == (
            team1.get("shortName")
        ):

            batting_first_team_id = team1_id

        elif first_batting_api_name == (
            team2.get("shortName")
        ):

            batting_first_team_id = team2_id


    # --------------------------------------------------------
    # Get latest score per team
    # --------------------------------------------------------

    team_scores = {}

    for innings in innings_list:

        team_name = innings.get(
            "batTeamName"
        )

        score = innings.get(
            "score",
            0
        )

        wickets = innings.get(
            "wickets",
            0
        )

        if team_name:

            team_scores[team_name] = (
                score,
                wickets
            )


    # --------------------------------------------------------
    # Prepare team rows
    # --------------------------------------------------------

    team_data = []

    for mysql_team_id, api_short_name in [
        (
            team1_id,
            team1.get("shortName")
        ),
        (
            team2_id,
            team2.get("shortName")
        )
    ]:

        score = None
        wickets = None

        if api_short_name in team_scores:

            score, wickets = team_scores[
                api_short_name
            ]

        batting_first = (
            1
            if mysql_team_id == batting_first_team_id
            else 0
        )

        team_data.append(
            (
                mysql_match_id,
                mysql_team_id,
                batting_first,
                score,
                wickets
            )
        )


    # --------------------------------------------------------
    # Insert or update
    # --------------------------------------------------------

    for row in team_data:

        cursor.execute(
            """
            SELECT match_id
            FROM match_teams
            WHERE match_id = %s
              AND team_id = %s
            LIMIT 1
            """,
            (
                row[0],
                row[1]
            )
        )

        exists = cursor.fetchone()

        if exists:

            cursor.execute(
                """
                UPDATE match_teams
                SET
                    batting_first = %s,
                    team_score = %s,
                    team_wickets = %s
                WHERE match_id = %s
                  AND team_id = %s
                """,
                (
                    row[2],
                    row[3],
                    row[4],
                    row[0],
                    row[1]
                )
            )

        else:

            cursor.execute(
                """
                INSERT INTO match_teams
                (
                    match_id,
                    team_id,
                    batting_first,
                    team_score,
                    team_wickets
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                row
            )


# ============================================================
# SYNC INNINGS
# ============================================================

def sync_innings(
    cursor,
    mysql_match_id,
    header,
    innings_list
):

    team1 = header.get(
        "team1",
        {}
    )

    team2 = header.get(
        "team2",
        {}
    )

    team1_mysql_id = get_team_id(
        cursor,
        team1.get("name")
    )

    team2_mysql_id = get_team_id(
        cursor,
        team2.get("name")
    )

    if not team1_mysql_id or not team2_mysql_id:
        print(
            "Warning: team mapping missing. "
            "Skipping innings."
        )
        return


    for innings in innings_list:

        innings_number = innings.get(
            "inningsId"
        )

        bat_short_name = innings.get(
            "batTeamName"
        )

        if bat_short_name == team1.get(
            "shortName"
        ):
            batting_team_id = team1_mysql_id
            bowling_team_id = team2_mysql_id

        elif bat_short_name == team2.get(
            "shortName"
        ):
            batting_team_id = team2_mysql_id
            bowling_team_id = team1_mysql_id

        else:
            continue


        total_runs = innings.get(
            "score",
            0
        )

        total_wickets = innings.get(
            "wickets",
            0
        )

        total_balls = innings.get(
            "ballNbr"
        )

        if total_balls is None:

            total_balls = overs_to_balls(
                innings.get("overs", 0)
            )


        # ----------------------------------------------------
        # Check whether innings exists
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT innings_id
            FROM innings
            WHERE match_id = %s
              AND innings_number = %s
            LIMIT 1
            """,
            (
                mysql_match_id,
                innings_number
            )
        )

        row = cursor.fetchone()


        if row:

            cursor.execute(
                """
                UPDATE innings
                SET
                    batting_team_id = %s,
                    bowling_team_id = %s,
                    total_runs = %s,
                    total_wickets = %s,
                    total_balls = %s
                WHERE innings_id = %s
                """,
                (
                    batting_team_id,
                    bowling_team_id,
                    total_runs,
                    total_wickets,
                    total_balls,
                    row[0]
                )
            )

        else:

            cursor.execute(
                """
                INSERT INTO innings
                (
                    match_id,
                    innings_number,
                    batting_team_id,
                    bowling_team_id,
                    total_runs,
                    total_wickets,
                    total_balls
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    mysql_match_id,
                    innings_number,
                    batting_team_id,
                    bowling_team_id,
                    total_runs,
                    total_wickets,
                    total_balls
                )
            )


# ============================================================
# SYNC COMMENTARY
# ============================================================

def sync_commentary(
    cursor,
    mysql_match_id,
    api_data
):

    items = (
        api_data
        .get("matchCommentary", {})
        .values()
    )

    inserted = 0
    skipped = 0


    for item in items:

        if item.get(
            "commType"
        ) != "commentary":
            continue


        commentary_text = item.get(
            "commText"
        )

        if not commentary_text:
            continue


        timestamp_ms = item.get(
            "timestamp"
        )


        cursor.execute(
            """
            SELECT commentary_id
            FROM commentary
            WHERE match_id = %s
              AND timestamp_ms = %s
            LIMIT 1
            """,
            (
                mysql_match_id,
                timestamp_ms
            )
        )


        if cursor.fetchone():

            skipped += 1
            continue


        batsman = (
            item.get("batsmanDetails")
            or {}
        )

        bowler = (
            item.get("bowlerDetails")
            or {}
        )


        cursor.execute(
            """
            INSERT INTO commentary
            (
                match_id,
                innings_id,
                comm_type,
                commentary_text,
                team_name,
                event_type,
                timestamp_ms,
                batsman_api_id,
                batsman_name,
                bowler_api_id,
                bowler_name
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                mysql_match_id,

                item.get(
                    "inningsId"
                ),

                item.get(
                    "commType"
                ),

                commentary_text,

                item.get(
                    "teamName"
                ),

                None,

                timestamp_ms,

                (
                    str(
                        batsman.get(
                            "playerId"
                        )
                    )
                    if batsman.get(
                        "playerId"
                    )
                    else None
                ),

                batsman.get(
                    "playerName"
                ),

                (
                    str(
                        bowler.get(
                            "playerId"
                        )
                    )
                    if bowler.get(
                        "playerId"
                    )
                    else None
                ),

                bowler.get(
                    "playerName"
                )
            )
        )

        inserted += 1


    print(
        "Commentary inserted:",
        inserted
    )

    print(
        "Commentary skipped:",
        skipped
    )


# ============================================================
# MAIN SYNC FUNCTION
# ============================================================

def sync_match(api_match_id):

    print(
        "\nStarting sync for API match:",
        api_match_id
    )

    # --------------------------------------------------------
    # Fetch Cricbuzz API
    # --------------------------------------------------------

    api_data = get_match_commentary(
        api_match_id
    )

    header = api_data.get(
        "matchHeader",
        {}
    )

    mini = api_data.get(
        "miniscore",
        {}
    )

    match_score_details = mini.get(
        "matchScoreDetails",
        {}
    )

    innings_list = match_score_details.get(
        "inningsScoreList",
        []
    )


    # --------------------------------------------------------
    # Open MySQL
    # --------------------------------------------------------

    conn = get_connection()
    cursor = conn.cursor()


    try:

        # ----------------------------------------------------
        # Find internal match
        # ----------------------------------------------------

        mysql_match_id = get_mysql_match_id(
            cursor,
            api_match_id
        )

        if not mysql_match_id:

            raise ValueError(
                f"MySQL match not found for API ID "
                f"{api_match_id}. Create the match first."
            )


        print(
            "MySQL match_id:",
            mysql_match_id
        )


        # ----------------------------------------------------
        # Sync match header
        # ----------------------------------------------------

        sync_match_header(
            cursor,
            mysql_match_id,
            header
        )


        # ----------------------------------------------------
        # Sync teams
        # ----------------------------------------------------

        sync_match_teams(
            cursor,
            mysql_match_id,
            header,
            innings_list
        )


        # ----------------------------------------------------
        # Sync innings
        # ----------------------------------------------------

        sync_innings(
            cursor,
            mysql_match_id,
            header,
            innings_list
        )


        # ----------------------------------------------------
        # Sync commentary
        # ----------------------------------------------------

        sync_commentary(
            cursor,
            mysql_match_id,
            api_data
        )


        # ----------------------------------------------------
        # Commit all changes
        # ----------------------------------------------------

        conn.commit()

        print(
            "Match sync completed successfully."
        )


    except Exception as e:

        conn.rollback()

        print(
            "Sync failed:",
            e
        )

        raise


    finally:

        cursor.close()
        conn.close()


# ============================================================
# COMMAND LINE
# ============================================================

if __name__ == "__main__":

    if len(sys.argv) > 1:

        api_match_id = sys.argv[1]

    else:

        api_match_id = "169980"


    sync_match(api_match_id)