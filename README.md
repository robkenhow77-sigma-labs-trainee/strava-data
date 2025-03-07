Getting Strava data:

1. create an api account
2. go to https://www.strava.com/oauth/authorize?client_id=CLIENT_ID&redirect_uri=http://localhost&response_type=code&scope=activity:read_all and authorize
3. copy code from url "code=..."
4. make a post request to https://www.strava.com/oauth/token?client_id=CLIENT_ID&client_secret=CIENT_SECRET&code=CODE&grant_type=authorization_code, this gives you a new access token
5. Use this access token for read all access

FOR THE WEBSITE:
1. redirect user to strava login
2. get them to login
3. redirect to authentication page (step 2 above)

THE client_id and client secret are unique to the app provider not the user, only the CODE is unique to the user.