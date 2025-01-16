# Railway Management System

A comprehensive Railway Management System designed to simplify and streamline the processes of railway operations, including ticket booking, train scheduling, passenger management, and more. This system is built to provide an intuitive interface and efficient performance.

## Features

- **User-Friendly Interface:** Easy navigation and clean design for a seamless user experience.
- **Ticket Booking:** Allows users to book, cancel, and view tickets.
- **Train Scheduling:** View and manage train schedules effortlessly.
- **Passenger Management:** Maintain passenger details securely.
- **Admin Dashboard:** Admin functionalities to monitor and manage the system.
- **Secure:** Robust authentication and data management.

---

## Technologies Used

- **Frontend:** Streamlit
- **Backend:** Python (Flask/Custom API)
- **Database:** MySQL
- **Version Control:** Git, GitHub

---

## Installation and Setup

Follow these steps to set up the project locally:

### Prerequisites
Ensure you have the following installed on your system:
- [Python](https://www.python.org/) (v3.8 or later)
- [MySQL](https://www.mysql.com/)
- [Git](https://git-scm.com/)

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/amanbhati/Railway-Management-System.git
   ```
   Navigate to the project directory:
   ```bash
   cd Railway-Management-System
   ```

2. **Set Up a Virtual Environment**
   Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**
   - Start your MySQL server.
   - Create a new database named `railway_management`.
   - Update the database configuration in the `config.py` file:
     ```python
     DB_HOST = "localhost"
     DB_USER = "your_mysql_username"
     DB_PASSWORD = "your_mysql_password"
     DB_NAME = "railway_management"
     ```

   - Import the database schema:
     ```bash
     mysql -u <username> -p < railway_management.sql
     ```

5. **Run the Application**
   Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```
   The application will be accessible at `http://localhost:8501`.

---

## Usage

1. **Access the System:**
   - Open your browser and navigate to `http://localhost:8501`.

2. **User Operations:**
   - Register or log in to access user functionalities.
   - Book, cancel, or view tickets.

3. **Admin Operations:**
   - Log in as an admin to access the dashboard.
   - Manage train schedules and passenger details.

---

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature description"
   ```
4. Push your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request on GitHub.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact

For any inquiries or support, please contact:

**Aman Kumar Bhati**  
[GitHub Profile](https://github.com/amanbhati)  
Email: amanb9154@gmail.com
