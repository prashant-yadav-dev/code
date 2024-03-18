import re
import sys
from datetime import datetime


class LineInPieces:
    """Class to represent the lines in pieces"""

    def __init__(self):
        self.hours = None
        self.minutes = None
        self.seconds = None
        self.userid = None
        self.action = None
        self.valid = False


class UserSession:
    """Class to represent user session"""

    def __init__(self, userid):
        self.userid = userid
        self.start_time = None
        self.end_time = None


class UserReport:
    """Class to represent user report for eg user,number of sessions and total session time"""

    def __init__(self, userid, number_of_sessions, total_session_time):
        self.userid = userid
        self.number_of_sessions = number_of_sessions
        self.total_session_time = total_session_time


class FairBilling:

    def read_log_file_to_list(self, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                return lines
        except FileNotFoundError:
            raise FileNotFoundError(f"No such file {file_name}")

    def process_valid_lines(self, lines):
        line_in_pieces_list = []
        for line in lines:
            line_in_pieces = self.filter_valid_data(line)
            if line_in_pieces.valid and line_in_pieces.action in ['Start', 'End']:
                line_in_pieces_list.append(line_in_pieces)
            # else:
            #     print(f"Invalid: Log data {line.strip()} - Skipped")
        return line_in_pieces_list

    def create_user_session_map(self, lines):
        user_session_map = {}
        for line in lines:
            if line.userid not in user_session_map:
                user_session_map[line.userid] = []
            user_session_map[line.userid] = self.process_line(line, user_session_map[line.userid])
        return user_session_map

    def process_line(self, line, user_session_list):
        try:
            line_time = datetime.strptime(f"{line.hours}:{line.minutes}:{line.seconds}", '%H:%M:%S').time()
        except BaseException:
            line_time = None
        if line.action == 'Start':
            user_session = UserSession(line.userid)
            user_session.start_time = line_time
            user_session_list.append(user_session)
        elif line.action == 'End':
            for user_session in user_session_list:
                if user_session.end_time is None:
                    user_session.end_time = line_time
                    break
            else:
                user_session = UserSession(line.userid)
                user_session.end_time = line_time
                user_session_list.append(user_session)
        return user_session_list

    def filter_valid_data(self, line):
        line_in_pieces = LineInPieces()
        pattern = re.compile(r'^([01]\d|2[0-3]):([0-5]\d):([0-5]\d) ([A-Z0-9]+) (Start|End)$')
        match = pattern.match(line.strip())
        if match:
            line_in_pieces.hours, line_in_pieces.minutes, line_in_pieces.seconds, line_in_pieces.userid, line_in_pieces.action = match.groups()
            # check for valid user name
            user_name = line_in_pieces.userid
            user_name_pattern = r'(.)\1{2,}'
            if bool(re.search(user_name_pattern, user_name)):
                line_in_pieces.valid = False
            else:
                line_in_pieces.valid = True
        return line_in_pieces

    def process_file_as_list(self, lines):
        pieces_list = self.process_valid_lines(lines)
        # checking for the first time in file
        first_time_in_file = datetime.strptime(f"{pieces_list[0].hours}:{pieces_list[0].minutes}:{
            pieces_list[0].seconds}", '%H:%M:%S').time()
        # checking the last time in the file
        last_time_in_file = datetime.strptime(
            f"{pieces_list[-1].hours}:{pieces_list[-1].minutes}:{pieces_list[-1].seconds}", '%H:%M:%S').time()
        user_session_map = self.create_user_session_map(pieces_list)
        results = []
        for user, sessions in user_session_map.items():
            total = 0
            for session in sessions:
                if session.start_time is None:
                    session.start_time = first_time_in_file
                if session.end_time is None:
                    session.end_time = last_time_in_file
                total += (datetime.combine(datetime.min, session.end_time) -
                          datetime.combine(datetime.min, session.start_time)).total_seconds()
            results.append(UserReport(user, len(sessions), total))
        return results


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print("Wrong number of arguments:", len(sys.argv) - 1)
            print("Syntax is: python fair_billing.py <path to file>")
            sys.exit(1)

        file_name = sys.argv[-1]
        if file_name.split('.')[-1] != 'txt':
            raise ValueError("Invalid file format. Please pass .txt file")
        fair_billing = FairBilling()
        print("=> Reading log file:", file_name)
        lines = fair_billing.read_log_file_to_list(file_name)
        print("=> Processing in progress")
        results = fair_billing.process_file_as_list(lines)
        print("******* User Reports *******")
        for result in results:
            print(f"{result.userid} {result.number_of_sessions} {result.total_session_time}")

    except BaseException as e:
        print("Something went wrong:", e)
