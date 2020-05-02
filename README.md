# Twitter_Database
Course project for DBMS: Creating multiple databases to store tweets and building search applications.

Data collection: We have collected the data using the keyword “US Economy”. We have about 29000 tweets.

Data Preprocessing: The downloaded data is a JSON file which is a dictionary of
dictionaries. We loaded the data and converted it into a pandas DataFrame. We separated the
‘user’ data from it and stored it in another DataFrame. We removed the other language entries
from our data.

Systems used for Data Storage:
1. MongoDB
We are using MongoDB as a Non-Relational database for our project. PyMongo is a
python library for interacting with MongoDB database from the python interface. We
completed the installation of MongoDB and PyMongo on our laptop. For the next step,
we have set up a connection with MongoClient and created a database and a collection
inside it to store the Twitter data. The data is already in the recommended JSON format
and is ready to be inserted into the collection. Lastly, we imported our data to MongoDB.
Note that we are not going to insert the user data from the output.
2. Postgres
We are using Postgres as a Relational database for our project. We converted the twitter
data JSON file into Pandas DataFrame to extract the ‘user’ information and stored it as a
DataFrame along with ‘tweet_id’. Using SqlAlchemy in Python, we then created a
database in Postgres and stored the ‘user’ DataFrame.
3. Redis:
We used Redis for the catching

Search Application:
The search application is divided into three-parts. First, Search application for queries
based on data in PostgreSQL. Second, Search application for data based in MongoDB.
Third, Search Application for queries based on the combination of both MongoDB and
Postgres database. First two we will get the results in the Jupyter notebook environment
and show in pandas data frame format. For third, we will retrieve the corresponding
results from each database and stored in a pandas data format. Then we will combine
results using pandas operations. We have common ID for both databases which we
have created using hashing function on tweetID(tweetID will always be unique)
We are using Postgres SQL for the relational queries and MongoDB CRUD operations
for tweet text related queries.
Following are the possible ways we plan to use the Search application scenarios discussed
above:
1. First Scenario(Postgres based queries) :
Postgres to find Summary of retweet_count, favorite_count, reply_count etc for
tweet based on US Economy.
We will use data from Postgres to get the name of the users who tweets the most
about the US economy.
2. Second Scenario(MongoDb based queries) :
MongoDB to find Tweet containing certain words. Such as: how many tweets \
the word ‘trump’ occur along with the ‘US Economy’.
We can use MongoDB to find the average length of the tweet
What is the most frequent hashtag in our tweet collection?
Running MapReduce to count certain words.
3. Third Scenario(Combination of them both for queries) :
Get the name of the user from Postgres whose tweet got the most retweets from
the data coming via MongoDB.
User Interface web application for the search application: We are planning to use python
flask tools for generating websites for search applications. We already created a basic website
for running backend python code and showing the basic results (such as addition) on the web
interface. We need to work on showing the output of the panda’s data frame through the flask
