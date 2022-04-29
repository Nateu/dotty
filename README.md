# Dotty chat bot
This is a generic chat bot script in Python. It isn't coupled with and chat platform, framework or service at this point.  
It is partly storing data in AWS DynamoDB, persistent storage is for User Profiles only so far. This will be extended in the near future to Substitution Commands and User activity tracking.  


## Todos
* Add support for tracking user last text post timestamp
* Add support for tracking user last image/video post timestamp
* Add support for tracking user last message read timestamp
* Tracking data should be persisted as well
* Add storage of Substitution Commands
* Add retrieval of stored Substitution Commands
* Add a command to remove Substitution Command
* Improve user list to sort by Security Level and identify with heading only

