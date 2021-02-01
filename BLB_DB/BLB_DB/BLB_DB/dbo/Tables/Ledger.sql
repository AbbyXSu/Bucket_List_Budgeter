CREATE TABLE [dbo].[Ledger]
(
	[event_id] INT NOT NULL PRIMARY KEY IDENTITY(1,1), 
    [Budgeter_ID] INT NOT NULL, 
    [Action_ID] INT NOT NULL, 
    [Value_in_GBP] INT NOT NULL, 
    [Action_date] DATE NOT NULL DEFAULT GETDATE(), 
    CONSTRAINT [FK_Ledger_ToTable] FOREIGN KEY (Budgeter_ID) REFERENCES [BudgetSummary]([Budgeter_ID])
)
