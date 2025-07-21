# Development Guide

## 🚀 Quick Start for Developers

### Prerequisites
- Python 3.11+
- MongoDB Atlas account (or local MongoDB)
- Git

### Initial Setup

1. **Clone and navigate**
   ```bash
   git clone https://github.com/jhasachin02/E-commerce-Fast-API.git
   cd E-commerce-Fast-API
   ```

2. **Setup environment**
   ```bash
   # Install all dependencies
   make setup
   
   # Or manually:
   pip install -r requirements.txt
   pip install pytest pytest-asyncio httpx black flake8
   ```

3. **Configure environment variables**
   ```bash
   # Create .env file
   cp .env.example .env
   # Edit .env with your MongoDB connection details
   ```

## 📋 Development Commands

### Using Make (Recommended)
```bash
# Show all available commands
make help

# Development server with auto-reload
make run

# Run all tests
make test

# Format code
make format

# Lint code  
make lint

# Clean cache files
make clean

# Deploy to production
make deploy
```

### Direct Commands
```bash
# Start development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run tests
python tests/run_all_tests.py
pytest tests/ -v

# Format code
black app/ tests/ main.py

# Lint code
flake8 app/ main.py
```

## 📁 Directory Structure Guide

### `/app/` - Main Application
- `config.py` - Configuration settings
- `database.py` - MongoDB connection and operations
- `middleware.py` - Custom middleware (CORS, logging)
- `models.py` - Pydantic data models
- `routers/` - API route handlers

### `/tests/` - Test Suite
- `run_all_tests.py` - Master test runner
- `test_*.py` - Individual test modules
- Organized by functionality (database, API, deployment)

### `/scripts/` - Utility Scripts  
- `start.py` - Production server startup
- `demo_api.py` - API demonstration
- `mongodb_diagnostics.py` - Database diagnostics

### `/deployment/` - Deployment Configs
- `render.yaml` - Render platform config
- `Procfile` - Heroku/Railway config
- `runtime.txt` - Python version spec

### `/docs/` - Documentation
- `TEST_REPORT.md` - Comprehensive test results

## 🧪 Testing Strategy

### Test Categories

1. **Database Tests** (`test_mongodb.py`)
   - Connection testing
   - CRUD operations
   - Data validation

2. **API Tests** (`test_local_app.py`)
   - Endpoint functionality
   - Request/response validation
   - Error handling

3. **Deployment Tests** (`test_render_deployment.py`)
   - Production environment testing
   - Live API validation

4. **Integration Tests** (in various files)
   - End-to-end workflows
   - Cross-module functionality

### Running Tests

```bash
# All tests with detailed reporting
python tests/run_all_tests.py

# Specific test file
python tests/test_mongodb.py

# With pytest (more detailed output)
pytest tests/test_mongodb.py -v -s

# Quick smoke tests
pytest tests/ -x --tb=short
```

## 🔧 Code Style and Standards

### Formatting
- **Black** for code formatting
- **isort** for import organization
- **flake8** for linting

### Standards
- Type hints for function parameters and returns
- Docstrings for classes and functions
- Async/await for I/O operations
- Error handling with proper exceptions

### Example Function Structure
```python
async def create_product(product: ProductCreate) -> ProductResponse:
    """
    Create a new product in the database.
    
    Args:
        product: Product data to create
        
    Returns:
        ProductResponse: Created product information
        
    Raises:
        HTTPException: If creation fails
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Product creation failed: {e}")
        raise HTTPException(status_code=500, detail="Creation failed")
```

## 🗄️ Database Guidelines

### MongoDB Collections
- `products` - Product catalog
- `orders` - Order transactions

### Data Validation
- Use Pydantic models for all data
- Validate inputs at API layer
- Handle MongoDB ObjectId conversions

### Connection Management
- Async Motor driver
- Connection pooling enabled
- Proper error handling

## 🚀 Deployment Process

### Local Testing
```bash
# Test locally
make test
make run

# Verify endpoints
curl http://localhost:8000/health
```

### Production Deployment
```bash
# Deploy to Render (auto-deploy on push)
git add .
git commit -m "Feature: description"
git push origin master

# Or use make command
make deploy
```

## 📊 Monitoring and Debugging

### Logs
- Application logs in structured format
- Request/response logging via middleware
- Error tracking with stack traces

### Health Checks
- `/health` endpoint for uptime monitoring
- Database connection validation
- Environment variable checks

### Performance Monitoring
- Response time tracking in headers
- Database query optimization
- Memory usage monitoring

## 🤝 Contributing Workflow

1. **Create feature branch**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Develop and test**
   ```bash
   # Make changes
   make test
   make format
   make lint
   ```

3. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: descriptive message"
   git push origin feature/new-feature
   ```

4. **Create pull request**
   - Include description of changes
   - Ensure all tests pass
   - Update documentation if needed

## 🔍 Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**
   ```bash
   # Check connection string in .env
   python tests/test_mongodb.py
   ```

2. **Import Errors**
   ```bash
   # Check Python path
   export PYTHONPATH="${PYTHONPATH}:${PWD}"
   ```

3. **Port Already in Use**
   ```bash
   # Find and kill process
   netstat -ano | findstr :8000
   taskkill /PID <process_id> /F
   ```

### Getting Help
- Check logs in terminal output
- Run diagnostic scripts in `/scripts/`
- Review test outputs for specific errors
- Check MongoDB Atlas connection and whitelist

## 📈 Performance Tips

- Use async/await for all I/O operations
- Implement proper database indexing
- Monitor response times in headers
- Use connection pooling
- Cache frequently accessed data

## 🔐 Security Considerations

- Never commit `.env` files
- Use environment variables for secrets
- Validate all input data with Pydantic
- Implement proper error handling
- Use HTTPS in production
