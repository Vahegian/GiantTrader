# Giant Trader 
[Demo](https://www.linkedin.com/embed/feed/update/urn:li:ugcPost:6644926669507317760?compact=1)

The software can connect to "Binance" exchange and perform trades with different neural networks or hardcoded rules. It provides a user interface with charts and feedback text describing the current state. 

## Backend 
* Flask, Flask-Restful
* TensorFlow 1.5
* Keras
* numpy
* OpenCV 3
* PostgreSQL and SQLite3 (depends on a service)

## Frontend
* AngularJs
* nginx

## Architecture
* Microservices
* Docker (For managing services)


        1.Type "docker-compose up -d" in folder "docker" to start the software 

        2.Navigate to localhost:10003

## UI

<h3> Login Page. </h3> 
<h3>Users can be created by inserting username, password, apiKey and apiSecret into table "utable" in "binance" service. </h3>
<img src="other_files/login.png" width=640></img>
<hr>
<h3> Select asset to trade from top panel, it can only be changed here, so every operation uses selected asset until it is changed. </h3>
<img src="other_files/top_panel.png" width=640></img>
<hr>
<h3>Basic exchange functionality for quick limit or market orders.</h3>
<h3>Live view of currently open orders and wallet.</h3>
<img src="other_files/exCharts.png" width=640></img>
<img src="other_files/ex.png" width=640></img>
<hr>
<h3>A Deep Neural Network is beating a market. This means if the DNN were to trade for you instead of holding you will loos less as the market falls.</h3>
<img src="other_files/PCNN.png" width=640></img>
<hr>
<h3>Here you can starts bots, which will trade for you. You can have as many bots as you want for every pair. The bots will trade if they have access to $11. For example if you have $100 this will allow 9 bots to run at the same time.</h3>
<img src="other_files/bot.png" width=640></img>
<br>
<h3>RollingDay means the bot will close its position at the end of the day regardless of the trade status. </h3> 

<h3>As long as the server is running the bots will continue trading even if you close the browser. To stop the bots, press on the remove button and wait "for some bots it can take more than 3 minutes to stop".
To immediately prevent bots from placing orders just log out the user from the top panel or stop the server by typing on terminal: </h3>


        docker-compose down 
<h3>in "docker" folder</h3>

<hr>

