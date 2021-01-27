﻿CREATE LOGIN [BLBAPP] WITH PASSWORD = 'password' MUST_CHANGE, DEFAULT_DATABASE=[BLB_DB], DEFAULT_LANGUAGE=[us_english], CHECK_EXPIRATION=ON, CHECK_POLICY=ON;
GO
ALTER SERVER ROLE [sysadmin] ADD MEMBER [BLBAPP];
GO
ALTER SERVER ROLE [serveradmin] ADD MEMBER [BLBAPP];



