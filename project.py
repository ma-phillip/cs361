import os
from datetime import datetime
from datetime import timedelta

class GuineaPig:
    def __init__(self, name, weight, sex):
        self.name = name
        self.weight = weight
        self.sex = sex

class WaterTracker:
    def __init__(self, log_file):
        self.log_file = log_file
        self.last_refill = None
        self.previous_refills = []
        self.load_logs()

    def load_logs(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    self.previous_refills.append(datetime.strptime(line.strip(), '%m/%d/%Y'))
                if len(lines) > 0:
                    self.last_refill = datetime.strptime(lines[-1].strip(), '%m/%d/%Y')

    def save_logs(self):
        with open(self.log_file, 'w') as f:
            for refill in self.previous_refills:
                f.write(refill.strftime('%m/%d/%Y') + '\n')

    def log_refill(self, date):
        with open(self.log_file, 'a') as f:
            f.write(date.strftime('%m/%d/%Y') + '\n')
        self.last_refill = date
        self.previous_refills.append(date)

    def view_logs(self):
        for refill in self.previous_refills:
            print(refill.strftime('%m/%d/%Y'))

    def estimate_next_refill(self):
        if len(self.previous_refills) >= 2:
            total_days_between_refills = 0
            num_intervals = len(self.previous_refills) - 1

            for i in range(num_intervals):
                days_between_refills = (self.previous_refills[i + 1] - self.previous_refills[i]).days
                total_days_between_refills += days_between_refills

            average_days_between_refills = total_days_between_refills / num_intervals
            next_refill_date = self.last_refill + timedelta(days=average_days_between_refills)
            print("The next estimated refill date is:", next_refill_date.strftime('%m/%d/%Y'), "\n")
        else:
            print("Not enough previous logs to estimate next refill date.")


def create_guinea_pig():
    name = input("Please enter the name of your guinea pig: ")
    weight = input("Please enter the weight of your guinea pig: ")
    sex = input("Please enter the sex of your guinea pig: ")
    return GuineaPig(name, weight, sex)


def create_multiple_guinea_pigs():
    num_guinea_pigs = int(input("How many guinea pigs would you like to create? "))
    guinea_pigs = []
    for i in range(num_guinea_pigs):
        guinea_pigs.append(create_guinea_pig())
    return guinea_pigs


def water_tracking_ui(water_tracker):
    while True:
        print("The last logged water refill was on", water_tracker.last_refill.strftime('%m/%d/%Y'))
        choice = input(
            "What would you like to do?\n1. Log today's date as a refill\n2. View all previous logs\n3. Estimate next refill date\n4. Go home\n")

        if choice == '1':
            water_tracker.log_refill(datetime.now())
            print("Refill logged successfully.")
        elif choice == '2':
            water_tracker.view_logs()
        elif choice == '3':
            if len(water_tracker.previous_refills) >= 2:
                water_tracker.estimate_next_refill()
            else:
                print("Not enough previous logs to estimate next refill date.")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please choose again.")


def main():
    water_tracker = WaterTracker('water_logs.txt')
    while True:
        print("What would you like to do?")
        print("1. Create 1 guinea pig (This allows you create and track a single guinea pig)")
        print("2. Create Multiple guinea pigs (If you have more than one guinea pig you would like to track, use this!")
        print("3. Water tracking (This allows you to track guinea pig water consumption")
        print("4. Exit (Close the application)")
        choice = input()

        if choice == '1':
            guinea_pig = create_guinea_pig()
            print("Guinea pig created successfully.")
        elif choice == '2':
            guinea_pigs = create_multiple_guinea_pigs()
            print(len(guinea_pigs), "guinea pigs created successfully.")
        elif choice == '3':
            water_tracking_ui(water_tracker)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please choose again.")

if __name__ == '__main__':
    main()

