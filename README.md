# Fair Billing

Fair Billing is a Python program designed to analyze log files containing user session data and calculate information based on the duration of user sessions.

### Features

- Log File Processing: Reads log files containing user session data.
- Session Calculation: Calculates the duration of each user session.
- Fair Billing: Generates fair billing information for each user based on their session durations.
- Error Handling: Handles errors gracefully, including file not found and invalid log data.

### Usage

1.Installation:

    - Clone this repository to your local machine or extract the zip file.
  ```git clone https://github.com/prashant-yadav-dev/code.git```
    
    - Make sure you have Python 3 installed.

2.Run the Program:

- Navigate to the directory containing the Fair Billing program.
- Run the program by executing the following command in your terminal:

```shell
  python fair_billing.py 'samplelog.txt'
```

- Replace log.txt with the path to your log file.

  3.View Results:

- The program will process the log file and print the fair billing information for each user to the console.

### Input Format

The input log file should contain lines in the following format:
14:02:03 ALICE99 Start
14:02:05 CHARLIE End
14:02:34 ALICE99 End
14:02:58 ALICE99 Start
14:03:02 CHARLIE Start
14:03:33 ALICE99 Start

### Output Format

USERNAME NUMBER_OF_SESSIONS TOTAL_SESSION_TIME
USERNAME: Unique identifier for the user.
NUMBER_OF_SESSIONS: The total number of sessions for the user.
TOTAL_SESSION_TIME: The total duration of all sessions for the user in seconds.

Sample Output:

```python
ALICE99 4 240
CHARLIE 3 37
```
