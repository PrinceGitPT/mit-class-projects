"""
6.1010 Spring '23 Lab 0: Audio Processing
"""

import wave
import struct

# No additional imports allowed!


def backwards(sound):
    return {"rate": sound["rate"], "samples": sound["samples"][::-1]}


def mix(sound1, sound2, p):
    """
    Parameters
    ----------
    sound1 : DICT
    sound2 : DICT
    p : FLOAT
        Ratio to split the mix into; not commutative

    Returns
    -------
    DICT
        Dictionary with combination of sound1 and sound2 in the ratio p : (1-p)

    """

    # mix 2 good sounds
    if sound1["rate"] != sound2["rate"]:
        return
    r = sound1["rate"]  # get rate

    if "samples" in sound1.keys():

        sound1 = sound1["samples"]
        sound2 = sound2["samples"]

        if len(sound1) <= len(sound2):
            sound_length = len(sound1)
        else:
            sound_length = len(sound2)

        sound_sequence = []
        x = 0
        while x < sound_length:
            s2, s1 = p * sound1[x], sound2[x] * (1 - p)
            sound_sequence.append(s1 + s2)  # add sounds
            x += 1

        return {"rate": r, "samples": sound_sequence}

    else:
        sound1_left = sound1["left"]
        sound1_right = sound1["right"]

        sound2_left = sound2["left"]
        sound2_right = sound2["right"]

        if len(sound1_left) <= len(sound2_left):
            sound_length = len(sound1_left)
        else:
            sound_length = len(sound2_left)

        sound_sequence_left = []
        x = 0
        while x < sound_length:
            s2, s1 = p * sound1_left[x], sound2_left[x] * (1 - p)
            sound_sequence_left.append(s1 + s2)  # add sounds
            x += 1

        if len(sound1_right) <= len(sound2_right):
            sound_length = len(sound1_right)
        else:
            sound_length = len(sound2_right)

        sound_sequence_right = []
        x = 0
        while x < sound_length:
            s2, s1 = p * sound1_right[x], sound2_right[x] * (1 - p)
            sound_sequence_right.append(s1 + s2)  # add sounds
            x += 1

        return {"rate": r, "left": sound_sequence_left, "right": sound_sequence_right}


def convolve(sound, kernel):
    """
    Applies a filter to a sound, resulting in a new sound that is longer than
    the original mono sound by the length of the kernel - 1.
    Does not modify inputs.

    Args:
        sound: A mono sound dictionary with two key/value pairs:
            * "rate": an int representing the sampling rate, samples per second
            * "samples": a list of floats containing the sampled values
        kernel: A list of numbers

    Returns:
        A new mono sound dictionary.
    """
    # samples = []  # a list of scaled sample lists

    # for i, scale in enumerate(kernel):
    #     scaled_sample = [0] * i  # offset scaled sound by filter index
    #     scaled_sample += [scale * x for x in sound["samples"]]
    #     samples.append(scaled_sample)

    # # combine samples into one list
    # final_sample = []
    # for sample in samples:
    #     for i, val in enumerate(sample):
    #         # if not long enough, add [0] to end
    #         if i >= len(final_sample):
    #             final_sample = final_sample + [0]

    #         # update final sample with new sample value
    #         new_sample = [0] * len(final_sample)
    #         new_sample[i] = val
    #         for j, prev_val in enumerate(final_sample):
    #             new_sample[j] += prev_val
    #         final_sample = new_sample

    sample_list = sound["samples"]
    length = len(sample_list) + len(kernel) - 1
    final_sample = [0] * length
    for kernel_boy in enumerate(kernel):
        if kernel_boy[1] != 0:
            for sample in enumerate(sample_list):
                final_sample[kernel_boy[0] + sample[0]] += kernel_boy[1] * sample[1]

    return {"rate": sound["rate"], "samples": final_sample}


def echo(sound, num_echoes, delay, scale):
    """
    Compute a new signal consisting of several scaled-down and delayed versions
    of the input sound. Does not modify input sound.

    Args:
        sound: a dictionary representing the original mono sound
        num_echoes: int, the number of additional copies of the sound to add
        delay: float, the amount of seconds each echo should be delayed
        scale: float, the amount by which each echo's samples should be scaled

    Returns:
        A new mono sound dictionary resulting from applying the echo effect.
    """
    sample_delay = round(delay * sound["rate"])
    echo_filter = [0] * (sample_delay * num_echoes + 1)
    echo_filter[0] = 1

    new = 1
    for i in range(sample_delay, len(echo_filter), sample_delay):
        new *= scale
        echo_filter[i] += new

    return convolve(sound, echo_filter)


def pan(sound):
    """


    Parameters
    ----------
    sound : DICT
        A dictionary representing the stereo sound

    Returns
    -------
    dict
        A dictionary representing a panned version of the stereo
        sound (sound "moves" from left speaker to right)

    """
    left_speaker = sound["left"][:]
    right_speaker = sound["right"][:]
    sample_length = len(left_speaker)
    rate = sound["rate"]

    for i in range(sample_length):
        left_speaker[i] *= 1 - i / (sample_length - 1)
        right_speaker[i] *= i / (sample_length - 1)

    return {"rate": rate, "left": left_speaker, "right": right_speaker}


def remove_vocals(sound):
    """
    Parameters
    ----------
    sound : DICT
        A dictionary containing the original stereo sound

    Returns
    -------
    dict
        A dictionary containing the new karaoke sound

    """
    left_speaker = sound["left"][:]
    right_speaker = sound["right"][:]
    sample_length = len(left_speaker)
    rate = sound["rate"]
    new_mono = []

    for i in range(sample_length):
        new_mono.append(left_speaker[i] - right_speaker[i])

    return {"rate": rate, "samples": new_mono}


# below are helper functions for converting back-and-forth between WAV files
# and our internal dictionary representation for sounds


def bass_boost_kernel(boost, scale=0):
    """
    Constructs a kernel that acts as a bass-boost filter.

    We start by making a low-pass filter, whose frequency response is given by
    (1/2 + 1/2cos(Omega)) ^ N

    Then we scale that piece up and add a copy of the original signal back in.

    Args:
        boost: an int that controls the frequencies that are boosted (0 will
            boost all frequencies roughly equally, and larger values allow more
            focus on the lowest frequencies in the input sound).
        scale: a float, default value of 0 means no boosting at all, and larger
            values boost the low-frequency content more);

    Returns:
        A list of floats representing a bass boost kernel.
    """
    # make this a fake "sound" so that we can use the convolve function
    base = {"rate": 0, "samples": [0.25, 0.5, 0.25]}
    kernel = {"rate": 0, "samples": [0.25, 0.5, 0.25]}
    for i in range(boost):
        kernel = convolve(kernel, base["samples"])
    kernel = kernel["samples"]

    # at this point, the kernel will be acting as a low-pass filter, so we
    # scale up the values by the given scale, and add in a value in the middle
    # to get a (delayed) copy of the original
    kernel = [i * scale for i in kernel]
    kernel[len(kernel) // 2] += 1

    return kernel


def load_wav(filename, stereo=False):
    """
    Load a file and return a sound dictionary.

    Args:
        filename: string ending in '.wav' representing the sound file
        stereo: bool, by default sound is loaded as mono, if True sound will
            have left and right stereo channels.

    Returns:
        A dictionary representing that sound.
    """
    sound_file = wave.open(filename, "r")
    chan, bd, sr, count, _, _ = sound_file.getparams()

    assert bd == 2, "only 16-bit WAV files are supported"

    out = {"rate": sr}

    left = []
    right = []
    for i in range(count):
        frame = sound_file.readframes(1)
        if chan == 2:
            left.append(struct.unpack("<h", frame[:2])[0])
            right.append(struct.unpack("<h", frame[2:])[0])
        else:
            datum = struct.unpack("<h", frame)[0]
            left.append(datum)
            right.append(datum)

    if stereo:
        out["left"] = [i / (2**15) for i in left]
        out["right"] = [i / (2**15) for i in right]
    else:
        samples = [(ls + rs) / 2 for ls, rs in zip(left, right)]
        out["samples"] = [i / (2**15) for i in samples]

    return out


def write_wav(sound, filename):
    """
    Save sound to filename location in a WAV format.

    Args:
        sound: a mono or stereo sound dictionary
        filename: a string ending in .WAV representing the file location to
            save the sound in
    """
    outfile = wave.open(filename, "w")

    if "samples" in sound:
        # mono file
        outfile.setparams((1, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = [int(max(-1, min(1, v)) * (2**15 - 1)) for v in sound["samples"]]
    else:
        # stereo
        outfile.setparams((2, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = []
        for l_val, r_val in zip(sound["left"], sound["right"]):
            l_val = int(max(-1, min(1, l_val)) * (2**15 - 1))
            r_val = int(max(-1, min(1, r_val)) * (2**15 - 1))
            out.append(l_val)
            out.append(r_val)

    outfile.writeframes(b"".join(struct.pack("<h", frame) for frame in out))
    outfile.close()


if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place to put your
    # code for generating and saving sounds, or any other code you write for
    # testing, etc.

    # here is an example of loading a file (note that this is specified as
    # sounds/hello.wav, rather than just as hello.wav, to account for the
    # sound files being in a different directory than this file)
    hello = load_wav("sounds/hello.wav")
    
    chord = load_wav("sounds/chord.wav")
    echoed_chord = echo(chord, 5, 0.3, 0.6)
    write_wav(echoed_chord, "echoed_chord.wav")
