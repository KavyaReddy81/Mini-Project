import time
import datetime

class Patient:
    def __init__(self, patient_id, name, age, complaint, priority):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.complaint = complaint
        self.priority = priority
        self.arrival_time = time.time()
        self.arrival_str = datetime.datetime.now().strftime("%H:%M:%S")

    def __str__(self):
        label = {1: "Critical", 2: "Urgent", 3: "Less Urgent", 4: "Non-Urgent"}
        return (f"[P{self.priority}-{label[self.priority]}] "
                f"ID:{self.patient_id} | {self.name}, Age:{self.age} | {self.complaint} | Arrived:{self.arrival_str}")

    def __lt__(self, other):
        if self.priority != other.priority:
            return self.priority < other.priority
        return self.arrival_time < other.arrival_time

    def __eq__(self, other):
        return self.priority == other.priority and self.arrival_time == other.arrival_time

class MinHeap:
    def __init__(self):
        self._heap = []

    def insert(self, patient):
        self._heap.append(patient)
        self._bubble_up(len(self._heap) - 1)

    def extract_min(self):
        if not self._heap:
            return None
        self._swap(0, len(self._heap) - 1)
        patient = self._heap.pop()
        if self._heap:
            self._sink_down(0)
        return patient

    def peek(self):
        return self._heap[0] if self._heap else None

    def size(self):
        return len(self._heap)

    def is_empty(self):
        return not self._heap

    def display(self):
        if not self._heap:
            print("  Queue is empty.")
            return
        temp = MinHeap()
        temp._heap = self._heap[:]
        rank = 1
        while not temp.is_empty():
            p = temp.extract_min()
            marker = " <-- NEXT" if rank == 1 else ""
            print(f"  {rank}. {p}{marker}")
            rank += 1

    def _bubble_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self._heap[i] < self._heap[parent]:
                self._swap(i, parent)
                i = parent
            else:
                break

    def _sink_down(self, i):
        n = len(self._heap)
        while True:
            smallest = i
            left = 2 * i + 1
            right = 2 * i + 2
            if left < n and self._heap[left] < self._heap[smallest]:
                smallest = left
            if right < n and self._heap[right] < self._heap[smallest]:
                smallest = right
            if smallest != i:
                self._swap(i, smallest)
                i = smallest
            else:
                break

    def _swap(self, i, j):
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

class EmergencyRoom:
    PRIORITY_LABELS = {1: "Critical", 2: "Urgent", 3: "Less Urgent", 4: "Non-Urgent"}

    def __init__(self):
        self.queue = MinHeap()
        self._next_id = 1
        self.treated = []
        self.total_wait_sec = 0

    def admit(self, name, age, complaint, priority):
        if priority not in range(1, 5):
            print("  Invalid priority. Choose 1 (Critical) to 4 (Non-Urgent).")
            return
        patient = Patient(self._next_id, name, age, complaint, priority)
        self._next_id += 1
        self.queue.insert(patient)
        print(f"\n  ? Patient admitted: {patient}")

    def treat_next(self):
        patient = self.queue.extract_min()
        if patient is None:
            print("\n  Queue is empty. No patients to treat.")
            return
        wait_sec = time.time() - patient.arrival_time
        self.total_wait_sec += wait_sec
        self.treated.append((patient, wait_sec))
        print(f"\n  ? Now treating: {patient}")
        print(f"     Wait time: {self._fmt_wait(wait_sec)}")

    def show_queue(self):
        print(f"\n  --- Queue ({self.queue.size()} patients) ---")
        self.queue.display()

    def show_stats(self):
        n = len(self.treated)
        avg = self.total_wait_sec / n if n else 0
        print("\n  --- Statistics ---")
        print(f"  Patients waiting : {self.queue.size()}")
        print(f"  Patients treated : {n}")
        print(f"  Avg wait time    : {self._fmt_wait(avg)}")
        if self.treated:
            print("\n  Treated list:")
            for p, w in self.treated:
                print(f"    - {p.name} ({self.PRIORITY_LABELS[p.priority]}) | waited {self._fmt_wait(w)}")

    @staticmethod
    def _fmt_wait(sec):
        m = int(sec // 60)
        s = int(sec % 60)
        return f"{m}m {s}s" if m else f"{s}s"

def print_menu():
    print("\n" + "=" * 50)
    print("  HOSPITAL EMERGENCY QUEUE MANAGEMENT")
    print("=" * 50)
    print("  1. Admit new patient")
    print("  2. Treat next patient (extract min)")
    print("  3. View current queue")
    print("  4. Peek at next patient")
    print("  5. Show statistics")
    print("  6. Exit")
    print("=" * 50)

def get_priority():
    print("\n  Triage Levels:")
    print("    1 - Critical   (life-threatening, immediate)")
    print("    2 - Urgent     (could deteriorate rapidly)")
    print("    3 - Less Urgent(stable, needs care)")
    print("    4 - Non-Urgent (minor, can wait)")
    while True:
        try:
            p = int(input("  Enter priority (1-4): "))
            if 1 <= p <= 4:
                return p
            print("  Please enter a number between 1 and 4.")
        except ValueError:
            print("  Invalid input.")

def main():
    er = EmergencyRoom()
    while True:
        print_menu()
        choice = input("  Select option: ").strip()
        if choice == "1":
            print("\n  -- Admit New Patient --")
            name = input("  Name      : ").strip()
            age_str = input("  Age       : ").strip()
            complaint = input("  Complaint : ").strip()
            age = int(age_str) if age_str.isdigit() else 0
            priority = get_priority()
            er.admit(name, age, complaint, priority)
        elif choice == "2":
            er.treat_next()
        elif choice == "3":
            er.show_queue()
        elif choice == "4":
            next_p = er.queue.peek()
            if next_p:
                print(f"\n  Next patient ? {next_p}")
            else:
                print("\n  Queue is empty.")
        elif choice == "5":
            er.show_stats()
        elif choice == "6":
            print("\n  Exiting. Stay safe!\n")
            break
        else:
            print("\n  Invalid option. Try again.")

if __name__ == "__main__":
    main()
