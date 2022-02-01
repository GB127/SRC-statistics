from code_SRC.run_entry import Run

class Table_Runs:
    def __init__(self, data, level:bool):
        self.liste = []
        for run in data:
            tempo = Run(run)
            if level and tempo.level:
                self.liste.append(tempo)
            elif not tempo.level and not level:
                self.liste.append(tempo)
            


    def __len__(self):
        return len(self.liste)