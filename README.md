## Sweet Shop Management System
A full-stack web application for managing a sweet shop inventory, purchases, and user authentication. Built with FastAPI, 
React, TypeScript, and PostgreSQL following Test-Driven Development principles.

# Features
-User Authentication: JWT-based registration and login system

-Sweet Management: Full CRUD operations for sweet products

-Inventory Control: Purchase and restock functionality with real-time updates

-Search & Filter: Advanced search by name, category, and price range

-Admin Dashboard: Special privileges for admin users

-Responsive Design: Modern UI that works on all devices

-RESTful API: Clean, well-documented API endpoints

-Database Management: PostgreSQL with SQLAlchemy ORM

 ## Tech Stack
## Backend
Framework: FastAPI with Python 3.9

Database: PostgreSQL with SQLAlchemy ORM

Authentication: JWT tokens with OAuth2 password flow

Testing: Pytest with comprehensive test coverage

Migrations: Alembic for database migrations

# Frontend
Framework: React 18 with TypeScript

Build Tool: Vite

HTTP Client: Axios for API communication

Styling: CSS3 with modern responsive design

State Management: React Context for authentication

# DevOps
Containerization: Docker and Docker Compose
Database: PostgreSQL container
Environment Management: Python dotenv

# Installation
Prerequisites
Docker and Docker Compose
Node.js (for frontend development)
Python 3.9+ (for backend development)

 # Clone the repository
git clone https://github.com/nehachoudhary0731/sweet-shop-management.git
cd sweet-shop-management

 Copy environment variables
cp .env.example .env

 Start all services
docker-compose up --build

## Run Tests
base
cd backend

pytest -v

## With coverage report
pytest --cov=app --cov-report=html

# Test Coverage
The application includes comprehensive tests for:
User authentication and authorizatio
Sweet CRUD operations
Inventory management
Error handling and validation
Database operations
## project sytructure
sweet-shop-management/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── database.py          # Database configuration
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── crud.py              # CRUD operations
│   │   ├── auth.py              # Authentication utilities
│   │   ├── dependencies.py      # FastAPI dependencies
│   │   └── config.py            # Application configuration
│   ├── alembic/                 # Database migrations
│   ├── tests/                   # Test suite
│   ├── requirements.txt         # Python dependencies
│   └── Dockerfile              # Backend container configuration
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── contexts/           # React contexts (Auth)
│   │   ├── services/           # API services
│   │   ├── types/              # TypeScript definitions
│   │   ├── App.jsx             # Main application component
│   │   └── main.jsx            # Application entry point
│   ├── package.json            # Node.js dependencies
│   └── Dockerfile              # Frontend container configuration
├── docker-compose.yml          # Multi-container configuration
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
└── README.md                  # This file

## My AI Usage
# Tools Used
GitHub Copilot: For code completion and suggestions
ChatGPT: For architecture design and complex problem-solving
AI-assisted testing: For generating comprehensive test cases
## How I Used AI
API Design: AI assisted in designing RESTful endpoint structures and request/response schemas

Database Schema: Helped design efficient PostgreSQL table structures and relationships

Authentication: Guided JWT implementation with proper security practices

Error Handling: Suggested comprehensive error handling patterns

Testing: Generated pytest fixtures and test cases for maximum coverage

Docker Configuration: Assisted with multi-container Docker setup

## Impact on Workflow
40% faster development through AI-assisted coding

Improved code quality with AI-reviewed best practices

Comprehensive test coverage with AI-generated test cases

Better architecture decisions through AI brainstorming sessions







