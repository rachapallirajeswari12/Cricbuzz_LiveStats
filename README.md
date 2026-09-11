\# 🏏 Cricbuzz LiveStats



\## Real-Time Cricket Insights \& SQL-Based Analytics



Cricbuzz LiveStats is a cricket analytics dashboard built using \*\*Python, Streamlit, MySQL, SQL, and Cricbuzz API\*\*.



The application provides real-time cricket match information, player statistics, SQL-based analytics, CRUD operations, and an interactive dashboard for exploring cricket data.



\---



\## 🚀 Live Application



\*\*Streamlit Cloud:\*\*  

https://rachapallirajeswari12-cricbuzz-livestats-main-8gsaij.streamlit.app/



\*\*GitHub Repository:\*\*  

https://github.com/rachapallirajeswari12/Cricbuzz\_LiveStats



\---



\## 📌 Project Overview



The goal of Cricbuzz LiveStats is to build an interactive cricket analytics platform that combines:



\- Real-time cricket data

\- Cricbuzz API integration

\- MySQL database

\- SQL analytics

\- Player statistics

\- Match analytics

\- CRUD operations

\- Streamlit dashboard



The application allows users to monitor live matches and analyze stored cricket data through an easy-to-use web interface.



\---



\## 🛠️ Technologies Used



| Technology | Purpose |

|---|---|

| Python | Application development |

| Streamlit | Interactive dashboard |

| MySQL | Relational database |

| SQL | Data analysis and reporting |

| Cricbuzz API | Live cricket data |

| Pandas | Data processing |

| Requests | API requests |

| BeautifulSoup | Cricket data extraction |

| Git | Version control |

| GitHub | Source code hosting |

| Aiven MySQL | Cloud database |

| Streamlit Cloud | Cloud deployment |



\---



\## ⭐ Key Features



\### 🏠 Dashboard Overview



The dashboard provides an overview of the cricket database including:



\- Total Matches

\- Total Players

\- Total Teams

\- Total Venues

\- Recent Matches



\---



\### 🏏 Live Match Center



The Live Match Center retrieves real-time cricket information and displays:



\- Live match status

\- Teams

\- Current score

\- Overs

\- Run rate

\- Striker

\- Non-striker

\- Current bowler

\- Innings summary

\- Partnership information

\- Commentary

\- Last wicket

\- Recent overs



\---



\### 📋 Recent Matches



Displays recently stored cricket matches from the MySQL database.



\---



\### 💬 Commentary



Displays live cricket commentary retrieved from the Cricbuzz data source.



\---



\### 📊 Innings Summary



Provides innings-level information including:



\- Batting team

\- Score

\- Overs

\- Declared status

\- Follow-on status



\---



\### 🎯 Bowling Analytics



Displays current bowling information including:



\- Bowler

\- Overs

\- Runs

\- Wickets

\- Economy information



\---



\### 📈 Cricket Analytics



Provides visual analytics for:



\- Current run rate

\- Partnerships

\- Innings scores

\- Batsman performance

\- Match statistics



\---



\### 👤 Top Player Stats



Provides player-level performance analytics such as:



\- Top run scorers

\- Highest individual scores

\- Top wicket takers

\- Bowling performance

\- Player averages



\---



\## 🛠️ CRUD Operations



The application supports full CRUD operations for the `players` table.



\### Create



Add a new player with:



\- Full Name

\- Role

\- National Team

\- Batting Style

\- Bowling Style

\- API Player ID

\- Active Status



\### Read



View all players stored in the database.



\### Update



Modify existing player information.



\### Delete



Remove a player from the database.



\---



\## 📚 SQL Analytics



The project contains \*\*25 SQL analytics queries\*\* covering different cricket data analysis requirements.



The queries include:



1\. All Players

2\. Active Players

3\. Players by Role

4\. Players by National Team

5\. Team List

6\. Venue List

7\. Match List

8\. Completed Matches

9\. Live Matches

10\. Matches by Format

11\. Matches by Venue

12\. Matches by Year

13\. Top Run Scorers

14\. Highest Individual Scores

15\. Top Wicket Takers

16\. Bowling Economy

17\. All-Round Players

18\. Match Winners

19\. Toss Winners

20\. Toss Winner Also Won Match

21\. Close Matches

22\. Partnerships

23\. Head-to-Head Matches

24\. Player Batting Consistency

25\. Recent Player Form



\---



\## 🗄️ Database



The project uses MySQL as the primary relational database.



\### Database Name



`cricbuzz\_livestats`



\### Main Tables



The database contains 15 tables:



\- countries

\- formats

\- roles

\- teams

\- players

\- venues

\- series

\- matches

\- match\_teams

\- innings

\- batting\_performance

\- bowling\_performance

\- fielding\_performance

\- partnerships

\- commentary



\---



\## 🔗 API Integration



The application integrates cricket data through Cricbuzz-related endpoints.



The API is used to retrieve information such as:



\- Live matches

\- Match scores

\- Commentary

\- Batsmen

\- Bowlers

\- Innings information

\- Recent overs



API credentials and database passwords are stored securely using environment variables and Streamlit Secrets.



Sensitive credentials are not stored in the GitHub repository.



\---



\## ☁️ Cloud Architecture



The deployed application uses:



```text

User

&#x20; |

&#x20; v

Streamlit Cloud

&#x20; |

&#x20; +----> Cricbuzz API

&#x20; |

&#x20; +----> Aiven Cloud MySQL

&#x20; |

&#x20; v

Cricket Analytics Dashboard

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │        User         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Streamlit Dashboard │
                    │       main.py       │
                    └────────┬─────┬──────┘
                             │     │
                 ┌───────────┘     └────────────┐
                 ▼                              ▼
        ┌──────────────────┐          ┌──────────────────┐
        │   Cricbuzz API   │          │   MySQL Database │
        │                  │          │                  │
        │ Live Scores      │          │ 15 Relational   │
        │ Commentary       │          │ Tables           │
        │ Match Data       │          │ Cricket Data     │
        └──────────────────┘          └────────┬─────────┘
                                               │
                                               ▼
                                  ┌────────────────────────┐
                                  │ SQL Analytics           │
                                  │ CRUD Operations         │
                                  │ Player Statistics       │
                                  │ Match Analytics         │
                                  └────────────────────────┘