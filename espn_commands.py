def get_projected_total(lineup):
    total_projected = 0
    for i in lineup:
        if i.slot_position != "BE" and i.slot_position != "IR":
            if i.points != 0 or i.game_played > 0:
                total_projected += i.points
            else:
                total_projected += i.projected_points
    return total_projected


def get_matchups(league, week=None):
    # Gets current week's Matchups
    matchups = league.box_scores(week=week)

    score = [
        "**%s** (%s-%s) vs **%s** (%s-%s)"
        % (
            i.home_team.team_name,
            i.home_team.wins,
            i.home_team.losses,
            i.away_team.team_name,
            i.away_team.wins,
            i.away_team.losses,
        )
        for i in matchups
        if i.away_team
    ]

    text = ["Matchups"] + score
    return "\n".join(text)


def get_projected_scoreboard(league, week=None):
    # Gets current week's scoreboard projections
    box_scores = league.box_scores(week=week)
    score = [
        "%s %.2f - %.2f %s"
        % (
            i.home_team.team_abbrev,
            get_projected_total(i.home_lineup),
            get_projected_total(i.away_lineup),
            i.away_team.team_abbrev,
        )
        for i in box_scores
        if i.away_team
    ]
    text = ["Approximate Projected Scores"] + score
    return "\n".join(text)


def get_power_rankings(league, week=None):
    # power rankings requires an integer value, so this grabs the current week for that
    if not week:
        week = league.current_week
    # Gets current week's power rankings
    # Using 2 step dominance, as well as a combination of points scored and margin of victory.
    # It's weighted 80/15/5 respectively
    power_rankings = league.power_rankings(week=week)

    power_rankings = sorted(
        power_rankings, key=lambda tup: tup[1].playoff_pct, reverse=True
    )

    score = [
        "%s (%.1f%%) - %s" % (i[0], i[1].playoff_pct, i[1].team_name)
        for i in power_rankings
        if i
    ]

    text = ["Power Rankings (Playoff %)"] + score
    return "\n".join(text)


def get_scoreboard_short(league, week=None):
    # Gets current week's scoreboard
    box_scores = league.box_scores(week=week)
    score = [
        "%s %.2f - %.2f %s"
        % (i.home_team.team_abbrev, i.home_score, i.away_score, i.away_team.team_abbrev)
        for i in box_scores
        if i.away_team
    ]
    text = ["The current scores are:"] + score
    return "\n".join(text)
