This project splits predefined set of Twitter users into clusters based on their recent Tweets.
How it works:
 1. Input requires a text file with single Twitter ID per row
 2. Copy config.yml.dist to config.yml and fill/set parameters
 3. Run `import_tweets.py` to fetch recent users Tweets
 4. Run `cluster_users.py` to print information about users clusters
 
 Requires Python 3.5+
