# KFUPM COVID-19 Dashboard (Obsolete)
[Current Project Website](https://dssl-kfupm.github.io/PSM/)

## Introduction
Pandemic surveillance aims at monitoring and detection of infectious diseases outbreak by collecting and analyzing health data related to infected people. Typically, data collection focuses on pre-diagnosis information collected from patients admitted to emergency rooms and urgent care. Such information is insufficient for a full understanding of the dynamics of the disease outbreak. To address this challenge, we will develop a system that will allow collection, analysis, and visualization of infectious pandemic disease data.
## Proposed solution
It is built using Dash, which is a Python framework for building analytical web applications.

## Architecture of project
Figure 1 shows the architecture diagram of COVID-19 Dashboard that has been deployed to the Heroku and Azure. The client communicates with the web hosting server to get the web dashboard over the public network. Inside the private server space, the developer hosts a Gunicorn HTTP server that responds to the web server over a private network. The application is written on Python using tools such as Pandas, Plotly, Dash, and more. The PaaS Cloud Provider will contain the application using tools such as Docker, and then it will host it online. Moreover, the application will communicate daily with MongoDB to update and retrieve the data of database.
![Alt text](./photos/architecture.png?raw=true "main")

## How to run
install the requirements using pip and run app.py. Data.py is used to download, process, and update the data by a schedular in the PaaS provider.

## Photos of dashboard
![Alt text](./photos/main.png?raw=true "main")
![Alt text](./photos/1.png?raw=true "1")
![Alt text](./photos/2.png?raw=true "2")
![Alt text](./photos/3.png?raw=true "3")
![Alt text](./photos/4.png?raw=true "4")
![Alt text](./photos/5.png?raw=true "5")
![Alt text](./photos/6.gif?raw=true "6")
## Tasks
- Data Download Automation (Scheduling) - Done
- Codes Optimization - Done
- UI improvements - Done
- Add sliders for Regions and Cities and embed them using call-back functions. - Done
- Add a table of data - Done
- Develop a PWA for phones - Not feasible

UI Improvements:
- Add a NavBar - Done
- Add the sliders to the DOC - Done
- Add a summary region with x by y px boxes - Done
- Divide the div sections of each graph into 2 graphs with good padding - Done
- Add a footer - Done
- Organize stuff in the dashboard - Done

Future Improvements to consider:
- Add Simulation done by KFUPM@COE COVID19 Team - Done
- Expand to All Saudi Arabia Regions and Cities
- Make UI more rebust, organized, and mobile friendly. - Done
- Update layout to imitate real dashboard design.
- Add Arabic Language Support.
- Improve CSS in the page. - Done
- Optimize Codes. - Done
- Use MongoDB or Postgre instead of csv files. - Done
## License
[MIT](https://choosealicense.com/licenses/mit/)