# 3DNS Market Metrics Api Calls

This is a flask app which makes several api calls to Opensea endpoints for listing and descriptive data for 3DNS tokenized domains.  This data is fed to the following data dashboard:https://flipsidecrypto.xyz/Brandyn/3dns-market-metrics-dashboard-h4tkYC  This needed to be done because Flipside does not natively support pagination in Data Studio.  This app paginates through the api calls and returns full results.  The endpoints are hosted via a Ngrok server.    
