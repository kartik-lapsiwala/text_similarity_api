# text_similarity_api
api to check the percentage of similarity between two texts

To run this api you need to install docker and docker compose on you machine.

after the docker and docker compose are installed type the following commands in the terminal.

>sudo docker-compose build

This command will install the required packages

>docker-compose up

This command will start the server on 0.0.0.0/5000

This api has 3 end points.

* register

* detect

* refill

### Register takes 2 arguments
  * username
  * password
  
### Detect takes 4 arguments
 * username
 * password
 * text1
 * text2
 
### Refill takes 3 arguments
 * username
 * password(which is admin password)
 * refill amount
