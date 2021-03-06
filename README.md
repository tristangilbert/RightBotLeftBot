# RightBotLeftBot
### Tristan Gilbert

RightBotLeftBot is a reddit bot that analyzes reddit users' political leanings. It finds reddit posts about controversial political topics and replies with a top level comment that guesses the severity and direction of the post author's political inclinations.

The project is written in Python and uses the reddit API with PRAW wrapper and IBM's Watson Natural Language Classifier service/API.

The bot first finds controversial posts by keyword. It then finds the author's most recent comments, and sends them individually to the language classifier, which has been trained from ~500 of the top comments on several conservative and liberal subreddits. The classifier replies with a classification (liberal or conservative) for each comment and a reported confidence. These values are compiled by the bot into a single classifaction and confidence. The bot replies to the reddit post with a top level comment reporting these results.

The file BiasChecker is the bot itself, and TrainingDataCollector pulls the comments used to train Watson NLC
