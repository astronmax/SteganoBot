import math
import struct
import sys
import wave


def get_size_to_hide(sound_path, num_lsb):
    """
    Returns the amount of bytes available for hiding with that amount of LSB

    :param sound_path: Path to audio file
    :param num_lsb: Number of LSBs to use
    :return: Amount of bytes
    """
    global n_samples
    prepare(sound_path, num_lsb)
    max_bytes_to_hide = (n_samples * num_lsb) // 8
    return max_bytes_to_hide


def prepare(sound_path, num_lsb):
    """
    Loads .wav file data and specifications

    :param sound_path: Path to audio file
    :param num_lsb: Number of LSBs to use
    :return: None
    """
    global sound, params, n_frames, n_samples, fmt, mask, smallest_byte
    sound = wave.open(sound_path, "r")

    params = sound.getparams()
    num_channels = sound.getnchannels()
    sample_width = sound.getsampwidth()
    n_frames = sound.getnframes()
    n_samples = n_frames * num_channels

    if sample_width == 1:  # samples are unsigned 8-bit integers
        fmt = "{}B".format(n_samples)
        # Used to set the least significant num_lsb bits of an integer to zero
        mask = (1 << 8) - (1 << num_lsb)
        # The least possible value for a sample in the sound file is actually
        # zero, but we don't skip any samples for 8 bit depth wav files.
        smallest_byte = -(1 << 8)
    elif sample_width == 2:  # samples are signed 16-bit integers
        fmt = "{}h".format(n_samples)
        # Used to set the least significant num_lsb bits of an integer to zero
        mask = (1 << 15) - (1 << num_lsb)
        # The least possible value for a sample in the sound file
        smallest_byte = -(1 << 15)
    else:
        # Python's wave module doesn't support higher sample widths
        raise ValueError("File has an unsupported bit-depth")


def hide_bytes(sound_path, input_data, output_path, num_lsb):
    """
    Hides bytes in .wav file using LSB

    :param sound_path: Path to audio file
    :param input_data: Path to file to hide
    :param output_path: Path to output audio file
    :param num_lsb: Number of LSBs to use
    :return: None
    """
    global sound, params, n_frames, n_samples, fmt, mask, smallest_byte
    prepare(sound_path, num_lsb)
    # We can hide up to num_lsb bits in each sample of the sound file
    max_bytes_to_hide = (n_samples * num_lsb) // 8
    byte_size = sys.getsizeof(input_data)

    if byte_size > max_bytes_to_hide:
        required_lsbs = math.ceil(byte_size * 8 / n_samples)
        raise ValueError("Input file too large to hide, "
                         "requires {} LSBs, using {}"
                         .format(required_lsbs, num_lsb))

    print("Using {} B out of {} B".format(byte_size, max_bytes_to_hide))

    # Put all the samples from the sound file into a list
    raw_data = list(struct.unpack(fmt, sound.readframes(n_frames)))
    sound.close()

    # The number of bits we've processed from the input file
    data_index = 0
    sound_index = 0

    # values will hold the altered sound data
    values = []
    buffer = 0
    buffer_length = 0
    done = False

    while not done:
        while buffer_length < num_lsb and data_index // 8 < len(input_data):
            # If we don't have enough data in the buffer, add the
            # rest of the next byte from the file to it.
            buffer += (input_data[data_index // 8] >> (data_index % 8)
                       ) << buffer_length
            bits_added = 8 - (data_index % 8)
            buffer_length += bits_added
            data_index += bits_added

        # Retrieve the next num_lsb bits from the buffer for use later
        current_data = buffer % (1 << num_lsb)
        buffer >>= num_lsb
        buffer_length -= num_lsb

        while (sound_index < len(raw_data) and
               raw_data[sound_index] == smallest_byte):
            # If the next sample from the sound file is the smallest possible
            # value, we skip it. Changing the LSB of such a value could cause
            # an overflow and drastically change the sample in the output.
            values.append(struct.pack(fmt[-1], raw_data[sound_index]))
            sound_index += 1

        if sound_index < len(raw_data):
            current_sample = raw_data[sound_index]
            sound_index += 1

            sign = 1
            if current_sample < 0:
                # We alter the LSBs of the absolute value of the sample to
                # avoid problems with two's complement. This also avoids
                # changing a sample to the smallest possible value, which we
                # would skip when attempting to recover data.
                current_sample = -current_sample
                sign = -1

            # Bitwise AND with mask turns the num_lsb least significant bits
            # of current_sample to zero. Bitwise OR with current_data replaces
            # these least significant bits with the next num_lsb bits of data.
            altered_sample = sign * ((current_sample & mask) | current_data)

            values.append(struct.pack(fmt[-1], altered_sample))

        if data_index // 8 >= len(input_data) and buffer_length <= 0:
            done = True

    while sound_index < len(raw_data):
        # At this point, there's no more data to hide. So we append the rest of
        # the samples from the original sound file.
        values.append(struct.pack(fmt[-1], raw_data[sound_index]))
        sound_index += 1

    sound_steg = wave.open(output_path, "w")
    sound_steg.setparams(params)
    sound_steg.writeframes(b"".join(values))
    sound_steg.close()
    print("Data hidden over {} audio file".format(output_path))


def recover_data(sound_path, output_path, num_lsb, bytes_to_recover):
    """
    Gets bytes from .wav file, saves suggested file and returns bytes

    :param sound_path: Path to audio file
    :param output_path: Path to decoded file
    :param num_lsb: Number of LSBs to use
    :param bytes_to_recover: Amount of bytes hidden
    :return: Bytes of hidden data
    """
    # Recover data from the file at sound_path to the file at output_path
    global sound, n_frames, n_samples, fmt, smallest_byte
    prepare(sound_path, num_lsb)

    # Put all the samples from the sound file into a list
    raw_data = list(struct.unpack(fmt, sound.readframes(n_frames)))
    # Used to extract the least significant num_lsb bits of an integer
    mask = (1 << num_lsb) - 1
    output_file = None
    if output_path != "":
        output_file = open(output_path, "wb+")

    data = bytearray()
    sound_index = 0
    buffer = 0
    buffer_length = 0
    sound.close()

    while bytes_to_recover > 0:

        next_sample = raw_data[sound_index]
        if next_sample != smallest_byte:
            # Since we skipped samples with the minimum possible value when
            # hiding data, we do the same here.
            buffer += (abs(next_sample) & mask) << buffer_length
            buffer_length += num_lsb
        sound_index += 1

        while buffer_length >= 8 and bytes_to_recover > 0:
            # If we have more than a byte in the buffer, add it to data
            # and decrement the number of bytes left to recover.
            current_data = buffer % (1 << 8)
            buffer >>= 8
            buffer_length -= 8
            data += struct.pack('1B', current_data)
            bytes_to_recover -= 1

    if output_file is not None:
        output_file.write(bytes(data))
        output_file.close()
    print("Data recovered to {} file".format(output_path))
    return data
