# BingBong Airlines - GO2

(Formerly known as "Airline Seat Reservation Project")

(Legally known as "… (WIP)" since we forgott to change it in time)
## Description

- Standard Project: Airline Seat Reservation - ASR 

All information on the project for the proposal draft are directly taken from [here](https://docs.google.com/document/d/1oIJwP78fVMC2WSKWACdJ2SdwL_zk0BxP/edit)

----
## Functionalities

### Data Sources and Retrieval

#### Necessary

- The system takes in Seat Configurations, based on the contents of a text file.
- The system displays a basic seat chart consiting of only letters groped into two equally-sizted groups for left and right, pipe symbols and whiespaces between the grops represent the aisle, eg., A B C | | D E F
- The first row represents the headers for the columns that represent seats; the first column represents the seat rows in the airplane. Every plane has an even number of seats, equally distributed to two sides, so it is easier to identify window, middle, and aisle seats. In the example above, the airplane has three seats on each side. Seats A and F represent window seats, B and E middle seats, C and D aisle seats. [!]
- The system displays a basic seat chart consisting of only letters grouped into two equally-sized groups for left and right, pipe symbols and whitespace between the groups represent the aisle, e.g., A B C | | D E F. [!]
- The system shows available seats by showing the seat letter and occupied seats using X, e.g., X X C | | X E F. [!]


Example:
```
	A	B	C || D	E	F
1	A	B	C || D	E	F
2	A	B	C || D	E	F
3	A	B	C || D	E	F
4	A	B	C || D	E	F
5	A	B	C || D	E	F
6	A	B	C || D	E	F
7	A	B	C || D	E	F
8	A	B	C || D	E	F
9	A	B	C || D	E	F
10	A	B	C || D	E	F
```

#### Optional
- The system supports different seat classes, such as seats in first, business, and economy class and emergency seats. [*]
- The system supports assigning and displaying prices for different seats. [*]
- The system supports arbitrary seat layouts, e.g., A B C    D E F G    H I. For each seat, the system can store and display whether it is a window, middle or aisle seat and where the aisles are. [*]
- Admin users can create seat layouts via a graphical web-based user interface instead of reading them in via a text file. [*]
- First class seat layouts are usually different from Economy and Business class. The system supports different layouts for different classes within one plane. [*]


### Data Storage and Handling

- View Data Sources and Retrival for information about the Plane Seat Configuration Data
- Reservations get stored in a csv file (client, plane, seat id)
- All changes get logged to a logfile (bookings, layout changes...)

### Reserve/cancel seats
- Users can reserve seats and cancel their own, always confirming their actions. [!]
- Users are given an error message if they try to occupy an already reserved seat. [!]
- Admin can cancel any reservation. [!]

### User Management
#### Necessary
- Login using Interface [!] 
- The database should contain at least 4 user accounts with the following information: userID, name, user_name, and password. Only these users are allowed to enter the system. One of the users should have admin privileges in your system (explained later). [!]
- No passwords are found in plain text anywhere throughout the project [!].
- The system offers a logout button. When users click it, the system displays a thank you message and quits after a timeout period. [!]

#### Optional 
- The system offers a separate input for quitting the program, aside from the logout button. [*]
- The system allows users to create and delete accounts via the interface by specifying a username and password. [*]
- The system allows users to create and delete accounts via the interface by specifying an email and password. For account creation and deletion, a confirmation mail is sent to the specified email address. The user needs to confirm receiving the mail, e.g., via a token or clicking a URL. [*]

### Interface

- A CLI Interface for fast development and Admin Users
- A Graphical Interface for Usuall Users & Admins
- Help page on every page of the system (for regular users)

### Statistical Analysis
#### Necessary
- The system offers a statistics area exclusively for admin users. The options in this area or menu should at least include the following statistics that can be saved into a text file [!] 
    - Number and percentage of available seats
    - Number and percentage of reserved seats
    - List of available seats 
    - List of seats that are not available
    - Number of users in the system with their information, except for their password
- Show stats only (and automaticly) to admins [!]

#### Optional
- The system offers the above-mentioned statistics as charts. [*]
- The system offers additional statistics for advanced features, such as seat categories, seat prices, cashflow from seat reservations etc. [*]

### Visualizations

- Data from the analysis get displayed as an image using Matplotlib
- Admins automatically see the visualizations on login. Normal users have no access to the visualizations.
- Display Seat Numbering, Empty Rows (For traversel), Seats taken...

### Help page
- The system offers a help page describing how to use it and all its options [!].
- This help page is available at any step if the project has an interactive UI [!].

### Reserve and Cancel Seats 
- Users can Reserve Seats, Need Confirmation for actions
- Display error message if seat is already occupied
- Admins can cancel reservations
----
### Project Self-Checklist

(Because Markdown Tables are horrible to work with, I'm doing a checklist instead)

- [x] Input Data 
    - [x] Read Data from chartIn.txt
- [x] Login System 
    - [x] Interface for logging in 
    - [x] User accounts with different permissions
    - [x] QoL/Basic Security (Automatic Logoff, no plantext pw)
- [x] Display Seats 
    - [x] Display seat layout 
    - [x] Display seat status 
- [x] Reserve/Cancel Seats 
    - [x] Users can reserve seats and cancel their own 
    - [x] Admin can cancel any reservation 
- [x] Statistics 
    - [x] Viewable
    - [x] Exportable to:
        - [x] Image
        - [x] PDF
- [x] Mandatory Things
    - [x] Project Proposel done 
    - [x] Github init
    - [x] Sensible commit messages, ...
    - [x] Frequent commenting and Docstrings for every function/class 
    - [ ] Testing / Unit Testing 
        - [x] File Parser
        - [x] Statistics
        - [x] Data Structure 
        - [x] CLI
        - [x] Login 
    - [x] Help page 
    - [x] Milestone presentation
    - [x] AI-Usage Card 

----
## Installation and Usage

### Running from source 

1. Make sure to have Matplotlib installed using a method of choice (Manual install using pip or automatic through nix.flake) 
2. Activate env (Depending on step 1.)
3. Navigate into the src/ directory
4. Run ```python -m main -h``` To display the help page 
5. Run ```python -m main <PLANE NAME> <FILE_NAME>``` To start the Programm

### Packaged Version

(Currently unclear if it will work in time for final presentation)
1. Execute the .exe or .deb file through a terminal of choice (Programm is CLI only with the exception of the login page)
2. Done 
----




| Real Name | Name on Github | Contact Adress of Choice |
| -------- | -------- | -------- |
| Paul Stanisch    | Halfdrownedrat     
| Mayada Abdel Rahman     | pythondoda95    |
| Felix Fischer     | FFischerr   |
| Arthur Hirsch     | almostdrownedrat    
| Irem Ebrar  Yalcinkaya  | iremebrar    






