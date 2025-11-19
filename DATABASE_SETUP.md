# Trust Hub - Database Setup

This application uses PostgreSQL as the database, running in Docker.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.8+ installed

## Setup Instructions

### 1. Start PostgreSQL Database

From the project root directory:

```bash
docker-compose up -d
```

This will start a PostgreSQL container with the following configuration:
- **Database**: trusthub_db
- **User**: trusthub_user
- **Password**: trusthub_pass
- **Port**: 5432
- **Container name**: trust-hub-db

### 2. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Initialize Database

Create tables and seed with mock data:

```bash
cd backend
python init_db.py
```

### 4. Start Backend Server

```bash
cd backend
python app.py
```

The backend will run on `http://localhost:5001`

## Database Management

### Check Database Status

```bash
docker ps
```

### Stop Database

```bash
docker-compose down
```

### Reset Database (Delete all data)

```bash
docker-compose down -v
docker-compose up -d
cd backend
python init_db.py
```

### Access PostgreSQL CLI

```bash
docker exec -it trust-hub-db psql -U trusthub_user -d trusthub_db
```

Useful PostgreSQL commands:
- `\dt` - List all tables
- `\d table_name` - Describe table structure
- `SELECT * FROM users;` - Query users table
- `\q` - Quit

## Database Schema

The application includes the following tables:

- **users** - User accounts with authentication
- **tokens** - Session tokens for authenticated users
- **posts** - Social feed posts
- **courses** - Educational courses
- **spaces** - Community spaces/groups
- **members** - Community members
- **events** - Upcoming events

## Troubleshooting

### Port 5432 already in use

If you have PostgreSQL running locally, either:
1. Stop the local PostgreSQL service
2. Change the port in `docker-compose.yml` and `.env` file

### Connection refused

Make sure the database is running:
```bash
docker-compose ps
```

If the container is not healthy, check logs:
```bash
docker-compose logs postgres
```

### Database not initialized

Run the initialization script:
```bash
cd backend
python init_db.py
```
