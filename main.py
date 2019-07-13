# set the input files
input_file_name = 'inputPS4.txt'
prompts_file_name = 'promptsPS4.txt'

# output file to be written to
output_file = 'outputPS4.txt'

# According to the problem statement, courses were offered from 2008 till 2018
# Considering 2018 as the current year
current_year = 2018

""" 
Class for the Hashtable 

The class takes care of maintenance of hashtable and hash function
The insertion, retrieval and retrieval of keys are supported
Hash function uses, basic arithmetic operations and uses Linear 
probing for collisions
Resize of the hashtable is also done when the load reaches 75%

"""


class HashTable:
    # size of the hashtable
    size = 0

    # occupancy in the hashtable
    occupancy = 0

    # hash table
    hashTable = [[]]

    # init method to set the size of the hash table
    def __init__(self, size):
        self.size = size
        self.hashTable = [[None]] * size

    # Method to return the index of hash table when a student id/key is passed
    def hashid(self, key):
        year = key[:4]
        dept = key[4:7]
        just_id = key[7:]
        # The formula used is
        # (YYYY + weighted values of dept characters + id) % size
        # Weighted value of dept characters is for dept CSE ,
        # value = C^3 + S^2 + E^1
        index = (int(year)
                 + int(ord(dept[0])) * int(ord(dept[0])) * int(ord(dept[0]))
                 + int(ord(dept[1])) * int(ord(dept[1])) + int(ord(dept[2]))
                 + int(just_id))
        return index % self.size

    # Method to insert a record into the hash table
    # Uses linear probing to handle collisions
    # Resize when the load is greater than 75%
    def insert(self, key, value):

        # Resize when the load is high
        if self.load() > 0.75:
            self.resize()
        hash_id = self.hashid(key)

        # Using linear probing
        if self.hashTable[hash_id][0] is None:
            self.hashTable[hash_id] = (key, value)
        else:
            while self.hashTable[hash_id][0] is not None:
                hash_id = (hash_id + 1) % self.size
                continue
            self.hashTable[hash_id] = (key, value)
        self.occupancy = self.occupancy + 1

    # Method to get the value of a key from the hash table
    def get(self, key):
        hash_id = self.hashid(key)
        n = self.size

        # if the value is not available at the hash_id, then probe linearly
        while (
                n > 0 and self.hashTable[hash_id] is not None
                and self.hashTable[hash_id][0] != key
        ):
            hash_id = (hash_id + 1) % self.size
            n = n - 1
            continue
        # if n is not zero, then we found the key and value
        if n != 0:
            return self.hashTable[hash_id][1]
        return None

    # Method to get all the keys stored in the hashtable
    def getKeys(self):
        keys = []
        n = 0
        while n < self.size:
            if self.hashTable[n][0] is not None:
                keys.append(self.hashTable[n][0])
            n = n + 1
        return keys

    # Method to find out the load of the hashtable
    def load(self):
        return self.occupancy / self.size

    # Method to resize the hashtable to double its size
    def resize(self):
        # create new hashtable
        newSize = self.size * 2
        newHashTable = [[None]] * newSize

        # copy the contents from existing hashtable to new hashtable
        i = 0
        while i < self.size:
            newHashTable[i] = self.hashTable[i]
            i = i + 1

        # delete existing hashtable
        del self.hashTable[:]
        del self.hashTable

        # use new hashtable
        self.size = newSize
        self.hashTable = newHashTable


# Initialize the hash table
def initializeHash(StudentHashRecords):
    # refer _init_ for the initialization code
    StudentHashRecords = HashTable(1000)


# Insert the student_id and CGPA into the StudentHashRecords hashtable
def insertStudentRec(StudentHashRecords, student_id, CGPA):
    # refer HashTable insert() method for the insertion
    StudentHashRecords.insert(student_id, float(CGPA))


# Print the hall of fame students whose CGPA is greater the specified CGPA
def hallOfFame(StudentHashRecords, CGPA):
    hof_students = []

    # get CGPA for each key and filter students based on the CGPA
    for each_student_id in StudentHashRecords.getKeys():
        if (StudentHashRecords.get(each_student_id) >= CGPA):
            hof_students.append((each_student_id,
                                 StudentHashRecords.get(each_student_id)))

    # print the hall of fame students
    with open(output_file, 'w+') as of:
        of.write('---------- hall of fame ----------\n')
        of.write('Input: %s\n' % str(CGPA))
        of.write('Total eligible students: %d\n' % len(hof_students))
        of.write('Qualified students:\n')
        for each_hof_student in hof_students:
            hof_student_id = each_hof_student[0]
            hof_cgpa = each_hof_student[1]
            of.write('%s / %s\n' % (hof_student_id, str(hof_cgpa)))
        of.write('\n')


# Print the eligible students for a new course whose CGPA is between the range
def newCourseList(StudentHashRecords, CGPAFrom, CPGATo):
    qualified_students = []
    # get the qualified students based on their CGPA
    for each_student_id in StudentHashRecords.getKeys():
        if (
                (int(each_student_id[:4]) + 4) >= (current_year - 5) and
                StudentHashRecords.get(each_student_id) >= CGPAFrom and
                StudentHashRecords.get(each_student_id) <= CPGATo
        ):
            qualified_students.append((each_student_id,
                                       StudentHashRecords.get(each_student_id)))

    # print the qualified students
    with open(output_file, 'a+') as of:
        of.write('---------- new course candidates ----------\n')
        of.write('Input: %s to %s\n' % (str(CGPAFrom), str(CPGATo)))
        of.write('Total eligible students: %d\n' % len(qualified_students))
        of.write('Qualified students:\n')
        for qualified_student in qualified_students:
            qual_student_id = qualified_student[0]
            qual_cgpa = qualified_student[1]
            of.write('%s / %s\n' % (qual_student_id, str(qual_cgpa)))
        of.write('\n')


# Calculate and print the average and maximum for each department
def depAvg(StudentHashRecords):
    cse_count, mec_count, ece_count, arc_count = 0, 0, 0, 0
    cse_max, mec_max, ece_max, arc_max = 0, 0, 0, 0
    cse_sum, mec_sum, ece_sum, arc_sum = 0, 0, 0, 0
    cse_avg, mec_avg, ece_avg, arc_avg = 0, 0, 0, 0

    # loop over the students to count and get the cgpas of students
    # based on their departments
    for each_student_id in StudentHashRecords.getKeys():
        department = each_student_id[4:7]
        cgpa = StudentHashRecords.get(each_student_id)
        if department == 'CSE':
            cse_count += 1
            cse_sum += cgpa
            if cgpa > cse_max:
                cse_max = cgpa
        elif department == 'MEC':
            mec_count += 1
            mec_sum += cgpa
            if cgpa > mec_max:
                mec_max = cgpa
        elif department == 'ECE':
            ece_count += 1
            ece_sum += cgpa
            if cgpa > ece_max:
                ece_max = cgpa
        elif department == 'ARC':
            arc_count += 1
            arc_sum += cgpa
            if cgpa > arc_max:
                arc_max = cgpa

    # average_values
    cse_avg = cse_sum / cse_count if cse_count != 0 else 0
    mec_avg = mec_sum / mec_count if mec_count != 0 else 0
    ece_avg = ece_sum / ece_count if ece_count != 0 else 0
    arc_avg = arc_sum / arc_count if arc_count != 0 else 0
    # CSE: max: 3.5, avg: 3.4

    # print the max and averages for each department
    with open(output_file, 'a+') as of:
        of.write('---------- department CGPA ----------\n')
        of.write('CSE: max: %s, avg: %s\n' %
                 (str(cse_max), str(round(cse_avg, 2))))
        of.write('MEC: max: %s, avg: %s\n' % (str(mec_max), str(mec_avg)))
        of.write('ECE: max: %s, avg: %s\n' % (str(ece_max), str(ece_avg)))
        of.write('ARC: max: %s, avg: %s\n' % (str(arc_max), str(arc_avg)))


def main():
    StudentHashRecords = HashTable(1000)
    initializeHash(StudentHashRecords)
    # insert students records
    with open(input_file_name, 'r') as input_file:
        records = input_file.readlines()
        for each_record in records:

            # validate the input
            if not each_record.strip():
                print("Empty line found, ignoring the line")
                continue

            if(len(each_record.split('/')) < 2):
                print("The input format is not correct, ignoring the record:")
                print(each_record)
                continue

            student_id = each_record.split('/')[0].strip() # Getting student ID
            cgpa = each_record.split('/')[1].strip()  # Getting student CGPA

            # validate the input
            if not student_id or not cgpa:
                print("The input format is not correct, ignoring the record:")
                print(each_record)
                continue

            insertStudentRec(StudentHashRecords, student_id, cgpa)

    with open(prompts_file_name, 'r') as input_file:
        records = input_file.readlines()
        for each_record in records:

            # validate the input
            if not each_record.strip():
                print("Empty line found, ignoring the line")
                continue

            header = each_record.split(':')[0].strip()

            # get Hall Of Fame records
            if header == 'hallOfFame':

                # validate the input
                if(len(each_record.split(':')) < 2):
                    print("The input format is not correct, ignoring the record:")
                    print(each_record)
                    continue
                
                cutoff_cgpa = each_record.split(':')[1].strip()

                # validate the input
                if not cutoff_cgpa:
                    print("The input format is not correct, ignoring the record:")
                    print(each_record)
                    continue

                cutoff_cgpa = float(cutoff_cgpa)
                hallOfFame(StudentHashRecords, cutoff_cgpa)
            # get Course Offer records
            elif header == 'courseOffer':

                # validate the input
                if(len(each_record.split(':')) < 3):
                    print("The input format is not correct, ignoring the record:")
                    print(each_record)
                    continue
                
                cgpa_ranges = each_record.split(':')[1:]
                cgpa_from = float(cgpa_ranges[0].strip())
                cgpa_to = float(cgpa_ranges[1].strip())
                newCourseList(StudentHashRecords, cgpa_from, cgpa_to)
            else:
                print("specify either hallOfFame or courseOffer")

    depAvg(StudentHashRecords)
    print('Completed Operations!, Kindly visit %s for the output' % output_file)


if __name__ == "__main__":
    main()
