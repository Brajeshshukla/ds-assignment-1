"""
ASSUMPTIONS:
1. from promptsPS4.txt file, the data for course to offer is --> courseOffer: 3.5 : 4:0
but considered it as --> courseOffer: 3.5 : 4.0
2. New Course List considering the Current year as 2014
"""

hash_array = None
hash_size = 20
input_file_name = 'inputPS4.txt'
prompts_file_name = 'promptsPS4.txt'
output_file = 'outputPS4.txt'
current_year = 2014


def initializeHash():
    """
    Initialize the hash
    """
    global hash_array
    hash_array = [None] * hash_size

def hashId(student_id):
    year = student_id[:4]
    dept = student_id[4]
    just_id=student_id[7:]
    index = (int(year) + int(ord(dept)) + int(just_id))%hash_size
    return index % hash_size
    


def insertStudentRec(StudentHashRecords, student_id, CGPA):
    hash_id = hashId(student_id)
    # Using linear probing
    if StudentHashRecords[hash_id] == None:
        StudentHashRecords[hash_id] = (student_id,float(CGPA))
    else:
        while StudentHashRecords[hash_id] != None:
            hash_id = (hash_id+1) %hash_size
            continue
        StudentHashRecords[hash_id] = (student_id,float(CGPA))


def hallOfFame(StudentHashRecords, CGPA):

    hof_students = [data for data in StudentHashRecords if data is not None and data[1] >= CGPA]
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


def newCourseList(StudentHashRecords, CGPAFrom, CPGATo):
    eligible_students = [data for data in StudentHashRecords \
                         if data is not None and (int(data[0][:4]) + 4) >= (current_year - 5)]

    qualified_students = [data for data in eligible_students \
                          if (data[1] >= CGPAFrom and data[1] <= CPGATo)]
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


def depAvg(StudentHashRecords):
    cse_count, mec_count, ece_count, arc_count = 0, 0, 0, 0
    cse_max, mec_max, ece_max, arc_max = 0, 0, 0, 0
    cse_sum, mec_sum, ece_sum, arc_sum = 0, 0, 0, 0
    cse_avg, mec_avg, ece_avg, arc_avg = 0, 0, 0, 0
    temp_records = [record for record in StudentHashRecords if record is not None]
    for student_id, cgpa in temp_records:        
        department = student_id[4:7]
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
    cse_avg = cse_sum / cse_count if cse_count !=0 else 0
    mec_avg = mec_sum / mec_count if mec_count !=0 else 0
    ece_avg = ece_sum / ece_count if ece_count !=0 else 0
    arc_avg = arc_sum / arc_count if arc_count !=0 else 0
    # CSE: max: 3.5, avg: 3.4
    with open(output_file, 'a+') as of:
        of.write('---------- department CGPA ----------\n')
        of.write('CSE: max: %s, avg: %s\n' % (str(cse_max), str(round(cse_avg,2))))
        of.write('MEC: max: %s, avg: %s\n' % (str(mec_max), str(mec_avg)))
        of.write('ECE: max: %s, avg: %s\n' % (str(ece_max), str(ece_avg)))
        of.write('ARC: max: %s, avg: %s\n' % (str(arc_max), str(arc_avg)))

def destroyHash(StudentHashRecords):
    global hash_array
    hash_array = {}    


def main():
    initializeHash()
    
    # Insert students records
    with open(input_file_name, 'r') as input_file:
        records = input_file.readlines()
        for each_record in records:
            student_id = each_record.split('/')[0].strip()  # Getting student ID
            cgpa = each_record.split('/')[1].strip()  # Getting student CGPA
            insertStudentRec(hash_array, student_id, cgpa)
    
    with open(prompts_file_name, 'r') as input_file:
        records = input_file.readlines()
        for each_record in records:
            header = each_record.split(':')[0].strip()
            # Insert Hall Of Fame records
            if header == 'hallOfFame':
                cutoff_cgpa = each_record.split(':')[1].strip()
                cutoff_cgpa = float(cutoff_cgpa)
                hallOfFame(hash_array, cutoff_cgpa)
            # Insert Course Offer records
            elif header == 'courseOffer':
                cgpa_ranges = each_record.split(':')[1:]
                cgpa_from = float(cgpa_ranges[0].strip())
                cgpa_to = float(cgpa_ranges[1].strip())
                newCourseList(hash_array, cgpa_from, cgpa_to)

    depAvg(hash_array)
    destroyHash(hash_array)
    print('Completed Operations!, Kindly visit %s for the output'%output_file)

if __name__ == "__main__":
    main()
