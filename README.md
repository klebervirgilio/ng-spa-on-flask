### Why Angular?

AngularJS is an open-source MVC JavaScript framework created at Google maintained by Google and the community. Angular features between the most popular Javascript frameworks for building rich web applications. The first version of the framework, also known as Angular.js,  was released in 2010, followed by Angular 2, Angular 4, 5, 6, and the latest Angular 7.  You might have noticed that the angular team decided to skip Angular 3, that’s actually an interesting fact I would like to encourage you to read the full history from the [angular.js blog]  (https://blog.angularjs.org/2016/12/ok-let-me-explain-its-going-to-be.html#Why_not_version_3_then_62)

From AngularJS and Angular 2, there were not just API breaking changes but also new concepts were introduced into the framework. The version 1 of the framework is written in JavaScript while from Angular 2 onwards are written in [TypeScript](https://www.typescriptlang.org/) - which is an open-source programming language developed and maintained by Microsoft. TypeScript is a superset of JavaScript that transcompiles to JavaScript. Like React.js, Vue.js and many others JavaScript frameworks, from Angular 2 onwards the concept of  `Controller`, largely used in AngularJS, was eliminated in favor of UI Components, which promoted flexibility and reusability as never seen in the first version of Angular. These changes alone made it impossible for AngularJS developers to upgrade their web applications and many cases, the web applications had to be re-written. 

But why Angular? Angular brings a lot of benefits to the table, it paves the way so developers can create rich Single-Page Applications. Even though it hasn’t been used frequently on versions newer than AngularJS. Two-way data-binding, the feature that made AngularJS famous, it’s one of the out-of-the functionalities that comes handy when data from the view needs to be injected in the component. TypeScript can also be considered as an advantage, of course, this isn’t directly an Angular benefit since you can pick TypeScript up to write any kind of JavaScript application, However, what I want to point out is working in large applications with JavaScript can get very messy due to the programming language weakly typed nature. Here’s where TypeScript comes to rescue offering more control and helping the developer to write more robust code-bases thanks to the compiler which catches silly errors in the early stages of the development.

## Create a REST API with Python

Python is a dynamic language widely adopted by companies and developers. The language states on its core values that software should simple, readable making developers more productive and happier. Check the [The Zen of Python] (https://www.python.org/dev/peps/pep-0020/ ) for more values.

In this tutorial you are going to use [Flask](http://flask.pocoo.org/) a microframework that will help you to quickly put together a REST API. 

Make sure you have Python 3 installed. Check the version of the installed python by running the following command:

```bash
python --version
```

Your REST API will use some third-party code (libraries) to help you for example to connect to a database, to create schemas for your models, and validate whether the incoming requests are authenticated or not. Python has a very powerful tool to manage dependencies called pyenv. To install pyenv on your machine you need to follow this steps: https://github.com/pyenv/pyenv#installation

With pyenv installed, go ahead and create a directory for your backend code:

```bash
mkdir kudos_oss && cd kudos_oss
```

Then, within the newly created directory run the following command:

```bash
pipenv --three
```

The command above will create a Python 3 virtual environment. Now you can install flask by running the following command:

```bash
pipenv install flask
```

Also, Python 3 provide nice features like `absolute_import` and  `print_function` that you will use in this tutorial. To import them run the following commands:

```bash
touch {__main__, __init__}.py
```

And copy and paste the following content in the `__main__.py` file:

```python
from __future__ import absolute_import, print_function
```

For this tutorial, your backend will need to implement the following user stories:

- As an authenticated user I want to favorite an github open source project
- As an authenticated user I want to unfavorite an github open source project
- As an authenticated user I want to list all bookmarked github open source projects I’ve previously favorited

A normal REST API will expose endpoints so clients can `create`, `update`, `delete`, `read` and `list all` resources. So, by end of this section your back-end application will be capable to handle the following HTTP calls:

```
# For the authenticated user, fetches all favorited github open source projects
GET /kudos

# Favorite a github open source project for the authenticated user
POST /kudos

# Unfavorite a favorited github open source project
DELETE /kudos/:id
```

### Define the Model Schemas

Your REST API will have 2 core schemas, they are `GithubRepoSchema` and `KudoSchema`. `GithubRepoSchema` will represent a Github repository sent by the clients whereas `KudoSchema` will represent the data you are going to persist in the database. 

Go ahead and run the following commands:

```
mkdir -p app/kudo
touch app/kudo/{schema, service, __init__}.py
```

The above commands will create the `app` directory with another directory within it called `kudo`  then, the second command will create three files: `schema.py`, `service.py`,  and `__init__.py`. 

Copy and paste the content below within the `schema.py` file.

```python
from marshmallow import Schema, fields

class GithubRepoSchema(Schema):
   repo_id = fields.Int(required=True)
   repo_name = fields.Str()
   language = fields.Str()
   description = fields.Str()
   repo_url = fields.URL()

class KudoSchema(GithubRepoSchema):
   user_id = fields.Email(required=True)
```

As you may have noticed, the schemas are inheriting from `Schema` a package from the [marshmallow  library] (https://marshmallow.readthedocs.io/en/3.0/), marshmallow is an ORM/ODM/framework-agnostic library for serializing/deserializing complex datatypes, such as objects, to and from native Python datatypes.

Install the `marshmallow` library running the following commands:

```bash
pipenv install marshmallow
```
### REST API Persistence with MongoDB

Great! You have now your first files in place. The schemas were created to represent the incoming request data as well as the data your application persists in the MongoDB. In order to connect and to execute queries against the database, you are going to use a library created and maintained by MongoDB itself called [pymonog](https://api.mongodb.com/python/current/).

Install the `pymongo` library running the following commands:

```bash
pipenv install pymongo
```

You can either [install MongoDB following these steps](https://docs.mongodb.com/manual/installation/) in our machine or you can use docker to spin up a MongoDB container. This tutorial assumes you have docker and docker-compose installed.

`docker-compose` will manage the MongoDB container for you. 

Create `docker-compose.yml` 

```
touch docker-compose.yml
```

And copy and paste the following content in it:

```
version: '3'
services:
  mongo:
    image: mongo
    restart: always
    ports:
     - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: mongo_user
      MONGO_INITDB_ROOT_PASSWORD: mongo_secret
````

All you have to do now to spin up a MongoDB container is:

```bash
docker-compose up
```

With MongoDB up and running you are ready to work the `MongoRepository` class, it is always a good idea to have class with just a single one responsibility, so the only point in your back-end application MongoDB is going to be explicitly dealt with is in the `MongoRepository`. 

Start by creating a directory where all persistence related files should sit, a suggestion would be: `repository`.

```bash
mkdir -p app/repository
```

Then, create the file that will hold the MongoRepository class:

```bash
touch -p app/repository/{mongo,__init__}.py
```

With `pymongo` properly installed and MongoDB up and runnnig, copy and paste the following content in the `app/repository/mongo.py` file.

```python
import os
from pymongo import MongoClient

COLLECTION_NAME = 'kudos'

class MongoRepository(object):
 def __init__(self):
   mongo_url = os.environ.get('MONGO_URL')
   self.db = MongoClient(mongo_url).kudos

 def find_all(self, selector):
   return self.db.kudos.find(selector)
 
 def find(self, selector):
   return self.db.kudos.find_one(selector)
 
 def create(self, kudo):
   return self.db.kudos.insert_one(kudo)

 def update(self, selector, kudo):
   return self.db.kudos.replace_one(selector, kudo).modified_count
 
 def delete(self, selector):
   return self.db.kudos.delete_one(selector).deleted_count
```

As you can see the `MongoRepository` class is very straightforward, it creates a database connection on its initialization then saves it to a instance variable to be use later by the methods: `find_all`, `find`, `create`, `update`,  and `delete`. Notice that all methods explicitly use the pymongo api. 

You might have noticed that the `MongoRepository` class reads a environment variable `MONGO_URL` . To export the environment variable, run:

```bash
export MONGO_URL=mongodb://mongo_user:mongo_secret@0.0.0.0:27017/
```

Since you might want to use other database in the future, it is a good idea to decouple your application from MongoDB. For the sake of simplicity you are going to create an abstract class to represent a `Repository`, this class should be the one used throughout your application.

Copy and paste the following content into the `app/repository/__init__.py` file:

```python
class Repository(object):
 def __init__(self, adapter=None):
   self.client = adapter()

 def find_all(self, selector):
   return self.client.find_all(selector)
 
 def find(self, selector):
   return self.client.find(selector)
 
 def create(self, kudo):
   return self.client.create(kudo)
  
 def update(self, selector, kudo):
   return self.client.update(selector, kudo)
  
 def delete(self, selector):
   return self.client.delete(selector)
```

You might recall the user stories that you’re working on are: A authenticated user should able to create, delete and list all favorited Github open-source projects. In order to get that done those `MongoRepository`’s methods will come handy.

You will soon implement the endpoints of your REST API. First, you need to create a service class that knows how to translate the incoming request payload to our representation `KudoSchema` defined in the `app/kudo/schema.py`. The difference between the incoming request payload, represented by `GithubSchema`, and the object you persist in the database, represented by `KudoSchema` is: The first has an `user_Id` which determines who owns the object. 

Copy the content below to the `app/kudo/service.py` file:

```python
from ..repository import Repository
from ..repository.mongo import MongoRepository
from .schema import KudoSchema

class Service(object):
 def __init__(self, user_id, repo_client=Repository(adapter=MongoRepository)):
   self.repo_client = repo_client
   self.user_id = user_id

   if not user_id:
     raise Exception("user id not provided")

 def find_all_kudos(self):
   kudos  = self.repo_client.find_all({'user_id': self.user_id})
   return [self.dump(kudo) for kudo in kudos]

 def find_kudo(self, repo_id):
   kudo = self.repo_client.find({'user_id': self.user_id, 'repo_id': repo_id})
   return self.dump(kudo)

 def create_kudo_for(self, githubRepo):
   self.repo_client.create(self.prepare_kudo(githubRepo))
   return self.dump(githubRepo.data)

 def update_kudo_with(self, repo_id, githubRepo):
   records_affected = self.repo_client.update({'user_id': self.user_id, 'repo_id': repo_id}, self.prepare_kudo(githubRepo))
   return records_affected > 0

 def delete_kudo_for(self, repo_id):
   records_affected = self.repo_client.delete({'user_id': self.user_id, 'repo_id': repo_id})
   return records_affected > 0

 def dump(self, data):
   return KudoSchema(exclude=['_id']).dump(data).data

 def prepare_kudo(self, githubRepo):
   data = githubRepo.data
   data['user_id'] = self.user_id
   return data
```

Notice that our constructor `__init__` receives as parameters the `user_id` and the `repo_client` which are used in all operations in this service. That’s the beauty of having a class to represent a repository, As far as the service is concerned, it does not care if the `repo_client` is persisting the data in a MongoDB, PostgreSQL or sending the data over the network to a third party service API, all it needs to know is, the `repo_client` is a `Repository` instance that was configured with an adapter that implements methods like `create`, `delete` and `find_all`. 
### Define Your REST API Middlewares

At this point, you’ve covered 70% of the back-end. You are ready to implement the HTTP endpoints and the JWT middleware which will secure you REST API against unauthenticated requests.

You can start by creating a directory where HTTP related files should be placed.

```bash
mkdir -p app/http/api
```

Within this directory, you will have basically 2 files, `endpoints.py` and `middlewares.py`. To create them run the following commands:

```bash
touch app/http/api/{__init__,endpoints,middlewares}.py
```

The requests made to your REST API are JWT authenticated, which means you need to make sure that every single request carries a valid [json web token](https://stormpath.com/blog/beginners-guide-jwts-in-java). [`pyjwt`](https://pyjwt.readthedocs.io/en/latest/) will take care of the validation for us. To install it run the following command:

```bash
pyenv install pyjwt
```

Now that know the role of the JWT middleware, you need to write it. Copy and paste the following content to the `middlewares.py` file.

```python
from functools import wraps
from flask import request, g, abort
from jwt import decode, exceptions
import json

def login_required(f):
   @wraps(f)
   def wrap(*args, **kwargs):
       authorization = request.headers.get("authorization", None)
       if not authorization:
           return json.dumps({'error': 'no authorization token provied'}), 403, {'Content-type': 'application/json'}
      
       try:
           token = authorization.split(' ')[1]
           resp = decode(token, None, verify=False, algorithms=['HS256'])
           g.user = resp['sub']
       except exceptions.DecodeError as identifier:
           return json.dumps({'error': 'invalid authorization token'}), 403, {'Content-type': 'application/json'}
      
       return f(*args, **kwargs)
 
   return wrap
```

Flask provide a module called `g` which is basically a global context shared across the request life cycle. This middleware is checking whether or not the request is valid, if so, the middleware will extract the authenticated user details and persist it in the global context. 

### Define Your REST API endpoints

The HTTP handlers should be easy now, since you have already done the important pieces, it’s just a matter of putting everything together. 

Since your end goal is to create a JavaScript application that will run on web browsers, you need to make sure that web browsers are happy when a preflight is performed, you can learn more about it [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS). In order to implement CORS our your REST API, you are going to install [`flask_cors`](https://flask-cors.readthedocs.io/en/latest/)

```bash
pipenv install flask_cors
```

Next, implement your endpoints. Go ahead and copy and paste the content above into the `app/http/api/endpoints.py` file.

```
from .middlewares import login_required
from flask import Flask, json, g, request
from app.kudo.service import Service as Kudo
from app.kudo.schema import GithubRepoSchema
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/kudos", methods=["GET"])
@login_required
def index():
 return json_response(Kudo(g.user).find_all_kudos())


@app.route("/kudos", methods=["POST"])
@login_required
def create():
   github_repo = GithubRepoSchema().load(json.loads(request.data))
  
   if github_repo.errors:
     return json_response({'error': github_repo.errors}, 422)

   kudo = Kudo(g.user).create_kudo_for(github_repo)
   return json_response(kudo)


@app.route("/kudo/<int:repo_id>", methods=["GET"])
@login_required
def show(repo_id):
 kudo = Kudo(g.user).find_kudo(repo_id)

 if kudo:
   return json_response(kudo)
 else:
   return json_response({'error': 'kudo not found'}, 404)


@app.route("/kudo/<int:repo_id>", methods=["PUT"])
@login_required
def update(repo_id):
   github_repo = GithubRepoSchema().load(json.loads(request.data))
  
   if github_repo.errors:
     return json_response({'error': github_repo.errors}, 422)

   kudo_service = Kudo(g.user)
   if kudo_service.update_kudo_with(repo_id, github_repo):
     return json_response(github_repo.data)
   else:
     return json_response({'error': 'kudo not found'}, 404)

  
@app.route("/kudo/<int:repo_id>", methods=["DELETE"])
@login_required
def delete(repo_id):
 kudo_service = Kudo(g.user)
 if kudo_service.delete_kudo_for(repo_id):
   return json_response({})
 else:
   return json_response({'error': 'kudo not found'}, 404)


def json_response(payload, status=200):
 return (json.dumps(payload), status, {'content-type': 'application/json'})
```

Brilliant! It’s all in place now! You should be able to run the REST API with the command below:

```bash
FLASK_APP=$PWD/app/http/api/endpoints.py FLASK_ENV=development pipenv run python -m flask run --port 4433
```
## Create Angular Client-Side App
### Angular App Boilerplate

To create your Angular Client-Side App, you will use Angulas’s awesome [`ng-cli`](https://cli.angular.io/) tool to bypass all the JavaScript build process setup hassle.

Installing [`ng-cli`](https://cli.angular.io)  is quite simple. In this tutorial you will use [`npm`](https://www.npmjs.com/get-npm) make sure you either have it installed or use the dependency manager of your preference.

To install `ng-cli`, run the command above. For more install options check this angular quickstart https://angular.io/guide/quickstart#install-cli out.

```bash
npm install -g @angular/cli
```

Navigate to the `app/http` directory and use `ng-cli` to create a Angular application:

```bash
cd app/http
ng new web-app
```

Angular CLI will prompt two questions before creating all the files you need to start coding your front-end application. The first question is whether you want routing or not, you can type `y` to let the Angular CLI setup your application with routing enabled and the last question is which CSS flavour you will want, for this tutorial pick SCSS. 



Once Angular CLI finishes creating the files, you can now navigate to the newly created directory and spin up a web server.

```bash
cd web-app
ng serve --open --port 3000
```

Running `ng server --open` will start a web server listening to the port 3000. Open this url in your browser: `http://localhost:3000/` Your browser should load an Angular app and render the AppComponent created automatically by `ng-cli`. 


Your goal now is to use [Material Design](https://material.io/design/) to create a simple and beautiful UI. Thankfully, the Angular has a very mature library to help you in this journey,the awesome https://material.angular.io/ which basically are the [Material Design](https://material.io/design/) concepts translated into Angular components.

Run the following command to install what you will need from [Material Design](https://material.io/design/).

```bash
npm install --save @angular/material @angular/cdk @angular/animations
```

Great, now you have components like: MatToolbarModule, MatButtonModule, MatIconModule, MatCardModule, MatTabsModule, MatGridListModule e many more ready to be imported and used. You will use them soon. Let’s talk about protected routes.

### Add Authentication to Your Angular App with Okta

Writing secure user auth and building login pages are easy to get wrong and can be the downfall of a new project. Okta makes it simple to implement all the user management functionality quickly and securely. Get started by signing up for a [free developer account](https://developer.okta.com/signup/) and creating an OIDC application in Okta.



Once logged in, create a new application by clicking “Add Application”.



Select the “Single-Page App” platform option.



The default application settings should be the same as those pictured.



Great! With your token OIDC application in place, you can now move forward and secure the routes that requires authentication.
### Create your Routes.

[@angular/router](https://angular.io/guide/router) is library for routing URL to Angular components. 

Your Angular application will have two routes:

`/`  The root route does not require the user to be logged in, it actually is the landing page of your application. An user should be able to access this page in order to log in. You will use [Okta Angular SDK](https://developer.okta.com/code/angular) to integrate your routes with Okta's OpenID Connect API.

`/home` The Home route will render most of the components you application will have. It should implement the following user stories.

 An Authenticated User should be able to search through the Github API the open source projects of his/her preferences
An Authenticated User should be able to favorite an open source project that pleases him/her.
An Authenticated User should be able to see in different tabs his/her previous favorited open source projects and the search results.

To Install [`@okta/okta-angular`](https://www.npmjs.com/package/@okta/okta-angular) run the command:

```bash
npm install --save @okta/okta-angular
```

Now go ahead and copy and paste the following content into the `app-routing.module.ts` file.

```typescript
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';

import { OktaAuthModule, OktaCallbackComponent, OktaAuthGuard } from '@okta/okta-angular';

const routes: Routes = [
 { path: '', component: LoginComponent },
 {
   path: 'home',
   component: HomeComponent,
   canActivate: [OktaAuthGuard],
 },
 { path: 'implicit/callback', component: OktaCallbackComponent },
];

@NgModule({
 imports: [
   RouterModule.forRoot(routes),
   OktaAuthModule.initAuth({
     issuer: {ADD_YOUR_DOMAIN},
     clientId: {ADD_YOUR_CLIENT_ID},
     redirectUri: 'http://localhost:3000/implicit/callback',
     scope: 'openid profile email'
   })
 ],
 exports: [RouterModule]
})
export class AppRoutingModule { }
```

Disconsider for a minute the `Loign` and `Home` components being imported. You will work on them pretty soon. Focus in the `OktaAuthModule`, `OktaCallbackComponent`, and `OktaAuthGuard` components.

To guard a route with authentication anywhere in the application, you need to configure the route with `canActivate: [OktaAuthGuard]` component provided by Okta.

`OktaCallbackComponent` component is the route/URI destination to where the user will be redirected after Okta finishes the sign in process, whereas `OktaAuthModule` will inject a service which exposes useful methods to access the authenticated user.

Your are now ready to create the Login component, as mentioned previously, this component will be accessible all users (not only authenticated users), the main goal of the Login component is to authenticate the user.

Angular CLI has a verify useful generator to speed up components creation, within the directory `app/htpp/web-app`, run the command bellow:

```bash
ng generate component login
```



`ng generate component` will not just create the component files, it will also configure your Angular application to properly inject the newly created component.

Go ahead and copy and paste the following content into the `src/app/login/login.component.ts` file:

```typescript
import { Component, OnInit } from '@angular/core';
import { OktaAuthService } from '@okta/okta-angular';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  constructor(private oktaAuth: OktaAuthService, private router: Router) {
  }

  async ngOnInit() {
    const isAuthenticated = await this.oktaAuth.isAuthenticated();
    if (isAuthenticated) {
      this.router.navigate(['/home'], {replaceUrl: true})
    }
  }

  async login(event) {
    event.preventDefault();
    await this.oktaAuth.loginRedirect('/home');
  }
}
```

Then copy and paste the following content into the `src/app/login/login.component.html` file:

```typescript
<mat-card>
  <mat-card-content>
    <button mat-button (click)="login($event)" color="primary">Login</button>
  </mat-card-content>
</mat-card>
```

Here’s how the login process will work:

The user navigates to the landing page.


In the Login component you are using the [Okta Angular SDK](https://developer.okta.com/code/angular) to check whether the user has already signed in or not In case the user has already signed in, the user should be redirected to the `/home` route, otherwise he/she could click in the `Login` button to then be redirect to Okta, authenticate and be redirected the the home page. As shown in the image below.



You will work in the Home component soon. But after the sign in process finishes in the Okta end, here’s the page the user should see:


The Home is the main component of your application. It needs to list all favorited open source projects as well as the Github search results which is done using Tabs. 

Here’s how it works:

When the Home component is rendered, you should make a HTTP call to your Python REST API to get all the user’s favorites open-source repositories. `@angular/core` provides a module `OnInit` that a component can implement in order to have the `ngOnInit` method fired whenever the component is rendered. You will use `ngOnInit` to make the HTTP call to your Python REST API.

 



Users can type keywords in the text input on the top of the screen. The method `onSearch` will be called on the `keyPress` event of the input. Whenever the user types `Return/Enter` the method will perform a query against Github API.

Once Github responds with the list open-source repositories, you are going to render all the repositories in the “SEARCH” tab. Then the user can favorite any of the repositories. Favoriting a repository will make a HTTP call to the your REST API persisting it to the database.




Home component also takes care logging the user out When the user clicks in the `Logout` button, all data related to his/her session will be wiped out and the user will be redirected to the landing page.



`/home` is a authenticated route, So if the user tries to access it without authenticating first him/her should be redirected to Okta’s login page.






Copy and paste the following content into the `src/app/home/home.component.ts`.

```typescript
import { Component, OnInit } from '@angular/core';
import { OktaAuthService } from '@okta/okta-angular';
import { GithubClientService } from '../github-client.service';
import { ApiClientService } from '../api-client.service';

@Component({
 selector: 'app-home',
 templateUrl: './home.component.html',
 styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

 selectedTab: Number
 repos: Array<Object>
 kudos: Array<Object>

 constructor(
   private oktaAuth: OktaAuthService,
   private githubClient: GithubClientService,
   private apiClient: ApiClientService
 ) {
   this.selectedTab = 0;
   this.repos = [];
   this.kudos = [];
 }

 async ngOnInit() {
   this.apiClient.getKudos().then( (kudos) => {
     this.kudos = kudos;
   } )
 }

 async logout(event) {
   event.preventDefault();
   await this.oktaAuth.logout('/');
 }

 onSearch = (event) => {
   const target = event.target;
   if (!target.value || target.length < 3) { return }
   if (event.which !== 13) { return }

   this.githubClient
     .getJSONRepos(target.value)
     .then((response) => {
       target.blur();
       this.selectedTab = 1;
       this.repos = response.items;
     })
 }

 onKudo(event, repo) {
   event.preventDefault();
   this.updateBackend(repo);
 }

 updateState(repo) {
   if (this.isKudo(repo)) {
     this.kudos = this.kudos.filter( r => r['id'] !== repo.id )
   } else {
     this.kudos = [repo, ...this.kudos]
   }
 }

 isKudo(repo) {
   return this.kudos.find( r => r['id'] == repo.id );
 }

 updateBackend = (repo) => {
   if (this.isKudo(repo)) {
     this.apiClient.deleteKudo(repo);
   } else {
     this.apiClient.createKudo(repo);
   }
   this.updateState(repo);
 }
}
```

Then Copy and paste the following content into the `src/app/home/home.component.html`.

```html
<mat-toolbar color="primary">
 <input matInput (keyup)="onSearch($event)" placeholder="Search for your OOS project on Github + Press Enter">
 <button mat-button (click)="logout($event)">LOGOUT</button>
</mat-toolbar>

<mat-tab-group mat-align-tabs="center" [selectedIndex]="selectedTab" dynamicHeight>
   <mat-tab label="KUDO">
     <mat-grid-list cols="4">
         <mat-grid-tile *ngFor="let repo of kudos" rowHeight='200px' >
             <mat-card class="card">
               <mat-card-header class="title">
                 <mat-card-title>{{repo.name}}</mat-card-title>
               </mat-card-header>
               <mat-card-content>
                 {{repo.description}}
               </mat-card-content>
               <mat-card-actions>
                 <button mat-icon-button [color]="isKudo(repo) ? 'accent' : 'primary'" (click)="onKudo($event, repo)">
                   <mat-icon >favorite</mat-icon>
                 </button>
               </mat-card-actions>
             </mat-card>
         </mat-grid-tile>
     </mat-grid-list>
   </mat-tab>
   <mat-tab label="SEARCH">
     <mat-grid-list cols="4">
         <mat-grid-tile *ngFor="let repo of repos" rowHeight='200px' >
             <mat-card class="card">
               <mat-card-header class="title">
                 <mat-card-title>{{repo.name}}</mat-card-title>
               </mat-card-header>
               <mat-card-content>
                 {{repo.description}}
               </mat-card-content>
               <mat-card-actions>
                 <button mat-icon-button [color]="isKudo(repo) ? 'accent' : 'primary'" (click)="onKudo($event, repo)">
                   <mat-icon >favorite</mat-icon>
                 </button>
               </mat-card-actions>
             </mat-card>
         </mat-grid-tile>
     </mat-grid-list>
   </mat-tab>
</mat-tab-group>
```

Great, you will need to make HTTP calls to your Python REST API as well as to the Github REST API. The Github HTTP client will need to have a function to make a request to this URL: `https://api.github.com/search/repositories?q=USER-QUERY`. You are going to use the `q` query string to pass the term the user wants to query against Github’s repositories. 

Angular CLI offers a nice generator for services. To create a github client run the following command:

```bash
ng generate service gbClient
```



Then, copy and paste the following content into the `src/app/gb-client.service.ts` file.

```typescript
import { Injectable } from '@angular/core';

@Injectable({
 providedIn: 'root'
})
export class GithubClientService {

 constructor() { }

 getJSONRepos(query) {
   return fetch('https://api.github.com/search/repositories?q=' + query).then(response => response.json());
 }

 getJSONRepo(id) {
   return fetch('https://api.github.com/repositories/' + id).then(response => response.json())
 }
}
```

Now, you need to create a HTTP client to make HTTP calls to the Python REST API you’ve just implemented in the first section of this tutorial. Since all the requests made to your Python REST API requires the user to be authenticated, you will need to set the `Authorization` HTTP Header with the `acessToken` provided by Okta.

```bash
ng generate service apiClient
```

Then, copy and paste the following content into the `src/app/api-client.service.ts` file.

```typescript
import { Injectable } from '@angular/core';
import { OktaAuthService } from '@okta/okta-angular';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
 providedIn: 'root'
})
export class ApiClientService {
 constructor(private oktaAuth: OktaAuthService, private http: HttpClient) {
 }

 createKudo(repo) {
   return this.perform('post', '/kudos', repo);
 }

 deleteKudo(repo) {
   return this.perform('delete', `/kudo/${repo.id}`);
 }

 updateKudo(repo) {
   return this.perform('put', `/kudos/${repo.id}`, repo);
 }

 getKudos() {
   return this.perform('get', '/kudos');
 }

 getKudo(repo) {
   return this.perform('get', `/kudo/${repo.id}`);
 }

 async perform (method, resource, data = {}) {
   const accessToken = await this.oktaAuth.getAccessToken();
   const url = `http://localhost:4433${resource}`;

   const httpOptions = {
     headers: new HttpHeaders({
       'Content-Type':  'application/json',
       'Authorization': `Bearer ${accessToken}`
     })
   };

   switch (method) {
     case 'delete':
       return this.http.delete(url, httpOptions).toPromise()
     case 'get':
       return this.http.get(url, httpOptions).toPromise()
     default:
       return this.http[method](url, data, httpOptions).toPromise()
   }
 }
}
```

Lastly, you will need to make sure your angular application is properly importing all modules, in order to do so make sure your `src/app/app.module.ts` file looks like this:

```typescript
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';


import {
 MatToolbarModule,
 MatButtonModule,
 MatIconModule,
 MatCardModule,
 MatTabsModule,
 MatGridListModule
} from '@angular/material';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
@NgModule({
 declarations: [
   AppComponent,
   LoginComponent,
   HomeComponent
 ],
 imports: [
   BrowserModule,
   BrowserAnimationsModule,
   AppRoutingModule,
   HttpClientModule,
   MatToolbarModule,
   MatButtonModule,
   MatIconModule,
   MatCardModule,
   MatTabsModule,
   MatGridListModule
 ],
 providers: [],
 bootstrap: [AppComponent]
})
export class AppModule { }
```

Now you can run  both frontend and backend together to see the final result:

To start the Python REST API run:

```bash
cd kudos_oss &&
FLASK_APP=$PWD/app/http/api/endpoints.py FLASK_ENV=development pipenv run python -m flask run --port 4433
```

Then start the Angular application:

```bash
cd app/http/web-app && ng serve --open --port 3000
```

As you might have noticed, your Python REST API is listening to the port 4433 while the Angular application is being served by a process on the 3000 port. All you need to do is to open this URL http://localhost:3000 in your browser.

Learn more About Angular, Python, and Flask

In this tutorial, I have guided you through the development of a single page web application using Angular and Python. Using just a few lines of code you were able to implement user authentication for the client and the server. Angular makes use of TypeScript which is a superset of the JavaScript language and adds type information. 

If you’re ready to learn more about Angular we have some other resources for you to check out:

Angular 6 - What’s New and Why Upgrade?
Build a Basic CRUD App with Angular 7 and Spring Boot

And as always, we’d love to have you follow us for more cool content and updates from our team. You can find us on Twitter @oktadev, on Facebook, and LinkedIn.

