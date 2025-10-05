ShiftSync - Employee Shift Scheduling & Time-Off Portal

A full-stack web application for managing employee shifts and time-off requests with role-based access control.

🌟 Features
👥 For All Users
JWT Authentication - Secure login/signup system

Role-Based Access Control - Different permissions for managers and employees

Responsive Dashboard - Overview of shifts and time-off requests

👨‍💼 Manager Features
Shift Management - Create, edit, and delete employee shifts

Conflict Detection - Automatic shift conflict checking

Team Scheduling - View and manage all employee schedules

Time-Off Approvals - Approve or deny employee time-off requests

Employee Management - View employee list for shift assignment

👩‍💼 Employee Features
Personal Schedule - View assigned shifts in calendar format

Time-Off Requests - Submit and track time-off requests

Shift Overview - See upcoming shifts and request history

🛠 Tech Stack
Backend
Flask - Python web framework

PostgreSQL - Database

Flask-SQLAlchemy - ORM

Flask-JWT-Extended - Authentication

Flask-Migrate - Database migrations

Flask-CORS - Cross-origin resource sharing

Frontend
React - Frontend framework

React Router - Client-side routing

Context API - State management

React Big Calendar - Schedule visualization

Axios - HTTP client

🚀 Quick Start
Prerequisites
Python 3.8+

Node.js 16+

PostgreSQL 12+

Backend Setup
Clone and setup backend

bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
Configure environment

bash
cp .env.example .env
# Edit .env with your database credentials and JWT secret
Initialize database

bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
Create manager account

bash
flask shell
>>> from create_manager import create_manager
>>> create_manager('admin', 'admin@example.com', 'securepassword')
Start backend server

bash
flask run
# Server runs on http://localhost:5000
Frontend Setup
Install dependencies

bash
cd frontend
npm install
Start development server

bash
npm start
# App runs on http://localhost:3000
📁 Project Structure
text
shiftsync/
├── backend/
│   ├── app.py                 # Flask application factory
│   ├── config.py              # Configuration settings
│   ├── models.py              # SQLAlchemy models
│   ├── routes/                # API routes
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── shifts.py         # Shift management
│   │   ├── timeoff.py        # Time-off requests
│   │   ├── users.py          # User management
│   │   └── schedules.py      # Schedule views
│   ├── utils.py              # Decorators and utilities
│   └── extensions.py         # Flask extensions
└── frontend/
    ├── src/
    │   ├── components/       # React components
    │   ├── context/          # React context (Auth)
    │   ├── services/         # API service layer
    │   └── App.js           # Main app component
🔐 API Endpoints
Authentication
POST /api/auth/signup - Create new account

POST /api/auth/login - User login

POST /api/auth/refresh - Refresh JWT token

Shifts
GET /api/shifts/ - Get shifts (all for managers, own for employees)

POST /api/shifts/ - Create new shift (manager only)

PUT /api/shifts/<id> - Update shift (manager only)

DELETE /api/shifts/<id> - Delete shift (manager only)

Time-Off
GET /api/timeoff/ - Get time-off requests

POST /api/timeoff/ - Create time-off request

PUT /api/timeoff/<id>/status - Update request status (manager only)

Users & Schedules
GET /api/users/ - Get user list (manager only)

GET /api/schedules/<week_start> - Get weekly schedule

👥 User Roles
Manager
Full access to all features

Can manage all employee shifts

Can approve/deny time-off requests

Can view all schedules

Employee
View own shifts only

Request time off

View personal schedule

🗓️ Shift Conflict Detection
The application automatically detects and prevents:

Overlapping shifts for the same employee

Shifts that end before they start

Time-off requests that conflict with existing shifts

🔧 Configuration
Environment Variables (Backend)
bash
DATABASE_URL=postgresql://user:pass@localhost:5432/shiftdb
JWT_SECRET_KEY=your-super-secret-key-here
FLASK_ENV=development
Frontend Configuration
Create .env in frontend directory:

bash
REACT_APP_API_URL=http://localhost:5000
🐛 Troubleshooting
Common Issues
CORS Errors

Ensure backend CORS is configured for frontend URL

Check that all endpoints return proper CORS headers

Database Connection

Verify PostgreSQL is running

Check DATABASE_URL in .env file

Run flask db upgrade after schema changes

Authentication Issues

Verify JWT_SECRET_KEY is set

Check token expiration settings

Ensure Authorization header is included in requests

Development Tips
Use Flask shell for database debugging: flask shell

Check browser Network tab for API request/response details

Enable debug mode for detailed error messages

📝 License
This project is licensed under the MIT License.

🤝 Contributing
Fork the repository

Create a feature branch

Commit your changes

Push to the branch

Create a Pull Request

🆘 Support
For support and questions:

Check the troubleshooting section above

Review API documentation in the code

Create an issue in the repository

ShiftSync - Streamlining workforce management, one shift at a time.
