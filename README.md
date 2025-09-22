# Users API (PKB)

A part of the PKB app. The API provides endpoints to manage users and handle authentication.

### Features

- Create users.
- Create access tokens.
- Get my user info based on the access token provided with the Authorization header.

### Development

Use devcontainer.

When you get into the dev container for the first time, you should apply database migrations:
```bash
./scripts/migrate
```

There are several helpful scripts:
```bash
# Run migrations.
./scripts/migrate

# Run all tests.
./scripts/test

# Run the Ruff linter.
./scripts/lint
```
