# GLI Content Management Database Setup Commands

## 1. Install Dependencies
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

## 2. Create Migrations
```bash
# Create migrations for the new gli_content app
python manage.py makemigrations gli_content

# Optional: View migration SQL before applying
python manage.py sqlmigrate gli_content 0001

# Apply all migrations
python manage.py migrate
```

## 3. Create Superuser (for admin access)
```bash
python manage.py createsuperuser
```

## 4. Load Initial Data (Optional)
```bash
# If you have fixture files
python manage.py loaddata initial_categories.json
python manage.py loaddata initial_business_content.json
```

## 5. API Endpoints Available

### Business Content Management
- GET/POST `/api/v1/business-content/` - List/Create business content
- GET/PUT/PATCH/DELETE `/api/v1/business-content/{id}/` - Detail operations
- GET `/api/v1/business-content/by_section/?section=background` - Get content by section

### Shopping Mall
- GET `/api/v1/shopping/categories/` - List shopping categories
- GET `/api/v1/shopping/products/` - List products (with search & filters)
- GET `/api/v1/shopping/products/featured/` - Featured products
- GET `/api/v1/shopping/products/by_category/?category_id={uuid}` - Products by category
- POST/GET `/api/v1/shopping/orders/` - Create/List orders
- POST `/api/v1/shopping/orders/{id}/cancel/` - Cancel order
- POST `/api/v1/shopping/orders/{id}/confirm_payment/` - Confirm payment

### RWA Investment System
- GET `/api/v1/rwa/categories/` - List RWA categories
- GET `/api/v1/rwa/assets/` - List investment assets (with search & filters)
- GET `/api/v1/rwa/assets/featured/` - Featured assets
- GET `/api/v1/rwa/assets/by_category/?category_id={uuid}` - Assets by category
- GET `/api/v1/rwa/assets/by_risk_level/?risk_level=low` - Assets by risk level
- POST `/api/v1/rwa/assets/{id}/invest/` - Make investment

### Investment Portfolio
- GET `/api/v1/investments/` - List user investments
- GET `/api/v1/investments/stats/` - Investment statistics
- GET `/api/v1/investments/portfolio/` - Portfolio breakdown

### Dashboard Statistics
- GET `/api/v1/dashboard/overview/` - Complete dashboard statistics

## 6. Admin Interface
Access Django admin at `/admin/` to manage:
- Business content
- Shopping categories and products
- RWA categories and assets  
- Investment records
- User orders

## 7. API Documentation
- Swagger UI: `/api/schema/swagger-ui/`
- OpenAPI Schema: `/api/schema/`

## Notes
- All models use UUID primary keys for better security
- Comprehensive indexing for performance
- JSON fields for flexible metadata storage
- Built-in profit/loss calculations for investments
- Order management with transaction tracking
- Full CRUD operations via Django REST Framework