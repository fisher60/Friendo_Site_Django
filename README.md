# Friendo_Site
A website for managing Friendo bot and the Friendo API

### start docker
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up


# Notes Delete later
### it either decodes or it doesnt

validate_token: 
payload variable is vairable that raises errors (important), gets dict object from token and secret 

check if try catch is needed
if date is expired it should expire (test later) look at pip file
get rid of save token model. check if it makes sense to keep

rewrite AuthToken Class to be indepedent of Token class
no reference to user but on the user ie self.user.username should be self.username

encode_token is based on payload, check if dates expire. in settings.py look at jwt auth token delta

check if validate_token in AuthToken class is not needed
  static fucntion validate_token IS needed

mutations are post requests
get requests are queries
