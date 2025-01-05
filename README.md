### TO-DO App using Django
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