#!/usr/bin/env python
import codecs, io, encodings
from encodings import utf_8
from inlinec.codec.parser import transform


def inlinec_transform(stream):
    output = transform(stream.readlines())
    return output.rstrip()


def inlinec_transform_string(input):
    stream = io.StringIO(bytes(input).decode("utf-8"))
    return inlinec_transform(stream)


def inlinec_decode(input, errors="strict"):
    return inlinec_transform_string(input), len(input)


class InlinecIncrementalDecoder(utf_8.IncrementalDecoder):
    def decode(self, input, final=False):
        self.buffer += input
        if final:
            buff = self.buffer
            self.buffer = b""
            return super(InlinecIncrementalDecoder, self).decode(
                inlinec_transform_string(buff).encode("utf-8"), final=True
            )
        else:
            return ""


class InlinecStreamReader(utf_8.StreamReader):
    def __init__(self, *args, **kwargs):
        codecs.StreamReader.__init__(self, *args, **kwargs)
        self.stream = io.StringIO(inlinec_transform(self.stream))


def search_function(encoding):
    if encoding != "inlinec":
        return None
    utf8 = encodings.search_function("utf8")
    return codecs.CodecInfo(
        name="inlinec",
        encode=utf8.encode,
        decode=inlinec_decode,
        incrementalencoder=utf8.incrementalencoder,
        incrementaldecoder=InlinecIncrementalDecoder,
        streamreader=InlinecStreamReader,
        streamwriter=utf8.streamwriter,
    )


codecs.register(search_function)
