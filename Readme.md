# Todo App

![Website Image](ToDo-App.jpg)

This is a simple Todo App built using Flask, Python, and SQLAlchemy.
It allows users to manage their tasks with the following features:

- User Registration: Users can sign up for an account.
- User Login: Registered users can log in to their accounts.
- Add New Task: Users can create new tasks to keep track of their todos.
- Mark as Completed: Users can mark tasks as completed when they are done.
- Update and Delete: Users can edit or delete tasks as needed.
- Logout: Users can log out of their accounts securely.

## Technologies Used

- **Flask**: The web application framework used for building the app.
- **Python**: The programming language used for the backend logic.
- **SQLAlchemy**: A powerful SQL toolkit and Object-Relational Mapping (ORM) library used for data storage and retrieval.

## Getting Started

To run this application locally, follow these steps:

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/sheenam-waris/todo-app.git
    ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
    ```

3. Activate the virtual environment:
    * On Windows:
    ```bash
        venv\Scripts\activate
    ```
    * On macOS and Linux:
    ```bash
        source venv/bin/activate
    ```
4. Install the project dependencies:
    ```bash
    pip install -r requirements.txt

    ```

5. Run the application:
    ```bash
    python app.py
    ```

Open your web browser and navigate to http://localhost:5000 to use the Todo App.