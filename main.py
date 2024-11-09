import json
import os

def create_subject(subject):
  """Creates a new subject."""
  subjects_file = "subjects.json"
  dict = {}
  avl = False
  try:
    dict[subject] =[]
    with open(subjects_file, 'r+') as f:
      subjects = json.load(f)
      for index in range(len(subjects)) :
        for key in subjects[index]:
            if key == subject:
                print(f'   Sub {subject} already avl')
                avl = True
      if avl is False:
          subjects.append(dict)
          f.seek(0)
          json.dump(subjects, f, indent=4)
  except FileNotFoundError:
    with open(subjects_file, 'w') as f:
      json.dump([dict], f, indent=4)

def add_chapter(subject, chapter):
  """Adds a chapter to an existing subject."""
  subjects_file = "subjects.json"
  with open(subjects_file, 'r+') as f:
    subjects = json.load(f)
    for index in range(len(subjects)) :
        for key in subjects[index]:
            #print(key)
            if key == subject:
                list = subjects[index][key]
                if chapter not in list:
                    subjects[index][key].append(chapter)
                    print(f'   {chapter} added')
                else:
                    print(f'   chapter {chapter} already avl')
    f.seek(0)
    json.dump(subjects, f, indent=4)

def list_sub():
    subjects_file = "subjects.json"
    with open(subjects_file, 'r') as f:
        subjects = json.load(f)
        for index in range(len(subjects)) :
            for key in subjects[index]:
                print(f'   {key} ')

def list_chap(sub) :
    subjects_file = "subjects.json"
    with open(subjects_file, 'r') as f:
        subjects = json.load(f)
    for index in range(len(subjects)) :
        for key in subjects[index]:
            if key == sub:
                list = subjects[index][key]
    try:
      for ch in list:
        print(f'   {ch} ')
    except:
      print('   New Subject')

def get_subjects_with_chapters():
  """Retrieves a list of subjects with their chapters."""
  subjects_file = "subjects.json"
  try:
    with open(subjects_file, 'r') as f:
      return json.load(f)
  except FileNotFoundError:
    return []


def create_note(subject, chapter, topic, subtopic, notes):
  """Creates a new note and appends it to the subject's JSON file."""
  subject_dir = f"subjects/{subject}"
  if not os.path.exists(subject_dir):
    os.makedirs(subject_dir)

  file_path = f"{subject_dir}/{chapter}.json"

  try:
    with open(file_path, 'r+') as f:
      data = json.load(f)
      data.append({
        "topic": topic,
        "subtopic": subtopic,
        "notes": notes
      })
      f.seek(0)
      json.dump(data, f, indent=4)
  except FileNotFoundError:
    with open(file_path, 'w') as f:
      json.dump([
        {
          "topic": topic,
          "subtopic": subtopic,
          "notes": notes
        }
      ], f, indent=4)

def get_notes_by_chapter(subject, chapter):
  """Retrieves notes for a specific chapter."""
  file_path = f"subjects/{subject}/{chapter}.json"
  try:
    with open(file_path, 'r') as f:
      data = json.load(f)
      return data
  except FileNotFoundError:
    return []

def search_notes(subject, keyword):
  """Searches for notes containing a keyword within a subject."""
  file_path = f"subjects/{subject}"
  results = []
  for chapter_file in os.listdir(file_path):
    with open(os.path.join(file_path, chapter_file), 'r') as f:
      notes = json.load(f)
      for note in notes:
        if keyword.lower() in (note['topic'].lower() + note['subtopic'].lower() + note['notes'].lower()):
          results.append(note)
  return results

def edit_note(subject, chapter, index, updated_note):
  """Edits a specific note within a chapter."""
  file_path = f"subjects/{subject}/{chapter}.json"
  with open(file_path, 'r+') as f:
    data = json.load(f)
    data[index] = updated_note
    f.seek(0)
    json.dump(data, f, indent=4)

def delete_note(subject, chapter, index):
  """Deletes a specific note from a chapter."""
  file_path = f"subjects/{subject}/{chapter}.json"
  with open(file_path, 'r+') as f:
    data = json.load(f)
    del data[index]
    f.seek(0)
    json.dump(data, f, indent=4)

def take_note():
  global subject, chapter
  sb = subject
  ch = chapter
  tp = input('   topic: ')
  stp = input('   sub-topic: ')
  nts = input('   notes: ')
  clear_console()
  create_note(sb, ch, tp, stp, nts)
  create_subject(subject)
  add_chapter(subject, chapter)

def clear_console():
  global active_selection
  """Clears the console."""
  os.system('cls' if os.name == 'nt' else 'clear')
  active()

def select_sub():
  global subject, chapter
  list_sub() 
  subject = input('   Enter Sub: ')
  clear_console() 
  list_chap(subject)
  chapter= input('   Enter Chapter: ')
  clear_console() 

def view():
  global subject, chapter
  subject_dir = f"subjects/{subject}"
  if not os.path.exists(subject_dir):
    print('Sub or chap not exist.')

  file_path = f"{subject_dir}/{chapter}.json"

  try:
    with open(file_path, 'r') as f:
      data = json.load(f)
    for notes in data:
      print(json.dumps(notes, indent=4)) 
    x = input('0: exit, 1: cont. ')
    if int(x)==0:
      clear_console()
  except Exception as e:
    print(e)

def active():
  global subject, chapter, active_selection
  p = f'   Active Sub: {subject} Ch:{chapter} '
  print(p)


subject = '' 
chapter = '' 
active_selection = ''

               
select_sub()
# Example usage:
# ... (previous example usage)
while True:
  
  #print(active_selection)
  option = '   Options \n   1: Add Note\n   2: Select Sub & Ch \n   3: View \n   Ans: ' 
  x = input(option)
  if int(x) == 0:
    print('Exiting...')
    break
  elif int(x) == 1:
    clear_console()
    take_note()
  elif int(x) == 2:
    clear_console()
    select_sub()
  elif int(x)==3:
    clear_console()
    view()