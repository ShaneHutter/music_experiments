#!/usr/bin/env python3
"""
    Test to create a wave form with NumPy and play it as audio
"""

from pyaudio    import PyAudio , paFloat32
import numpy    as np

pa = PyAudio()

volume = 0.5
sample_rate = 44100
duration = 1
freq = 440

samples = (
    np.sin(
        2 * np.pi * np.arange( sample_rate * duration ) * freq / sample_rate
        )
    ).astype( np.float32 )

_stream_opt = {
    "format": paFloat32,
    "channels": 1,
    "rate": sample_rate,
    "output": True,
    }
stream = pa.open( **_stream_opt )

if __name__ == "__main__":
    ## Is there __enter__ for with?
    stream.write( volume * samples )
    stream.stop_stream()
    stream.close()
    pa.terminate()