# CS623-Database-Transaction-Project
 Database Transaction Project with ACID Properties

## Description
Implementation of ACID-compliant database transactions using PostgreSQL with reactive constraints (ON DELETE CASCADE, ON UPDATE CASCADE).

## Team Members
- Rohit Shukla
- Tae Kown

## Project Requirements
- 6 database transactions
- Python with psycopg2
- PostgreSQL database
- Interactive user interface

## Files
- `main.py` - Main transaction execution script
- `README.md` - Concept explanations
- `CS623.session.sql`

## How to Run
```bash
python main.py
```

## Database Setup
Ensure PostgreSQL is running on localhost:5433 with:
- Database: postgres
- User: postgres
- Password: postgres

## Concepts Covered
- ACID Properties (Atomicity, Consistency, Isolation, Durability)
- Reactive Constraints (Foreign Keys with CASCADE)
- Transaction Management
