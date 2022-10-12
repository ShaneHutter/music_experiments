#!/usr/bin/env python3
"""
    Calculate Equal temperment for and number of semi tones per octave
    Notes are all alphabetic, there are no sharps and flats
    total semitones in an octave limited to 52, allowing a note to 
    be represented as an upper case or lowercase


sidereal_period_sec = ( 23 * 60 * 60 ) + ( 56 * 60 ) + 4.09053
sidereal_period_sec
earth_hz = 1 / sidereal_period_sec
earth_hz
for octave in range( 1 , 100 ):
        for num , note in enumerate( notes ):
                earth_hz *= 2 ** ( 1 /12 )
                if earth_hz > 400 and earth_hz < 450:
                        print( earth_hz )
notes = ( "C","C#","D","D#","E","F","F#","G","G#","A","A#","B" )
for octave in range( 1 , 100 ):
        for num , note in enumerate( notes ):
                earth_hz *= 2 ** ( 1 /12 )
                if earth_hz > 400 and earth_hz < 450:
                        print( earth_hz )

    Later create sharps and flats after geometrically working out scale patterns
"""

from string import ascii_uppercase , ascii_lowercase
from yaml   import safe_dump
from numpy  import arange , array , unique

NOTES = ascii_uppercase + ascii_lowercase
EARTH_SIDERAL_HZ = 1 / ( ( 23 * 60 * 60 ) + ( 56 * 60 ) + 4.09053 )
AUDIBLE_RANGE = range( 20 , 20000 )

class ToManySemitonesError( Exception ):
    """More than 52 semitones not supported"""
    pass


def eqtemp_gen( semitones = 13 , base_freq = EARTH_SIDERAL_HZ ):
    """
        Generate note frequencies for x semitones per octave starting with y base frequency

        This needs to off set it self so that Octave 0 is the first one that has 20hz in it
        Maybe even detect the first Octave above 20,000Hz instead of taking octave as an argument
    """
    _ret = {}
    if semitones > len( NOTES ):
        raise ToManySemitonesError()
    _used_notes = NOTES[ :semitones ]
    _increase = 2 ** ( 1 / semitones )
    # Determine actual octave range
    def _determine_octave_offset():
        _check_freq = base_freq
        _octave = 0 
        while _check_freq < AUDIBLE_RANGE.stop:
            for note in _used_notes:
                if _check_freq > AUDIBLE_RANGE.start:
                    return _octave
                _check_freq *= _increase
            _octave += 1
    _octave_offset = _determine_octave_offset()
    _current_freq = base_freq
    _octave = 0
    while _current_freq < AUDIBLE_RANGE.stop:
        for note in _used_notes:
            _adjusted_octave = _octave - _octave_offset
            if _adjusted_octave >= 0:
                _current_note = f"{note}{_adjusted_octave}"
                _ret[ _current_note ] = _current_freq
            _current_freq *= _increase
        _octave += 1
    return _ret


def generate_modes( semitones , notes_per_mode ):
    """Deterine intervals between notes for modes

    using: _step_count.append( int( x % notes_per_mode ) )
        with a negative offset, and 12 semitones, 7 notes per mode
        will start with Lydian (F) and procead via modes
        in the "alphabetic" order ( natural: F , G , A , B , C , D , E )

        When this is done geometrically it shifts by tone
         Lydian , Myxo ... phrygian , locrean , then key shift up a 5th and repeat

    """
    _modes = []
    for offset in range( notes_per_mode ):
        _step_count = []
        for x in arange( 0 - offset , notes_per_mode - offset , notes_per_mode / semitones ):
            _step_count.append( int( x % notes_per_mode ) )
        _intervals = []
        for x in unique( array( _step_count ) ):
            _intervals.append( 
                str(
                    _step_count.count( x )
                    )
                )
        _modes.append( " ".join( _intervals ) )
    return _modes



    




if __name__ == "__main__":
    pass
    """
    print(
        safe_dump(
            eqtemp_gen()
            )
        )
    """
    print(
        safe_dump(
            generate_modes( 12 , 7 )
            )
        )