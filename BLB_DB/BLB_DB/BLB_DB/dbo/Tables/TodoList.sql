CREATE TABLE [dbo].[TodoList]
(
	[Todo_List_ID] INT UNIQUE NOT NULL PRIMARY KEY, 
    [Username] VARCHAR(50) NOT NULL, 
    [Number_of_items] TINYINT NOT NULL, 
    [Total_Costs] INT NOT NULL, 
    CONSTRAINT [FK_TodoList_ToTable] FOREIGN KEY ([Username]) REFERENCES [Users]([Username])
)
