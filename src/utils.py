from mido import MidiFile

def midi_to_note_events(midi_file_path):
    # Load the MIDI file
    mid = MidiFile(midi_file_path)
    
    # This will hold our note events
    note_events = []

    # Track absolute time in ticks
    current_time = 0
    
    # We need to keep track of note start times
    note_start_times = {}

    # Process each track in the MIDI file
    for track in mid.tracks:
        current_time = 0  # Reset time for each track
        for msg in track:
            # Update the current time
            current_time += msg.time
            
            # Check if this is a 'note on' message
            if msg.type == 'note_on' and msg.velocity > 0:
                # Record the start time of the note
                note_start_times[msg.note] = current_time
                
            # Check if this is a 'note off' message or a 'note on' with velocity=0
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                # Calculate the note duration and record the event
                start_time = note_start_times.pop(msg.note, None)
                if start_time is not None:  # Ensure the note was started earlier
                    duration = current_time - start_time
                    note_events.append((msg.note, start_time, current_time))

    # Convert ticks to seconds (assuming 500,000 microseconds per beat, which is MIDI's default)
    # For more accuracy with tempo changes, you'd need to handle tempo change events
    ticks_per_beat = mid.ticks_per_beat
    microseconds_per_beat = 500000  # MIDI default
    seconds_per_tick = microseconds_per_beat / (ticks_per_beat * 1000000.0)
    
    # Convert note event times from ticks to seconds
    note_events_in_seconds = [
        (note, start_time * seconds_per_tick, end_time * seconds_per_tick)
        for note, start_time, end_time in note_events
    ]

    return note_events_in_seconds


def ms_to_min_sec_centi(milliseconds):
    # Check if the time is negative and store this information
    is_negative = milliseconds < 0
    # Work with the absolute value of milliseconds to simplify calculations
    milliseconds = abs(milliseconds)
    
    seconds = milliseconds // 1000
    minutes = seconds // 60
    seconds = seconds % 60  # Remainder after dividing by 60
    centiseconds = (milliseconds % 1000) // 10  # Convert to centiseconds

    # Format the string to "MM:SS:CC", adding a '-' if the original time was negative
    formatted_time = "{:02d}:{:02d}:{:02d}".format(minutes, seconds, centiseconds)
    if is_negative:
        formatted_time = "-" + formatted_time

    return formatted_time