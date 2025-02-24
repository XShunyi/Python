-- 保单表
CREATE TABLE Policy (
    PolicyID INT PRIMARY KEY AUTO_INCREMENT,
    PolicyNumber VARCHAR(50) NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    PremiumAmount DECIMAL(15,2) NOT NULL
);

-- 退保表
CREATE TABLE Surrender (
    SurrenderID INT PRIMARY KEY AUTO_INCREMENT,
    PolicyID INT,
    SurrenderDate DATE NOT NULL,
    SurrenderAmount DECIMAL(15,2) NOT NULL,
    FOREIGN KEY (PolicyID) REFERENCES Policy(PolicyID)
);

-- 赔案表
CREATE TABLE Claim (
    ClaimID INT PRIMARY KEY AUTO_INCREMENT,
    PolicyID INT,
    ClaimDate DATE NOT NULL,
    ClaimAmount DECIMAL(15,2) NOT NULL,
    ClaimStatus VARCHAR(20) NOT NULL,
    FOREIGN KEY (PolicyID) REFERENCES Policy(PolicyID)
);

-- 准备金表
CREATE TABLE Reserve (
    ReserveID INT PRIMARY KEY AUTO_INCREMENT,
    ClaimID INT,
    ReserveType VARCHAR(50) NOT NULL,
    ReserveAmount DECIMAL(15,2) NOT NULL,
    RecoveredReserveAmount DECIMAL(15,2) DEFAULT 0,
    FOREIGN KEY (ClaimID) REFERENCES Claim(ClaimID)
);

-- 资本成本表
CREATE TABLE CapitalCost (
    CapitalCostID INT PRIMARY KEY AUTO_INCREMENT,
    CapitalAmount DECIMAL(15,2) NOT NULL,
    CapitalCostRate DECIMAL(5,2) NOT NULL
);

-- 插入保单数据
INSERT INTO Policy (PolicyNumber, StartDate, EndDate, PremiumAmount) VALUES
('P001', '2024-01-01', '2025-01-01', 10000.00),
('P002', '2024-02-01', '2025-02-01', 15000.00),
('P003', '2024-03-01', '2025-03-01', 20000.00),
('P010', '2024-10-01', '2025-10-01', 50000.00);

-- 插入退保数据
INSERT INTO Surrender (PolicyID, SurrenderDate, SurrenderAmount) VALUES
(1, '2024-06-01', 5000.00),
(2, '2024-07-01', 7500.00),
(10, '2024-12-01', 25000.00);

-- 插入赔案数据
INSERT INTO Claim (PolicyID, ClaimDate, ClaimAmount, ClaimStatus) VALUES
(1, '2024-04-01', 3000.00, '已决'),
(2, '2024-05-01', 4500.00, '已报告未决'),
(3, '2024-06-01', 6000.00, '已决'),
(10, '2024-12-15', 15000.00, '已决');

-- 插入准备金数据
INSERT INTO Reserve (ClaimID, ReserveType, ReserveAmount, RecoveredReserveAmount) VALUES
(1, '未决赔款准备金', 3000.00, 0),
(2, '已发生已报告未决赔款准备金', 4500.00, 1500.00),
(3, '未决赔款准备金', 6000.00, 3000.00),
(10, '已发生未报告未决赔款准备金', 15000.00, 0);

-- 插入资本成本数据
INSERT INTO CapitalCost (CapitalAmount, CapitalCostRate) VALUES
(1000000.00, 4.50),
(2000000.00, 4.00),
(5000000.00, 3.50);

