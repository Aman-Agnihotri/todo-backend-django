# Django Todo App Documentation

This project is a simple Todo application implemented with Django, providing a fully-featured backend that includes user authentication (token-based), CRUD operations on todos, filtering, searching, and an admin interface.

---

## Project Structure

```
.
├── db.sqlite3
├── manage.py
├── todo_app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── todo_backend
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── ...
```

---

## Major Components

### `todo_app/models.py`

• Defines the **Todo** model with the following fields:

- title (CharField)  
- description (TextField, optional)  
- completed (BooleanField, defaults to False)  
- created_at (DateTimeField, auto_now_add=True)  
- updated_at (DateTimeField, auto_now=True)  
- due_date (DateTimeField, optional)  
- priority (IntegerField, choices=Low, Medium, High)  
- user (ForeignKey to Django’s User model)

### `todo_app/serializers.py`

• Contains two serializers:  

1. **UserSerializer**  
   - Serializes/deserializes data for Django’s User model  
   - Includes handling for password creation  
2. **TodoSerializer**  
   - Serializes/deserializes todos  
   - Adds a custom status field (completed, overdue, or pending)

### `todo_app/views.py`

• Provides the REST API view logic:

1. **TodoViewSet**  
   - Inherits from DRF’s ModelViewSet  
   - Implements CRUD operations for todos  
   - Filters by user, status (pending, completed, overdue), and supports searching/ordering  
   - Custom endpoints:
     - GET `/statistics/` → Statistics of all todos for that user  
     - DELETE `/clear_completed/` → Bulk delete of completed todos  

2. **register_user**  
   - POST `/register/`  
   - Creates a new user account  
   - Generates and returns a token  

3. **login_user**  
   - POST `/login/`  
   - Authenticates user credentials  
   - Returns a token for subsequent requests  

### `todo_app/urls.py`

• Routes API endpoints:

- `/todos/` → All TodoViewSet operations  
- `/register/` → register_user  
- `/login/` → login_user  

### `todo_backend/settings.py`

• Django settings, including:  

- Installed apps (DRF, CORS, `todo_app`, etc.)  
- SQLite database configuration  
- Token authentication (via `rest_framework.authtoken`)  
- Default permission set to `IsAuthenticated` (token required)

### `todo_backend/urls.py`

• Defines global URLs:  

- `/admin/` → Django’s admin site  
- `/api/` → Routes from `todo_app/urls.py`

### `todo_app/admin.py`

• Registers the Todo model in Django admin:  

- Custom list display, filters, search  
- Fieldsets for logical grouping  
- User isolation for non-superusers

### `todo_app/tests.py`

• Test suite covering:  

- User registration and login  
- CRUD on todos  
- Status calculations (pending, completed, overdue)  
- Statistics endpoint (`/todos/statistics/`)  
- Clear completed endpoint (`/todos/clear_completed/`)  
- User isolation checks  

---

## Installation & Setup

1. Install packages:

```bash
   pip install -r requirements.txt
```

2. Apply migrations

```bash
   python manage.py makemigrations
   python manage.py migrate
```

3. Create a superuser:

```bash
   python manage.py createsuperuser
```

4. Run the development server:

```bash
   python manage.py runserver
```

5. Access Django admin at:
[localhost:8000/admin](http://127.0.0.1:8000/admin/)
(Use superuser credentials)

---

## API Usage

1. **Register a User**  
   POST `/api/register/`

   ```json
   {
     "username": "newuser",
     "password": "newpass123",
     "email": "new@example.com"
   }
   ```

   Returns a token, user_id, and username.

2. **Log In**  
   POST `/api/login/`  

   ```json
   {
     "username": "newuser",
     "password": "newpass123"
   }
   ```

   Returns a token, user_id, and username.

3. **Authenticated Requests**  
   Include the header:

   ```
   Authorization: Token <your_token>
   ```

4. **Todo Operations**  
   - GET `/api/todos/`  
     List all todos for the authenticated user  
   - POST `/api/todos/`  
     Create a new todo  
   - GET `/api/todos/{id}/`  
     Retrieve a specific todo  
   - PATCH/PUT `/api/todos/{id}/`  
     Update a specific todo  
   - DELETE `/api/todos/{id}/`  
     Delete a specific todo

5. **Advanced API Features**

- **Filtering** - Filter todos by their status using query parameters:

  - `GET /api/todos/?status=completed` - Get completed todos
  - `GET /api/todos/?status=pending` - Get pending todos
  - `GET /api/todos/?status=overdue` - Get overdue todos

- **Searching** - Search through todos using the search parameter:

  - `GET /api/todos/?search=keyword` - Search in title and description fields

- **Ordering** - Order todos using the ordering parameter:

  - `GET /api/todos/?ordering=created_at` - Order by creation date (ascending)
  - `GET /api/todos/?ordering=-created_at` - Order by creation date (descending)
  - `GET /api/todos/?ordering=due_date` - Order by due date
  - `GET /api/todos/?ordering=priority` - Order by priority

Available ordering fields: `created_at`, `due_date`, `priority`

- **Request** Examples

  1. Search for high priority todos:

   ```bash
   GET /api/todos/?search=important&ordering=-priority
   ```

  2. Get overdue todos ordered by due date:

  ```bash
  GET /api/todos/?status=overdue&ordering=due_date
  ```

  3. Get completed todos created recently:

  ```bash
  GET /api/todos/?status=completed&ordering=-created_at
  ```

6. **Additional Endpoints**  
   - GET `/api/todos/statistics/`  
     Returns total, completed, pending, and overdue counts  
   - DELETE `/api/todos/clear_completed/`  
     Deletes all completed todos

---

## Running Tests

```bash
python manage.py test todo_app
```

This command will run all tests located in `todo_app/tests.py`, covering registration, login, todos CRUD, statistics, and user isolation.

---

## Key Highlights

1. **Django Backend Implementation ✓**

- Complete `models.py` with `Todo` model
- REST API views in `views.py`
- URL routing in `urls.py`

2. **SQL Database Integration ✓**

- Using SQLite as configured in `settings.py`
- Database migrations in migrations/
- Model queries in `TodoViewSet`

3. **User Authentication ✓**

- Token-based authentication
- Login/Register endpoints
- User-specific todo items
- Password hashing and validation

4. **Todo Features ✓**

- CRUD operations
- Filtering and searching
- Priority levels
- Due dates
- Status tracking (pending/completed/overdue)
- Statistics endpoint

5. **Admin Interface ✓**

- Customized admin panel in `admin.py`
- User-specific views
- Filtering and searching capabilities

6. **API Endpoints ✓**

- `POST /api/register/` - User registration
- `POST /api/login/` - User login
- `GET/POST /api/todos/` - List/Create todos
- `GET/PUT/DELETE /api/todos/{id}/` - Retrieve/Update/Delete todo
- `GET /api/todos/statistics/` - Todo statistics
- `DELETE /api/todos/clear_completed/` - Clear completed todos

7. **Testing ✓**

- Comprehensive test suite in `tests.py`
- Coverage of all major functionality
