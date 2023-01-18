# Simple Blog API
Any  errors can be sent to me in telegram https://t.me/Gynshu 
Created according to "Test Task for Webtronics FastAPI candidate"
## Installation
<code>docker-compose up</code>
server runs at http://localhost:8000<br /><br />
You should use your own hanter.io  <b>EMAIL_VERIFICATION_KEY </b> in .env file<br /><br />
Or just comment this part of code at routs/auth.py <br/>
@router.post('/register'...
```   
else:
      if not tools.verify_email(payload.email):
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                              detail='Invalid email')
```
Stack:<br />
  Python <b>FastAPI</b><br />
  JWT<br />
  Oauth 2.0<br />
  <b>Redis</b> for user actions cache<br />
  MongoDb for user managment <br />
<br />
  Just noticed "Technology Requirements" for Db you requested relational DBs, sorry i have already made with Mongo, becouse its relatively new for me I wanted to try it)
    I like postgres more and I always use it<br />
  <br /><br />Swagger for documentation ( simplem <b>index.html and swagger.json</b>)<br />
Also postman collection for testing<br />
https://api.postman.com/collections/22312746-66ebe30b-f5f2-4d60-9343-8c69664cb003?access_key=PMAT-01GQ1SKHJN9550JNCWRWAGZGHE
