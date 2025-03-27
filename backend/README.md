
# Template Prompt Backend

This is a Python backend with clean architecture for the Template Prompt application.

## Setup

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Set environment variables:
```
export DB_URL=postgresql://postgres:[YOUR-PASSWORD]@db.oatxqwsmylwagybwqmjg.supabase.co:5432/postgres
```

3. Run the application:
```
python app.py
```

## Project Structure

- `app.py`: Main application entry point
- `config/`: Configuration files
- `domain/`: Domain entities and business rules
- `application/`: Application use cases
- `infrastructure/`: External interfaces (database, API, etc.)
- `adapters/`: Adapters between layers
- `migrations/`: Database migrations
