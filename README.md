# web_checkin
QR based web check in 

### Security features
- JWT token
- bcrypt for hashing password

### Config
Requires to set in `backend/.env` the following environment variables:
- `SECRET_KEY` for JWT encryption (see `api/config.py` for an example)
- `MASTER_KEY` for super permissions.
- `POSTGRES_PASSWORD` for Docker deploy.

### Docker deploy
Run with `docker-compose up`.
- The _api_ will be on port `8080`
- The _html_ files will be on port `80`