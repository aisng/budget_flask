# Budget tracker

Simple Flask application where users can create profiles and track their balance by adding income and expenses.

## Running the application

1. Open terminal or command prompt.
2. Navigate to the project directory where the file `app.py` is located.
3. Install dependencies: 
```bash
pip install -r requirements.txt
```
4. Add a SECRET_KEY to your enviroment variables or change it manually in `config.py` (default set to "verysecretkey").    Set up other environment variables in `config.py` if you want to send password reset emails from gmail.
5. Run the development server:
```bash
python app.py
```



