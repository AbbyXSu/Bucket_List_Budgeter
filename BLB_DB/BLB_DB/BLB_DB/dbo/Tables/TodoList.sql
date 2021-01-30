CREATE TABLE [dbo].[TodoList]
(
	[Todo_List_ID] INT NOT NULL IDENTITY(1,1) PRIMARY KEY, 
    [Username] VARCHAR(50) NOT NULL, 
    [Number_of_items] TINYINT NOT NULL DEFAULT 0, 
    [Total_Costs] INT NOT NULL DEFAULT 0, 
    CONSTRAINT [FK_TodoList_ToTable] FOREIGN KEY ([Username]) REFERENCES [Users]([Username])
)