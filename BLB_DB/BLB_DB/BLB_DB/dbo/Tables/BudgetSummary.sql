CREATE TABLE [dbo].[BudgetSummary]
(
    [Username] varchar(50) NOT NULL,
	[Budgeter_Id] INT IDENTITY(1,1) PRIMARY KEY, 
    [Balance] DECIMAL(10, 2) NOT NULL DEFAULT 0.00, 
    [Last_Update] DATE NOT NULL DEFAULT GETDATE(), 
    CONSTRAINT [FK_BudgetSummary_Users] FOREIGN KEY ([Username]) REFERENCES [Users]([Username])
)
