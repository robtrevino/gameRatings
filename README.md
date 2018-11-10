# gameRatings
This repository is for a simple alexa skill that will allow you to query a database for a game rating. I purposedly left it super simple so that it's easy to follow for those that have not built a skill before.

The skill will take the input of "Can you give me a rating for Mario Maker" and will query the api for a rating then play it back. The API has a lot more features, feel free to build upon it.

Use the config.ini file to put in your key from Game Ratings (https://www.igdb.com/api) and the skill ID from your Alexa skill. The zip up the whole repository, upload it to Lambda and use it as the endpoint when building the skill.