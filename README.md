# TICKET BOOKING SYSTEM

## Development

1. After making db model changes, run the following:
    ```
    alembic revision --autogenerate -m "Commit message"
    ```

2. To downgrade a change
    ```
    alembic downgrade <revision_id>
    ```

3. To apply migrations to DB.
    ```
    alembic upgrade head
    ```

4. To run server
    with uvicorn:
    ```
    uvicorn app.main:app --reload --port 8000
    ```
    or
    ```
    python -m app.run
    ```
