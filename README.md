# Campus Solutions

Campus Solutions

Campus Solutions is a web application designed to provide students and faculty with a seamless experience for managing academic activities. It offers features like attendance tracking, assignment submission, academic resource sharing, and interactive communication between students and faculty through a chatbot.
Features

1. Student Dashboard

   Attendance: Students can view their attendance and track their progress over time.
   Assignments: Students can submit assignments online, making the process simpler and more efficient.
   Academic Resources: Students can download academic resources such as previous years' question papers and notes.
   Book Marketplace: A feature for students to buy/sell books and notes.

2. Faculty Dashboard

   Attendance Management: Faculty can mark student attendance for each class and monitor students' attendance trends.
   Assignments: Faculty can manage assignments and track student submissions and grades.
   Exam Results: Faculty can enter and update exam results for students.
   Coursework Management: Teachers can manage course content and assignments with ease.

3. Chatbot for Student-Faculty Interaction

   A chatbot enables real-time communication between students and faculty, answering queries and facilitating interaction.

4. Upload Previous Year Question Papers (PYQs)

   Faculty and students can upload, view, and download previous year question papers, notes, and other academic materials.
   An intuitive interface allows users to upload files with details like name, semester, and session.

Technologies Used

    Frontend:
        HTML, CSS, EJS for rendering dynamic content (Django Templating)
        Bootstrap for responsive design and styling
    Backend:
        Django (Python web framework)
        Django ORM for database management
    Database:
        MongoDB (for storing student and faculty-related data)
        Django models to handle data and interactions
    Chatbot:
        Custom AI-powered chatbot for student-faculty communication (in development)

Installation Guide
Prerequisites

    Python 3.8+ installed on your system.
    Django framework installed.
    MongoDB for storing database entries.

Steps to Run Locally

    Clone the Repository:

git clone https://github.com/your-username/campus-solutions.git
cd campus-solutions

Install Dependencies: It’s recommended to create a virtual environment to keep your dependencies isolated.

python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt

Setup Database:

    Ensure MongoDB is running locally.
    Set up your Django settings to connect to the MongoDB database.

Migrate the Database:

python manage.py migrate

Create Superuser (for admin panel):

python manage.py createsuperuser

Run the Development Server:

    python manage.py runserver

    Your application should now be live at http://127.0.0.1:8000/.

Project Structure

campus-solutions/
├── manage.py # Django manage script
├── campus_solutions/ # Main app directory
│ ├── **init**.py
│ ├── settings.py # Django settings
│ ├── urls.py # URL routing for the application
│ ├── models.py # Database models for the application
│ ├── forms.py # Form handling
│ ├── views.py # Views and logic for handling requests
│ ├── templates/ # Template files for rendering HTML
│ └── static/ # Static files (CSS, JS, Images)
└── requirements.txt # Python package dependencies

Features in Development

    Chatbot Integration: We are working on integrating a chatbot feature to facilitate real-time interaction between students and faculty.
    Attendance Analytics: Additional tools to analyze attendance patterns for students and faculty.
    User Roles and Permissions: Further development of role-based access control (e.g., admin, student, faculty).

Future Enhancements

    Notification System: Push notifications to alert students and faculty about new assignments, attendance updates, and important announcements.
    Advanced Search: A search system for filtering assignments, resources, and attendance by subject, semester, and date range.
    Mobile Application: Develop a mobile application for easier access and use.

Contributing

We welcome contributions to this project! If you'd like to contribute, please follow these steps:

    Fork the repository.
    Create a new branch for your feature or bugfix.
    Make your changes and commit them.
    Push your branch to your forked repository.
    Open a pull request with a detailed description of your changes.

License

This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgements

    Bootstrap for the frontend styling.
    Django for the powerful and efficient web framework.
    MongoDB for the scalable database solution.
