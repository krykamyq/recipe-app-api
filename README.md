# Recipe App API

This is a simple Recipe API built with Django and Django REST framework.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Recipe App API is a RESTful web service that allows users to manage recipes. It provides endpoints for creating, updating, and viewing recipes and their associated ingredients. This API is designed as a back end for a recipe management system.

## Features

- User authentication and authorization.
- Create, edit, and delete recipes.
- Manage ingredients for each recipe.
- API endpoints for listing and filtering recipes.

## Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

- Python 3.7+
- Virtual environment (recommended)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/krykamyq/recipe-app-api.git
2. Create a virtual environment (optional but recommended):

    python -m venv env
    source env/bin/activate  # On Windows, use: env\Scripts\activate
3. Install the project dependencies:
    pip install -r requirements.txt
4. Apply database migrations:
    python manage.py migrate
5. Create superuser account:
    python manage.py createsuperuser
6. Start the development server:
    python manage.py runserver

The API should now be accessible at http://127.0.0.1:8000/

## Usage

To use the Recipe App API, you can interact with it via HTTP requests. You can find detailed documentation on how to use the API by accessing the /api/docs/ endpoint when the server is running locally. This documentation provides information on available endpoints and how to use them.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and test them.
4. Submit a pull request with a clear description of your changes.

## License
This project is licensed under the MIT License - see the LICENSE file for details.




