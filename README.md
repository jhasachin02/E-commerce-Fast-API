# E-Commerce Backend API

A modern, scalable FastAPI-based e-commerce backend application with MongoDB integration using Motor. Built with best practices including comprehensive error handling, type safety, and performance monitoring.

## 🚀 Features

- ✅ **FastAPI** with async/await support and automatic OpenAPI documentation
- ✅ **MongoDB** integration with Motor async driver
- ✅ **Pydantic** models for robust data validation and serialization
- ✅ **Comprehensive Error Handling** with custom exceptions and logging
- ✅ **Performance Monitoring** with request/response logging and timing
- ✅ **Type Safety** with complete type hints throughout
- ✅ **Environment Configuration** with Pydantic settings management
- ✅ **CORS Support** for frontend integration
- ✅ **Graceful Degradation** for missing data scenarios

## 🛠 Tech Stack

- **Python 3.10+** - Modern Python with type hints
- **FastAPI 0.104+** - High-performance web framework
- **Motor 3.3+** - Async MongoDB driver
- **MongoDB** - NoSQL database
- **Pydantic 2.5+** - Data validation and settings management
- **Uvicorn** - ASGI server for production deployment

## 📁 Project Structure

```
Backend 2/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .env.example           # Environment variables template
├── app/
│   ├── __init__.py        # App package initialization
│   ├── config.py          # Application configuration
│   ├── database.py        # MongoDB connection and utilities
│   ├── middleware.py      # Custom middleware for logging/error handling
│   ├── models.py          # Pydantic models for data validation
│   └── routers/
│       ├── __init__.py    # Routers package initialization
│       ├── products.py    # Product-related endpoints
│       └── orders.py      # Order-related endpoints
```

## 🚀 Detailed Setup Instructions

### Prerequisites

- **Python 3.10+** installed on your system
- **MongoDB** running locally or accessible remotely
- **Git** for version control

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd Backend-2

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the root directory:

```env
# MongoDB Connection Settings
MONGO_DETAILS=mongodb://localhost:27017
DATABASE_NAME=ecommerce

# Application Settings
APP_NAME=E-Commerce Backend API
APP_VERSION=1.0.0
DEBUG=false

# API Settings
API_PREFIX=/api/v1
DEFAULT_LIMIT=10
MAX_LIMIT=100

# CORS Settings (comma-separated for multiple origins)
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# Optional: MongoDB Authentication (for MongoDB Atlas)
# MONGODB_USERNAME=your_username
# MONGODB_PASSWORD=your_password
```

### 4. MongoDB Setup

#### Local MongoDB
```bash
# Install MongoDB (Ubuntu/Debian)
sudo apt-get install mongodb

# Start MongoDB service
sudo systemctl start mongodb

# Verify MongoDB is running
mongo --eval "db.runCommand('ping')"
```

#### MongoDB Atlas (Cloud)
1. Create account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a new cluster
3. Get your connection string
4. Update `MONGO_DETAILS` in `.env` file

### 5. Run the Application

#### Development Mode
```bash
# Start with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or run directly
python main.py
```

#### Production Mode
```bash
# Start production server
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

### Health Check
- **Health Endpoint**: `http://localhost:8000/health`

## 🔗 API Endpoints Documentation

### Products API

#### 1. Create Product
```http
POST /api/v1/products/
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Classic T-Shirt",
  "price": 29.99,
  "sizes": [
    {
      "size": "S",
      "quantity": 10
    },
    {
      "size": "M", 
      "quantity": 15
    },
    {
      "size": "L",
      "quantity": 8
    }
  ]
}
```

**Response (201 Created):**
```json
{
  "id": "507f1f77bcf86cd799439011"
}
```

#### 2. List Products
```http
GET /api/v1/products/?name=shirt&size=M&limit=10&offset=0
```

**Query Parameters:**
- `name` (optional): Product name for partial search (case-insensitive)
- `size` (optional): Filter products with specific size
- `limit` (default: 10): Number of products per page (1-100)
- `offset` (default: 0): Number of products to skip

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": "507f1f77bcf86cd799439011",
      "name": "Classic T-Shirt",
      "price": 29.99
    }
  ],
  "page": {
    "next": "10",
    "limit": 10,
    "previous": null
  }
}
```

#### 3. Get Product by ID
```http
GET /api/v1/products/{product_id}
```

**Response (200 OK):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "name": "Classic T-Shirt",
  "price": 29.99
}
```

### Orders API

#### 1. Create Order
```http
POST /api/v1/orders/
Content-Type: application/json
```

**Request Body:**
```json
{
  "userId": "user123",
  "items": [
    {
      "productId": "507f1f77bcf86cd799439011",
      "qty": 2
    },
    {
      "productId": "507f1f77bcf86cd799439012",
      "qty": 1
    }
  ]
}
```

**Response (201 Created):**
```json
{
  "id": "507f1f77bcf86cd799439013"
}
```

#### 2. Get User Orders
```http
GET /api/v1/orders/user/{user_id}?limit=10&offset=0
```

**Path Parameters:**
- `user_id`: User ID to filter orders

**Query Parameters:**
- `limit` (default: 10): Number of orders per page (1-100)
- `offset` (default: 0): Number of orders to skip

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": "507f1f77bcf86cd799439013",
      "userId": "user123",
      "items": [
        {
          "productDetails": {
            "id": "507f1f77bcf86cd799439011",
            "name": "Classic T-Shirt"
          },
          "qty": 2
        }
      ],
      "total": 59.98
    }
  ],
  "page": {
    "next": "10",
    "limit": 10,
    "previous": null
  }
}
```

#### 3. Get Order by ID
```http
GET /api/v1/orders/order/{order_id}
```

**Response (200 OK):**
```json
{
  "id": "507f1f77bcf86cd799439013",
  "userId": "user123",
  "items": [
    {
      "productDetails": {
        "id": "507f1f77bcf86cd799439011",
        "name": "Classic T-Shirt"
      },
      "qty": 2
    }
  ],
  "total": 59.98
}
```

## 🗄️ MongoDB Schema and Relationships

### Collections Structure

#### 1. `products` Collection
```javascript
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "name": "Classic T-Shirt",
  "price": 29.99,
  "sizes": [
    {
      "size": "S",
      "quantity": 10
    },
    {
      "size": "M",
      "quantity": 15
    }
  ]
}
```

#### 2. `orders` Collection
```javascript
{
  "_id": ObjectId("507f1f77bcf86cd799439013"),
  "userId": "user123",
  "items": [
    {
      "productId": "507f1f77bcf86cd799439011",
      "qty": 2,
      "price": 29.99
    }
  ],
  "total": 59.98,
  "created_at": ISODate("2024-01-15T10:30:00Z"),
  "updated_at": ISODate("2024-01-15T10:30:00Z")
}
```

### Relationships
- **Orders → Products**: Orders reference products via `productId` field
- **One-to-Many**: One product can be in multiple orders
- **Embedded Data**: Product details are fetched and embedded in order responses

### Indexes (Recommended)
```javascript
// For better performance
db.products.createIndex({ "name": "text" })
db.orders.createIndex({ "userId": 1 })
db.orders.createIndex({ "created_at": -1 })
```

## 🚀 Deployment

### Docker Deployment

#### 1. Create Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 2. Create docker-compose.yml
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MONGO_DETAILS=mongodb://mongo:27017
      - DATABASE_NAME=ecommerce
    depends_on:
      - mongo

  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
```

#### 3. Deploy with Docker
```bash
# Build and run
docker-compose up --build

# Or run in background
docker-compose up -d
```

### Production Deployment

#### 1. Environment Variables
```env
# Production settings
DEBUG=false
MONGO_DETAILS=mongodb://your-production-mongo:27017
DATABASE_NAME=ecommerce_prod
CORS_ORIGINS=https://your-frontend-domain.com
```

#### 2. Using Gunicorn (Recommended)
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### 3. Using Nginx as Reverse Proxy
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Cloud Deployment Options

#### 1. Heroku
```bash
# Create Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

#### 2. AWS EC2
```bash
# Install dependencies
sudo apt-get update
sudo apt-get install python3-pip nginx

# Setup systemd service
sudo nano /etc/systemd/system/ecommerce-api.service
```

#### 3. Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/ecommerce-api
gcloud run deploy --image gcr.io/PROJECT_ID/ecommerce-api --platform managed
```

## 🧪 Testing

### Run Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/
```

### API Testing with curl
```bash
# Health check
curl http://localhost:8000/health

# Create product
curl -X POST http://localhost:8000/api/v1/products/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Product","price":29.99,"sizes":[{"size":"M","quantity":10}]}'

# Get products
curl http://localhost:8000/api/v1/products/
```

## 📊 Monitoring and Logging

### Logs
- **Application Logs**: Structured logging with timestamps
- **Request Logs**: All API requests with processing time
- **Error Logs**: Detailed error information with stack traces

### Metrics
- **Response Times**: Available in `X-Process-Time` header
- **Error Rates**: Tracked in application logs
- **Database Performance**: MongoDB query performance

## 🔧 Configuration

### Environment Variables Reference
| Variable | Default | Description |
|----------|---------|-------------|
| `MONGO_DETAILS` | `mongodb://localhost:27017` | MongoDB connection string |
| `DATABASE_NAME` | `ecommerce` | Database name |
| `DEBUG` | `false` | Debug mode |
| `API_PREFIX` | `/api/v1` | API route prefix |
| `DEFAULT_LIMIT` | `10` | Default pagination limit |
| `MAX_LIMIT` | `100` | Maximum pagination limit |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the API docs at `/docs`
- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Use GitHub Discussions for questions

## 🔄 Version History

- **v1.0.0**: Initial release with basic CRUD operations
- **v1.1.0**: Added comprehensive error handling and logging
- **v1.2.0**: Enhanced type safety and validation
- **v1.3.0**: Added performance monitoring and middleware

---

**Built with ❤️ using FastAPI and MongoDB** 