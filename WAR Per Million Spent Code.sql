WITH team_war AS (
    SELECT 
        Team,
        SUM(WAR) as total_war
    FROM (
        SELECT Team, WAR FROM batting_war
        UNION ALL
        SELECT Team, WAR FROM pitching_war
    ) combined
    GROUP BY Team
)
SELECT 
    tw.Team,
    tw.total_war,
    p.total_payroll_allocations,
    ROUND((tw.total_war / (p.total_payroll_allocations / 1000000.0))::numeric, 2) as war_per_million
FROM team_war tw
JOIN mlb_team_payroll_2025 p ON tw.Team = p.team
ORDER BY war_per_million DESC;