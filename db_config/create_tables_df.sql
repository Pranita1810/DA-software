USE EDA_PROJECT

CREATE TABLE Orders(
OrderID INT,
CustomerID INT,
ProductID INT,
OrderDate DATE,
Quantity INT,
TotalSales DECIMAL(10,2)
)

CREATE TABLE Products(
ProductID INT,
ProductName VARCHAR(100),
Category VARCHAR(60),
UnitPrice DECIMAL(10,2),
Supplier VARCHAR(50)
)

CREATE TABLE Customers(
CustomerID INT,
CustomerName VARCHAR(50),
Region VARCHAR(50),
Age INT,
Gender VARCHAR(10),
CustomerSince DATE,
Email VARCHAR(100)
)

SELECT * FROM Customers
SELECT * FROM Orders
SELECT * FROM Products