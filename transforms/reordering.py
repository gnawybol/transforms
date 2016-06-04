__author__ = "Martin Etnestad Johansen"
__copyright__ = "Copyright 2015, Martin Etnestad Johansen"


from abc import ABCMeta, abstractstaticmethod
from collections import defaultdict, Counter


class ReorderingTransform(metaclass=ABCMeta):

    @abstractstaticmethod
    def iter_byte_indexes(len_bytes):
        """
        :param len_bytes:
        :type len_bytes:
        :return:
        :rtype:
        """

    @abstractstaticmethod
    def iter_sorted_bytes(byte_counter):
        """
        :param byte_counter:
        :type byte_counter:
        :return:
        :rtype:
        """

    @classmethod
    def forward(cls, input_bytes):
        """
        :param input_bytes:
        :type input_bytes:
        :return:
        :rtype:
        """
        successors_map = defaultdict(bytearray)
        first_byte = prev_byte = None

        for index in cls.iter_byte_indexes(len(input_bytes)):
            curr_byte = input_bytes[index]

            if first_byte is None:
                first_byte = curr_byte

            if prev_byte is not None:
                successors_map[prev_byte].append(curr_byte)

            prev_byte = curr_byte

        successors_map[prev_byte].append(first_byte)

        for successor_list in successors_map.values():
            successor_list.reverse()

        transformed_bytes = bytearray(input_bytes)

        index = 0
        for byte, count in cls.iter_sorted_bytes(Counter(input_bytes)):
            successor_list = successors_map[byte]
            transformed_bytes[index:index + count] = successor_list[:count]
            index += count

            if len(successor_list) == count:
                del(successors_map[byte])
            else:
                successors_map[byte] = successor_list[count:]

        assert(not successors_map.keys())

        transformed_bytes.append(first_byte)

        return transformed_bytes

    @classmethod
    def inverse(cls, input_bytes):
        first_byte = input_bytes.pop()

        successors_map = defaultdict(bytearray)
        bytes_len = len(input_bytes)

        start_index = 0
        for prev_byte, count in cls.iter_sorted_bytes(Counter(input_bytes)):
            successors_map[prev_byte].extend(input_bytes[start_index:start_index + count])
            start_index += count

        assert(start_index == bytes_len)

        plain_bytes = bytearray(input_bytes)
        curr_byte = first_byte
        for index in cls.iter_byte_indexes(bytes_len):
            plain_bytes[index] = curr_byte
            curr_byte = successors_map[curr_byte].pop()

        return plain_bytes


class BWT(ReorderingTransform):

    @staticmethod
    def iter_byte_indexes(len_bytes):
        return range(len_bytes)

    @staticmethod
    def iter_sorted_bytes(byte_counter):
        for byte in sorted(byte_counter):
            yield(byte, byte_counter[byte])
