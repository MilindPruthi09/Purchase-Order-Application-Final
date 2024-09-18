# Purchase-Order-Application-Final
<h1>Creating a Purchase Order Application</h1>

Overview
  This project is about building a purchase order application. The process is as follows:
    <ul>1.	First you have to log in.</ul>
    <ul>2.	Then the user is given 2 choices, either to create a new purchase order or edit an existing purchase order. </ul>
    <ul>3.	Then accordingly the user choose one of them and performs that activity.</ul>

<h2>Framework & Technology</h2>
  The framework used here is flask that acts as local server and runs python. Also, in combination to that I have used HTML, CSS to build the front-end UI. For the       functioning of the webpage I have used JavaScript along with AJAX to run python scripts and communicate with the server. For performing various operations like         adding a row or deleting a row, jQuery is used. For storage of data I am using MySQL database. 


<h3>Description of Code Segments</h3>
  1.	app.py – used to run flask web server and also used to connect to database. This file has functions like insertOrder(), editOrNew(), executeQuery() and many more       which perform several database operations and redirect to another web page. It also runs HTML files using render_template.
  2.	login.html – Its an HTML file for creating a login page.
  3.	editOrNew.html – Its an HTML file for choosing either of the options.
  4.	purchaseOrder.html – Its an HTML file for creating a new purchase order page.
  5.	editOrder.html – It’s an HTML file for editing an existing purchase order.
  6.	invoice.css – It is used for styling various webpages.
  7.	edit_Invoice.js – It’s the JS file for editing.
  8.	new_Invoice.js – It’s the JS file for creating a new PO.
  
