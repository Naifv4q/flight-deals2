# Flights Offer Search Project
Note: This project was made along with a udemy python course, the full code was written by me, I only got the requirements of the project.
<hr />
What this program does is it looks for flight offers for the cities in the cached file, and if it finds an offer with a price less than one of the cities in the file, it sends an emails to the users in the users cached file.

## Why did I build it ?
Simply to learn how to deal with APIs in future projects.

## How to use it:
<h3>First:</h3>
You have to provide your .env file which will have those keys:

<hr />
SHEETY_USER=YOUR_API_KEY<br />
SHEETY_PASS=YOUR_API_KEY_SECRET<br />
SHEETY_AUTH=YOUR_SHEETY_AUTH<br />
<br />
MY_EMAIL = THE_EMAIL_THAT_SENDS_EMAILS<br />
MY_PASS = THE_PASS_OF_THE_ABOVE_EMAIL<br />
<br />
AMADEUS_API_KEY=YOUR_AMADEUS_API_KEY<br />
AMADEUS_API_SECRET=YOUR_AMADEUS_API_SECRET<br />
AMADEUS_TOKEN_TYPE=YOUR_AMADEUS_TOKEN_TYPE<br />
AMADEUS_TOKEN=YOUR_AMADEUS_TOKEN<br />
AMADEUS_ACCESS_TOKEN=YOUR_AMADEUS_ACCESS_TOKEN<br />
<hr />

There are a list of libraries you have to install first, and they are: (You can just copy and paste from the below commands to your cmd)
<ul>
<li>pip install pandas</li>
<li>pip install python-dotenv</li>
<li>pip install requests</li>
</ul>
The rest of the libraries are built-in python and does not need to be installed, here they are listed:
<ul>
<li>os</li>
<li>datetime</li>
<li>time</li>
<li>smtplib</li>
</ul>
<h3>Secondly:</h3>
Check the cached sample cached files, you first have to rename them to "cached_flights_sheet" and the other "cached_users_sheet", and of course both to have an .csv extension.
<h3>Lastly:</h3>
Populate the files as you see fit manually, or link them to a google sheet, like I did using sheety, which I will provide links to below.

<h3>APIs used:</h3>
<ul>
<li><a href=https://sheety.co/>Sheety</a>: This API helps you read and write into a google sheet, to use it simply read the documentation they provide to work with your google sheets in this code.</li><br />
<li><a href=https://developers.amadeus.com/>Amadeus</a>: This API searches for iataCodes, flight offers for this project, sign up to get your API Keys, and read their documentation.</li>
</ul>
