-- 创建退保率统计表
CREATE TABLE IF NOT EXISTS SurrenderRateStats (
    StatDate DATE,
    SurrenderRate DECIMAL(5,2),
    StatPeriod VARCHAR(10)
);

-- 计算并插入按日统计的退保率
INSERT INTO SurrenderRateStats (StatDate, SurrenderRate, StatPeriod)
SELECT 
    DATE(S.SurrenderDate) AS StatDate,
    (SUM(S.SurrenderAmount) / (SUM(R.ReserveAmount) + SUM(P.PremiumAmount))) * 100 AS SurrenderRate,
    '日' AS StatPeriod
FROM 
    Surrender S
JOIN 
    Reserve R ON R.ReserveType IN ('期初寿险责任准备金', '期初长期健康险责任准备金')
JOIN 
    Premium P ON S.PolicyID = P.PolicyID
WHERE 
    DATE(S.SurrenderDate) = CURDATE() -- 假设只计算当天的退保率
GROUP BY 
    StatDate;
-- 创建未决赔款准备金与赔款支出比统计表
CREATE TABLE IF NOT EXISTS ClaimReserveRatioStats (
    StatDate DATE,
    ClaimReserveRatio DECIMAL(5,2),
    StatPeriod VARCHAR(10)
);

-- 计算并插入按日统计的未决赔款准备金与赔款支出比
INSERT INTO ClaimReserveRatioStats (StatDate, ClaimReserveRatio, StatPeriod)
SELECT 
    DATE(C.ClaimDate) AS StatDate,
    (SUM(R.ReserveAmount - R.RecoveredReserveAmount) / SUM(C.ClaimAmount - C.RecoveredClaimAmount)) * 100 AS ClaimReserveRatio,
    '日' AS StatPeriod
FROM 
    Claim C
JOIN 
    Reserve R ON C.ClaimID = R.ClaimID AND R.ReserveType = '未决赔款准备金'
WHERE 
    DATE(C.ClaimDate) = CURDATE() -- 假设只计算当天的比例
GROUP BY 
    StatDate;
-- 创建已付赔款赔付率统计表
CREATE TABLE IF NOT EXISTS PaidClaimRatioStats (
    StatYear INT,
    PaidClaimRatio DECIMAL(5,2)
);

-- 计算并插入按业务年度统计的已付赔款赔付率
INSERT INTO PaidClaimRatioStats (StatYear, PaidClaimRatio)
SELECT 
    YEAR(C.ClaimDate) AS StatYear,
    (SUM(C.ClaimAmount) / SUM(P.PremiumAmount)) * 100 AS PaidClaimRatio
FROM 
    Claim C
JOIN 
    Policy P ON C.PolicyID = P.PolicyID
WHERE 
    C.ClaimStatus = '已决'
GROUP BY 
    StatYear;
-- 创建已报告赔款赔付率统计表
CREATE TABLE IF NOT EXISTS ReportedClaimRatioStats (
    StatYear INT,
    ReportedClaimRatio DECIMAL(5,2)
);

-- 计算并插入按业务年度统计的已报告赔款赔付率
INSERT INTO ReportedClaimRatioStats (StatYear, ReportedClaimRatio)
SELECT 
    YEAR(C.ClaimDate) AS StatYear,
    ((SUM(C.ClaimAmount) + SUM(R.ReserveAmount)) / SUM(P.PremiumAmount)) * 100 AS ReportedClaimRatio
FROM 
    Claim C
JOIN 
    Reserve R ON C.ClaimID = R.ClaimID AND R.ReserveType = '已发生已报告未决赔款准备金'
JOIN 
    Policy P ON C.PolicyID = P.PolicyID
WHERE 
    C.ClaimStatus IN ('已决', '已报告未决')
GROUP BY 
    StatYear;
-- 创建业务年度赔付率统计表
CREATE TABLE IF NOT EXISTS AnnualClaimRatioStats (
    StatYear INT,
    AnnualClaimRatio DECIMAL(5,2)
);

-- 计算并插入按业务年度统计的业务年度赔付率
INSERT INTO AnnualClaimRatioStats (StatYear, AnnualClaimRatio)
SELECT 
    YEAR(C.ClaimDate) AS StatYear,
    ((SUM(C.ClaimAmount) + SUM(R1.ReserveAmount) + SUM(R2.ReserveAmount)) / SUM(P.PremiumAmount)) * 100 AS AnnualClaimRatio
FROM 
    Claim C
LEFT JOIN 
    Reserve R1 ON C.ClaimID = R1.ClaimID AND R1.ReserveType = '已发生已报告未决赔款准备金'
LEFT JOIN 
    Reserve R2 ON C.ClaimID = R2.ClaimID AND R2.ReserveType = '已发生未报告未决赔款准备金'
JOIN 
    Policy P ON C.PolicyID = P.PolicyID
GROUP BY 
    StatYear;
-- 创建综合资本成本率统计表
CREATE TABLE IF NOT EXISTS CapitalCostRateStats (
    StatDate DATE,
    CapitalCostRate DECIMAL(5,2)
);

-- 计算并插入综合资本成本率
INSERT INTO CapitalCostRateStats (StatDate, CapitalCostRate)
SELECT 
    CURDATE() AS StatDate,
    SUM(CC.CapitalAmount * CC.CapitalCostRate) / SUM(CC.CapitalAmount) AS CapitalCostRate
FROM 
    CapitalCost CC;