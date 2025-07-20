# E-Commerce FastAPI Backend

🚀 **A production-ready, modern e-commerce backend API built with FastAPI and MongoDB Atlas**

[![Deploy Status](https://img.shields.io/badge/Deploy-Live-brightgreen)](https://e-commerce-fast-api-1.onrender.com)
[![API Docs](https://img.shields.io/badge/API-Documentation-blue)](https://e-commerce-fast-api-1.onrender.com/docs)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-green)](https://fastapi.tiangolo.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green)](https://mongodb.com)

## 🌐 Live Deployment

- **🔗 API Base URL**: https://e-commerce-fast-api-1.onrender.com
- **📚 Interactive API Docs**: https://e-commerce-fast-api-1.onrender.com/docs  
- **🏥 Health Check**: https://e-commerce-fast-api-1.onrender.com/health
- **📖 Alternative Docs**: https://e-commerce-fast-api-1.onrender.com/redoc

## ✨ Features

- 🚀 **High Performance**: FastAPI with async/await support
- 📊 **MongoDB Integration**: Using Motor async driver with MongoDB Atlas
- 🔒 **Data Validation**: Comprehensive Pydantic models
- 📖 **Auto Documentation**: Interactive Swagger UI and ReDoc
- 🛡️ **Error Handling**: Robust error handling and logging
- 🌍 **CORS Enabled**: Ready for frontend integration  
- 🔍 **Health Monitoring**: Built-in health checks
- 📈 **Production Ready**: Deployed on Render with proper configuration

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | 0.116+ | Modern web framework for APIs |
| **Python** | 3.11+ | Programming language |
| **Motor** | 3.7+ | Async MongoDB driver |
| **MongoDB Atlas** | Cloud | NoSQL database (M0 free tier) |
| **Pydantic** | 2.11+ | Data validation and serialization |
| **Uvicorn** | Latest | ASGI server for production |
| **Render** | Cloud | Deployment platform |

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │◄──►│  FastAPI Backend │◄──►│ MongoDB Atlas   │
│   (React/Vue)   │    │  (Render Cloud)  │    │ (Cloud Database)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────┐
                       │ Auto-Generated│
                       │ API Docs      │
                       │ (Swagger UI)  │
                       └──────────────┘
```

## � API Endpoints

### **Products Management**
| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| `GET` | `/api/v1/products/` | List all products with filtering & pagination | ✅ Live |
| `POST` | `/api/v1/products/` | Create a new product | ✅ Live |
| `GET` | `/api/v1/products/{product_id}` | Get specific product by ID | ✅ Live |

### **Orders Management**  
| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| `POST` | `/api/v1/orders/` | Create a new order | ✅ Live |
| `GET` | `/api/v1/orders/{user_id}` | Get orders for specific user | ✅ Live |
| `GET` | `/api/v1/orders/order/{order_id}` | Get specific order by ID | ✅ Live |

### **System Endpoints**
| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| `GET` | `/` | Welcome message & API info | ✅ Live |
| `GET` | `/health` | Health check endpoint | ✅ Live |
| `GET` | `/docs` | Interactive API documentation | ✅ Live |
| `GET` | `/redoc` | Alternative API documentation | ✅ Live |

## 📊 Data Models

### **Product Model**
```json
{
  "name": "Classic T-Shirt",
  "price": 29.99,
  "sizes": [
    {"size": "S", "quantity": 10},
    {"size": "M", "quantity": 15},
    {"size": "L", "quantity": 12}
  ]
}
```

### **Order Model**
```json
{
  "userId": "user123",
  "items": [
    {"productId": "507f1f77bcf86cd799439011", "qty": 2}
  ]
}
```

## 🏃‍♂️ Quick Start

### **Test the Live API**
```bash
# Health Check
curl https://e-commerce-fast-api-1.onrender.com/health

# Get Products
curl https://e-commerce-fast-api-1.onrender.com/api/v1/products/

# Create Product
curl -X POST https://e-commerce-fast-api-1.onrender.com/api/v1/products/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Product","price":29.99,"sizes":[{"size":"M","quantity":10}]}'
```

## 💻 Local Development

### **Prerequisites**
- Python 3.11+ installed
- MongoDB Atlas account (free M0 cluster)
- Git installed

### **Setup**
1. **Clone the repository**
```bash
git clone https://github.com/jhasachin02/E-commerce-Fast-API.git
cd E-commerce-Fast-API
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Environment Configuration**
Create a `.env` file in the root directory:
```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/ecommerce?retryWrites=true&w=majority&appName=AppName
DATABASE_NAME=ecommerce
```

4. **Run the application**
```bash
# Using Python directly
python main.py

# Or using Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

5. **Access the API**
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Health: http://localhost:8000/health

## 📁 Project Structure

```
E-commerce-Fast-API/
├── 📄 main.py                 # FastAPI application entry point
├── 📄 start.py                # Production startup script
├── 📄 requirements.txt        # Python dependencies
├── 📄 Procfile               # Render deployment configuration
├── 📄 render.yaml            # Render service configuration
├── 📄 runtime.txt            # Python version specification
├── 📄 .gitignore             # Git ignore rules
├── 📄 README.md              # This documentation
├── 📁 app/
│   ├── 📄 __init__.py        # Package initialization
│   ├── 📄 config.py          # Application configuration
│   ├── 📄 database.py        # MongoDB connection & utilities
│   ├── 📄 middleware.py      # Custom middleware (logging, CORS)
│   ├── 📄 models.py          # Pydantic data models
│   └── 📁 routers/
│       ├── 📄 __init__.py    # Router package init
│       ├── 📄 products.py    # Product CRUD operations
│       └── 📄 orders.py      # Order management
## � Deployment

### **Current Deployment: Render**
The application is currently deployed on **Render** with automatic deployments from the `master` branch.

**Live URL**: https://e-commerce-fast-api-1.onrender.com

### **Deployment Configuration**
- **Platform**: Render (https://render.com)
- **Runtime**: Python 3.11
- **Start Command**: `python start.py`
- **Auto Deploy**: Enabled from GitHub
- **Environment Variables**: 
  - `MONGODB_URL`: MongoDB Atlas connection string
  - `DATABASE_NAME`: ecommerce

### **Deploy to Other Platforms**

#### **Heroku**
```bash
# Install Heroku CLI, then:
heroku create your-app-name
heroku config:set MONGODB_URL="your-mongodb-connection-string"
git push heroku master
```

#### **Railway**
```bash
# Connect GitHub repo to Railway
# Set MONGODB_URL environment variable
# Deploy automatically from GitHub
```

#### **Docker (Optional)**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "start.py"]
```

## 🧪 Testing

### **Run Tests Locally**
```bash
# Test API functionality
python simple_test.py

# Full demonstration
python demo_api.py

# Test MongoDB connection
python test_mongodb.py
```

### **API Testing with cURL**
```bash
# Test health endpoint
curl https://e-commerce-fast-api-1.onrender.com/health

# Test products endpoint
curl https://e-commerce-fast-api-1.onrender.com/api/v1/products/

# Create a product
curl -X POST https://e-commerce-fast-api-1.onrender.com/api/v1/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sample Product",
    "price": 19.99,
    "sizes": [
      {"size": "M", "quantity": 5}
    ]
  }'
```

## � Configuration

### **Environment Variables**
| Variable | Description | Example |
|----------|-------------|---------|
| `MONGODB_URL` | MongoDB Atlas connection string | `mongodb+srv://user:pass@cluster.mongodb.net/db` |
| `DATABASE_NAME` | Database name | `ecommerce` |
| `PORT` | Server port (auto-set by hosting platform) | `8000` |

### **MongoDB Atlas Setup**
1. Create free account at [MongoDB Atlas](https://cloud.mongodb.com/)
2. Create new cluster (M0 free tier)
3. Create database user
4. Whitelist IP addresses (0.0.0.0/0 for development)
5. Get connection string
6. Replace `<username>`, `<password>`, and `<database>` in connection string

## 📈 Performance Features

- ⚡ **Async Operations**: Full async/await implementation
- 🔄 **Connection Pooling**: Optimized MongoDB connections
- 📊 **Request Logging**: Comprehensive request/response logging
- 🛡️ **Error Handling**: Graceful error responses
- ⏱️ **Timeouts**: Configurable database timeouts
- � **Health Checks**: Built-in monitoring endpoints

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 API Documentation

The API is fully documented with OpenAPI/Swagger:

- **Interactive Docs**: https://e-commerce-fast-api-1.onrender.com/docs
- **ReDoc Format**: https://e-commerce-fast-api-1.onrender.com/redoc
- **OpenAPI JSON**: https://e-commerce-fast-api-1.onrender.com/openapi.json

## 📊 Database Schema

### **Products Collection**
```json
{
  "_id": "ObjectId",
  "name": "string",
  "price": "decimal",
  "sizes": [
    {
      "size": "string",
      "quantity": "integer"
    }
  ]
}
```

### **Orders Collection**
```json
{
  "_id": "ObjectId",
  "userId": "string",
  "items": [
    {
      "productId": "ObjectId",
      "qty": "integer"
    }
  ],
  "total": "decimal",
  "createdAt": "datetime"
}
```

## 🔮 Future Enhancements

- [ ] User authentication & JWT tokens
- [ ] Payment gateway integration
- [ ] Inventory management
- [ ] Order status tracking
- [ ] Email notifications
- [ ] Admin dashboard
- [ ] Rate limiting
- [ ] Caching with Redis
- [ ] Unit & integration tests
- [ ] CI/CD pipeline

## 📞 Support

- **GitHub Issues**: [Create an issue](https://github.com/jhasachin02/E-commerce-Fast-API/issues)
- **Documentation**: [API Docs](https://e-commerce-fast-api-1.onrender.com/docs)
- **Live Demo**: [Try the API](https://e-commerce-fast-api-1.onrender.com)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
- [MongoDB Atlas](https://cloud.mongodb.com/) - Cloud database service
- [Render](https://render.com/) - Deployment platform
- [Motor](https://motor.readthedocs.io/) - Async MongoDB driver

---

**⭐ If you found this project helpful, please give it a star on GitHub!**

**🚀 Ready to integrate with your frontend? Check out the [live API documentation](https://e-commerce-fast-api-1.onrender.com/docs)!**
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