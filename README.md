1.server.py:
          I used flask framework
•	This file is the core of my web application, written in Python using the Flask framework.
•	It defines routes, which are URLs that the application can handle.
•	There are routes for rendering HTML pages, as well as routes for fetching data to be used dynamically in the application.
•	The well() function is a controller that renders the main page of the application (well.html) along with some initial data.
•	I also used pie_chart and bar_chart using chart.js.
•	There's a route for rendering population pages (population_page.html) dynamically based on the year and program parameters.
•	The file listens for incoming requests and responds accordingly, running the Flask application when executed directly.
2. Well.html
•	This is an HTML template that represents the main page of the application.
•	It displays information and potentially interactive elements for users.
•	Data passed from the server-side controller (Well()) is used to customize the content displayed to users.
•	JavaScript code within the HTML file fetches additional data from the server (via the /attendance route) to generate a pie chart dynamically.
3. population_(year)_(program).html:
•	This HTML template is rendered dynamically for each population page based on the specified year and program.
•	It may display information specific to the selected population, such as student lists and course details.
•	Data can be fetched from the server (via routes like /population/(year)/(program)) to populate tables or other content dynamically.
4. course_grade.html:
•	This HTML template represents a page for displaying student grades.
•	It may be rendered dynamically based on the student's email address.
•	The server-side controller for this page (course-grade()) retrieves the student's grade data and passes it to the template for rendering.
Each part of the application plays a specific role in delivering content and functionality to users, from rendering static pages to fetching dynamic data and rendering it dynamically.

