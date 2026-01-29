-- Hard Hit Rate Calculation
SELECT batter,
        SUM(CASE WHEN PitchCall = 'InPlay' AND ExitSpeed >= 95 THEN 1 ELSE 0 END) AS HardHitCount,
        SUM(CASE WHEN PitchCall = 'InPlay' THEN 1 ELSE 0 END) AS TotalInPlay,
        ROUND(SUM(CASE WHEN PitchCall = 'InPlay' AND ExitSpeed >= 95 THEN 1 ELSE 0 END) * 100.0 /
              NULLIF(SUM(CASE WHEN PitchCall = 'InPlay' THEN 1 ELSE 0 END), 0), 2) AS HardHitRate
FROM your_table_name
GROUP BY batter
ORDER BY HardHitRate DESC;

-- Average Exit Velocity
SELECT Batter,
        COUNT(*) AS num_hits,
         ROUND(AVG(ExitSpeed), 2) AS AverageExitVelocity,
         MAX(ExitSpeed) AS MaxExitVelocity
FROM your_table_name
WHERE PitchCall = 'InPlay' AND ExitSpeed IS NOT NULL
GROUP BY Batter
ORDER BY AverageExitVelocity DESC;

--Barrel Rate Calculation
SELECT Batter,
        SUM(CASE WHEN ExitSpeed >= 98 AND Angle BETWEEN 26 AND 30 THEN 1 ELSE 0 END) AS BarrelCount,
        SUM(CASE WHEN PitchCall = 'InPlay' THEN 1 ELSE 0 END) AS TotalInPlay,
        ROUND(SUM(CASE WHEN ExitSpeed >= 98 AND Angle BETWEEN 26 AND 30 THEN 1 ELSE 0 END) * 100.0 /
              NULLIF(SUM(CASE WHEN PitchCall = 'InPlay' THEN 1 ELSE 0 END), 0), 2) AS BarrelRate
FROM your_table_name
GROUP BY Batter
ORDER BY BarrelRate DESC;

-- Zone Swing Percentage
SELECT Batter, 
        COUNT(*) AS TotalPitchesInZone,
        SUM(CASE WHEN PitchCall IN ('StrikeSwinging', 'InPlay', 'FoulBallNotFieldable') THEN 1 ELSE 0 END) AS Swings,
        ROUND(SUM(CASE WHEN PitchCall IN ('StrikeSwinging', 'InPlay', 'FoulBallNotFieldable') THEN 1 ELSE 0 END) * 100.0 /
              NULLIF(COUNT(*), 0), 2) AS ZoneSwingPercentage
FROM your_table_name
WHERE PlateLocSide BETWEEN -0.85 AND 0.85
  AND PlateLocHeight BETWEEN 1.5 AND 3.5
  AND PitchCall IS NOT NULL
GROUP BY Batter
ORDER BY ZoneSwingPercentage DESC;

-- Chase Rate
SELECT 
    batter, 
    COUNT(*) AS TotalPitchesOutZone,
    SUM(CASE WHEN PitchCall IN ('StrikeSwinging', 'FoulBall', 'InPlay') THEN 1 ELSE 0 END) AS ChaseSwings,
    ROUND(
        SUM(CASE WHEN PitchCall IN ('StrikeSwinging', 'FoulBall', 'InPlay') THEN 1 ELSE 0 END) * 100.0 / 
        NULLIF(COUNT(*), 0), 
        2
    ) AS ChaseRate
FROM your_table_name
WHERE (PlateLocSide < -0.85 OR PlateLocSide > 0.85 OR PlateLocHeight < 1.5 OR PlateLocHeight > 3.5)
  AND PitchCall IS NOT NULL
GROUP BY batter
ORDER BY ChaseRate ASC; 

-- Zone Contact 
SELECT 
    batter, 
    SUM(CASE WHEN PitchCall IN ('StrikeSwinging', 'FoulBall', 'InPlay') THEN 1 ELSE 0 END) AS ZoneSwings,
    SUM(CASE WHEN PitchCall IN ('FoulBall', 'InPlay') THEN 1 ELSE 0 END) AS ZoneContact,
    ROUND(
        SUM(CASE WHEN PitchCall IN ('FoulBall', 'InPlay') THEN 1 ELSE 0 END) * 100.0 / 
        NULLIF(SUM(CASE WHEN PitchCall IN ('StrikeSwinging', 'FoulBall', 'InPlay') THEN 1 ELSE 0 END), 0), 
        2
    ) AS ZoneContactRate
FROM your_table_name
WHERE PlateLocSide BETWEEN -0.85 AND 0.85 
  AND PlateLocHeight BETWEEN 1.5 AND 3.5
GROUP BY batter
ORDER BY ZoneContactRate DESC;

-- Groundball/Flyball Percentage
SELECT 
    batter,
    -- Individual Counts
    SUM(CASE WHEN TaggedHitType = 'GroundBall' THEN 1 ELSE 0 END) AS GroundBalls,
    SUM(CASE WHEN TaggedHitType = 'FlyBall' THEN 1 ELSE 0 END) AS FlyBalls,
    SUM(CASE WHEN TaggedHitType = 'LineDrive' THEN 1 ELSE 0 END) AS LineDrives,
    SUM(CASE WHEN TaggedHitType = 'Popup' THEN 1 ELSE 0 END) AS Popups,
    
    -- Denominator: Total Batted Ball Events (BBE)
    COUNT(TaggedHitType) AS TotalBBE,

    -- Rate Calculations
    ROUND(SUM(CASE WHEN TaggedHitType = 'GroundBall' THEN 1 ELSE 0 END) * 100.0 / 
          NULLIF(COUNT(TaggedHitType), 0), 1) AS GroundBallRate,
    ROUND(SUM(CASE WHEN TaggedHitType = 'FlyBall' THEN 1 ELSE 0 END) * 100.0 / 
          NULLIF(COUNT(TaggedHitType), 0), 1) AS FlyBallRate
FROM your_table_name
WHERE PitchCall = 'InPlay' 
  AND TaggedHitType IS NOT NULL
GROUP BY batter
HAVING TotalBBE >= 10
ORDER BY FlyBallRate DESC;

--Pull/Oppo Percentage
SELECT 
    batter,
    COUNT(*) AS total_bbe,
    ROUND(SUM(CASE 
        WHEN (BatterSide = 'R' AND Bearing <= -15) OR (BatterSide = 'L' AND Bearing >= 15) THEN 1 
        ELSE 0 
    END) * 100.0 / COUNT(*), 2) AS PullPercentage,
    ROUND(SUM(CASE 
        WHEN Bearing BETWEEN -15 AND 15 THEN 1 
        ELSE 0 
    END) * 100.0 / COUNT(*), 2) AS CentPercentage,
    ROUND(SUM(CASE 
        WHEN (BatterSide = 'R' AND Bearing >= 15) OR (BatterSide = 'L' AND Bearing <= -15) THEN 1 
        ELSE 0 
    END) * 100.0 / COUNT(*), 2) AS OppoPercentage
FROM your_table_name
WHERE PitchCall = 'InPlay' 
  AND Bearing IS NOT NULL
GROUP BY batter
ORDER BY PullPercentage DESC;