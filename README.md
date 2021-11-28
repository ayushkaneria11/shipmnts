# Synopsis
This project consists of Graphql api endpoints that are created using Django and graphene. List of api endpoints are given at the end of the file. 
Some API endpoints need the authentication token which can be applied by registering user or using existing login details.

### Deployed on heroku -
[https://shipmnts-stackoverflow.herokuapp.com/](https://shipmnts-stackoverflow.herokuapp.com/)

### How to run project on local host -
- Clone the repository
`git clone https://github.com/ayushkaneria11/shipmnts.git`

- Install all the required library and dependencies
`pip install -r requirements.txt`

- To migrate database
`python manage.py makemigrations`
`python manage.py migrate`

- To run the project
`python manage.py runserver`


### API endpoints
- Access graphql: `/graphql/`

### Postman collection
- Collection can be downloaded from [here]()
