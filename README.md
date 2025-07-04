# My E-commerce REST API

This is a RESTful API for an e-commerce platform built with Django and Django REST Framework. It provides functionalities for user authentication, product and category management, a shopping cart, and order processing.

## Project Structure

'''
my_ecommerce_api_project/
├── my_ecommerce_api/          # Main Django project directory
│   ├── manage.py              # Django's command-line utility
│   ├── my_ecommerce_api/      # Project's core settings
│   │   ├── init.py
│   │   ├── asgi.py
│   │   ├── settings.py        # Project settings (Database, INSTALLED_APPS, etc.)
│   │   ├── urls.py            # Main URL configurations (includes app-specific URLs)
│   │   └── wsgi.py
│   ├── accounts/              # User authentication and custom user model app
│   │   ├── migrations/
│   │   ├── init.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py          # Custom User Model
│   │   ├── serializers.py     # User serializers (for Djoser)
│   │   ├── urls.py            # Djoser authentication URLs
│   │   └── views.py
│   ├── products/              # Product and category management app
│   │   ├── migrations/
│   │   ├── init.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py          # Category and Product models
│   │   ├── serializers.py     # Category and Product serializers
│   │   ├── urls.py            # Product and Category API routes
│   │   └── views.py           # ViewSets for Products and Categories
│   ├── cart/                  # Shopping cart app
│   │   ├── migrations/
│   │   ├── init.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py          # Cart and CartItem models
│   │   ├── serializers.py     # Cart and CartItem serializers
│   │   ├── urls.py            # Cart API routes
│   │   └── views.py           # ViewSets for Cart and CartItem
│   ├── orders/                # Order processing app
│   │   ├── migrations/
│   │   ├── init.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py          # Order and OrderItem models
│   │   ├── serializers.py     # Order and OrderItem serializers
│   │   ├── urls.py            # Order API routes
│   │   └── views.py           # ViewSet for Orders
│   └── media/                 # Directory for user-uploaded files (e.g., product images)
└── venv/                      # Python Virtual Environment

'''
## API Routes (Endpoints)

All API endpoints are prefixed with `/api/`. The base URL for the API is `http://127.0.0.1:8000/api/`.

### 1. Authentication & User Management (Accounts App)

These endpoints are handled by Djoser and included under the `/api/auth/` prefix.

| Method | Endpoint                    | Description                                       | Authentication Required |
| ------ | --------------------------- | ------------------------------------------------- | ----------------------- |
| `POST` | `/api/auth/users/`          | Register a new user                               | None                    |
| `POST` | `/api/auth/token/login/`    | Log in and get an authentication token            | None                    |
| `POST` | `/api/auth/token/logout/`   | Log out (invalidates current token)               | Token                   |
| `GET`  | `/api/auth/users/me/`       | Retrieve details of the currently logged-in user  | Token                   |
| `PUT`  | `/api/auth/users/me/`       | Update details of the currently logged-in user    | Token                   |
| `PATCH`| `/api/auth/users/me/`       | Partially update details of the current user      | Token                   |
| `POST` | `/api/auth/users/set_password/` | Change password for the logged-in user        | Token                   |
| `POST` | `/api/auth/users/reset_password/` | Request a password reset email                | None                    |
| `POST` | `/api/auth/users/reset_password_confirm/` | Confirm password reset with token             | None                    |
| `POST` | `/api/auth/users/activation/` | Activate user account via UID/token (if enabled)  | None                    |
| `GET`  | `/api/auth/users/{id}/`     | Retrieve a specific user by ID (if permitted)   | Token (Admin/Staff)     |
| `DELETE`| `/api/auth/users/me/`      | Delete the currently logged-in user's account     | Token                   |

### 2. Product Management (Products App)

These endpoints are included under the `/api/` prefix.

#### Categories

| Method | Endpoint                        | Description                                        | Authentication Required | Permissions       |
| ------ | ------------------------------- | -------------------------------------------------- | ----------------------- | ----------------- |
| `GET`  | `/api/categories/`              | Retrieve a list of all product categories          | None                    | Any               |
| `POST` | `/api/categories/`              | Create a new product category                      | Token                   | Admin/Staff       |
| `GET`  | `/api/categories/{id}/`         | Retrieve details of a specific category            | None                    | Any               |
| `PUT`  | `/api/categories/{id}/`         | Update details of a specific category              | Token                   | Admin/Staff       |
| `PATCH`| `/api/categories/{id}/`         | Partially update details of a specific category    | Token                   | Admin/Staff       |
| `DELETE`|`/api/categories/{id}/`         | Delete a specific category                         | Token                   | Admin/Staff       |

#### Products

| Method | Endpoint                        | Description                                        | Authentication Required | Permissions       |
| ------ | ------------------------------- | -------------------------------------------------- | ----------------------- | ----------------- |
| `GET`  | `/api/products/`                | Retrieve a list of all products                    | None                    | Any               |
| `POST` | `/api/products/`                | Create a new product                               | Token                   | Admin/Staff       |
| `GET`  | `/api/products/{id}/`           | Retrieve details of a specific product             | None                    | Any               |
| `PUT`  | `/api/products/{id}/`           | Update details of a specific product               | Token                   | Admin/Staff       |
| `PATCH`| `/api/products/{id}/`           | Partially update details of a specific product     | Token                   | Admin/Staff       |
| `DELETE`|`/api/products/{id}/`           | Delete a specific product                          | Token                   | Admin/Staff       |

### 3. Shopping Cart (Cart App)

These endpoints are included under the `/api/` prefix.

| Method | Endpoint                        | Description                                        | Authentication Required |
| ------ | ------------------------------- | -------------------------------------------------- | ----------------------- |
| `GET`  | `/api/my-cart/`                 | Retrieve or create the current user's shopping cart| Token                   |
| `POST` | `/api/cart-items/`              | Add an item to the current user's cart (or update quantity if exists) | Token |
| `GET`  | `/api/cart-items/{id}/`         | Retrieve a specific cart item                      | Token                   |
| `PUT`  | `/api/cart-items/{id}/`         | Update a specific cart item                        | Token                   |
| `PATCH`| `/api/cart-items/{id}/`         | Partially update a specific cart item              | Token                   |
| `DELETE`|`/api/cart-items/{id}/`         | Remove a specific item from the cart               | Token                   |

### 4. Order Processing (Orders App)

These endpoints are included under the `/api/` prefix.

| Method | Endpoint                            | Description                                           | Authentication Required |
| ------ | ----------------------------------- | ----------------------------------------------------- | ----------------------- |
| `POST` | `/api/orders/create-from-cart/`     | Create a new order from the user's current cart       | Token                   |
| `GET`  | `/api/orders/`                      | Retrieve a list of all orders for the current user    | Token                   |
| `GET`  | `/api/orders/{id}/`                 | Retrieve details of a specific order                  | Token                   |
| `POST` | `/api/orders/{id}/mark-as-paid/`    | Mark a specific order's payment status as 'paid'      | Token                   |
| `PUT`  | `/api/orders/{id}/`                 | Update a specific order (e.g., status, shipping address) | Token (Admin/Staff)  |
| `PATCH`| `/api/orders/{id}/`                 | Partially update a specific order                     | Token (Admin/Staff)  |
| `DELETE`|`/api/orders/{id}/`                 | Delete a specific order                               | Token (Admin/Staff)  |

## How to Run the Project

1.  **Clone the repository:**
    ```bash
    git clone <repository_url_here>
    cd my_ecommerce_api_project/my_ecommerce_api
    ```
2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```
3.  **Activate the virtual environment:**
    * **Windows:** `.\venv\Scripts\activate`
    * **macOS/Linux:** `source venv/bin/activate`
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *If you don't have a `requirements.txt` file, create one in your `my_ecommerce_api` directory with the following content, then run `pip install -r requirements.txt`:*
    ```
    Django>=4.0
    djangorestframework
    djoser
    django-cors-headers
    Pillow # For image fields
    django-imagekit # If you are using this for image processing
    ```
5.  **Apply migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
6.  **Create a Superuser (for Admin Panel access):**
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to set up your admin username, email, and password.

7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The API will be accessible at `http://127.0.0.1:8000/`.

## Testing the API

You can test the API endpoints using tools like [Postman](https://www.postman.com/downloads/) or `cURL`.

**Key points for testing with Postman:**

* Always set `Content-Type: application/json` in your request headers for `POST`/`PUT`/`PATCH` requests with JSON bodies.
* For authenticated requests, include the `Authorization` header with your token:
    `Authorization: Token <your_auth_token_here>`
    (Remember the `Token ` prefix followed by a space).
* Ensure URLs end with a trailing slash (`/`) for `POST` requests to avoid `RuntimeError` due to `APPEND_SLASH=True` (Django's default).
