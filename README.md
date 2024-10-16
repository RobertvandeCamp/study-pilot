# study-pilot

## Setup and Run the Application

### Prerequisites

- Python 3.6 or higher
- Virtual environment (optional but recommended)

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/RobertvandeCamp/study-pilot.git
   cd study-pilot
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Configuration

1. Set the OpenAI API key as an environment variable:
   ```sh
   export OPENAI_API_KEY='your_openai_api_key'  # On Windows use `set OPENAI_API_KEY=your_openai_api_key`
   ```

2. Create a `.env` file in the root directory of the project and add the following line:
   ```sh
   OPENAI_API_KEY=your_openai_api_key
   ```

3. Update the database configuration in `__init__.py` if necessary.

### Running the Application

1. Start the Flask application:
   ```sh
   python -m flask run
   ```

2. The application will be available at `http://127.0.0.1:5000/`.

### API Endpoints

- **POST /chat**
  - Request body:
    ```json
    {
      "user_id": "user123",
      "input": "Hello, how are you?"
    }
    ```
  - Response:
    ```json
    {
      "response": "I'm good, thank you!"
    }
    ```

- **GET /chat/latest**
  - Request parameters:
    - `user_id`: The ID of the user.
  - Response:
    ```json
    {
      "response": "I'm good, thank you!"
    }
    ```

### Unit Tests

1. Run the unit tests:
   ```sh
   python -m unittest discover tests
   ```

### Dependencies

- Flask
- SQLAlchemy
- OpenAI
- python-dotenv
- flask-cors
- Other dependencies listed in `requirements.txt`
