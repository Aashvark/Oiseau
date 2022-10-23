class SimpleError: 
    def __init__(self, type_, note) -> None: 
        print(f"{type_}: {note.lower()}")
        quit()
