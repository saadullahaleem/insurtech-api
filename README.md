## How to start
Simply run `make setup` to setup and run the server. You can use `make shell` to start an instance of the django shell.

The documentation can be viewed at either `/api/schema/swagger-ui/` or `api/schema/redoc/`. Swagger can be used to try 
out the APIs. The Swagger UI provides extensive support for making API calls to available endpoints. It also lets you 
view the Schemas within the backend. This is achieved via the [Django Spectacular](https://drf-spectacular.readthedocs.io/en/latest/) 
library that auto generates an OpenAPI spec for the backend and provides functionality to render both Redoc and Swagger 
UIs.

## User Types
Both Customers and Admin users are handled via the same `User` model. This model extends the builtin Django `User` model.
This gives us the advantage to rely on Django's extensive support for authentication, authorization, and permissions 
management. It also lets us use third-party modules easily. If it were a hard requirement to have different models for 
different types of users, we would be better off bypassing the Django User system entirely.

### Customer
These can be created via the `/customers` endpoint. There is also a custom action `/set_password` to update a user's 
password.

## Filtering and Searching
Available parameters are documented and can be viewed against the endpoints using the Swagger UI.

## Authentication

This backend uses JWT authentication powered by the [Django Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
package. It uses access and refresh tokens. The default access token lifetime is set to 60 minutes.