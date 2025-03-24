class MusicFunctions:
    """class that provides special function handling for music notation"""
    
    @staticmethod
    def transpose(note, semitones):
        """transpose a note by given number of semitones"""
        notes = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
        if note.lower() not in notes:
            raise ValueError(f"Invalid note: {note}")
        
        idx = notes.index(note.lower())
        new_idx = (idx + semitones) % 12
        return notes[new_idx]
    
    @staticmethod
    def tempo_variation(base_tempo, factor):
        """calculate a tempo variation"""
        return int(base_tempo * factor)
    
    @staticmethod
    def frequency(note, octave=4):
        """calculate frequency in Hz for a given note and octave"""
        # a4 is 440hz
        notes = {'c': -9, 'c#': -8, 'd': -7, 'd#': -6, 'e': -5, 
                 'f': -4, 'f#': -3, 'g': -2, 'g#': -1, 'a': 0, 
                 'a#': 1, 'b': 2}
        
        if note.lower() not in notes:
            raise ValueError(f"Invalid note: {note}")
        
        # Calculate semitones from a4
        n = notes[note.lower()] + (octave - 4) * 12
        
        # Calculate frequency using standard formula: f = 440 * 2^(n/12)
        return 440 * (2 ** (n / 12))

def parse_function_call(command, args):
    """parse and execute a function call from tokens"""
    if not hasattr(MusicFunctions, command):
        return f"Unknown function: {command}"
    
    try:
        func = getattr(MusicFunctions, command)
        # Convert string args to appropriate types when possible
        parsed_args = []
        for arg in args:
            try:
                # Try to convert to float first
                parsed_args.append(float(arg))
            except ValueError:
                # If not a number, keep as string
                parsed_args.append(arg)
        
        result = func(*parsed_args)
        return result
    except Exception as e:
        return f"Error executing {command}: {str(e)}"

def get_available_functions():
    """get a list of available music functions"""
    return [func for func in dir(MusicFunctions) 
            if callable(getattr(MusicFunctions, func)) and not func.startswith('_')] 