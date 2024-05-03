# ModeMixer Backend

## How to run API
- get .env file
- run `uvicorn app.main:app --reload`

## Tasks

### Webscaper
- [ ] Create List of Celebrities with most fashion
- [ ] Automatically scrape celebs, upload image to s3 and create entry in Mongo in MensFashionReference or WomensFashionReference table. Look at ./app/models.py for db models

## Frontend
- [ ] Display Collections
- [ ] Display Items
- [ ] Create Admin portal
    - [ ] Keep Item Description Under 450 characters

## Backend
- [ ] Create paginated view of collections