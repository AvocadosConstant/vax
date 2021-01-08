from contextlib import contextmanager
import enum
import re

import ansi


class Convert(enum.Enum):
    NONE = 0
    TO_DNA = 1
    TO_RNA = 2


def format_base(base, diff=None):
    t_u_psi_color = 'MAGENTA'
    base_color = {
        'A': 'GREEN',
        'C': 'BLUE',
        'G': 'YELLOW',
        'T': t_u_psi_color,
        'U': t_u_psi_color,
        'Ψ': t_u_psi_color
    }
    diff_attr = (ansi.bg('DEFAULT'),)
    if diff:
        diff_attr = (ansi.BOLD,
                     ansi.UNDERLINE,
                     ansi.bg(base_color[base]),
                     ansi.fg('DEFAULT'))
    return ansi.format_text(base, ansi.fg(base_color[base]), *diff_attr)


def convert_base(base, conv_code):
    if conv_code == Convert.TO_DNA:
        base = 'T' if base in ['U', 'Ψ'] else base
    if conv_code == Convert.TO_RNA:
        base = 'U' if base in ['T', 'Ψ'] else base
    return base


def convert_codon(codon):
    codon_table = {
        'ATA': 'I', 'ATC': 'I', 'ATT': 'I', 'ATG': 'M',
        'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
        'AAC': 'N', 'AAT': 'N', 'AAA': 'K', 'AAG': 'K',
        'AGC': 'S', 'AGT': 'S', 'AGA': 'R', 'AGG': 'R',
        'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',
        'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
        'CAC': 'H', 'CAT': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
        'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
        'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
        'GAC': 'D', 'GAT': 'D', 'GAA': 'E', 'GAG': 'E',
        'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
        'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S',
        'TTC': 'F', 'TTT': 'F', 'TTA': 'L', 'TTG': 'L',
        'TAC': 'Y', 'TAT': 'Y', 'TAA': '*', 'TAG': '*',
        'TGC': 'C', 'TGT': 'C', 'TGA': '*', 'TGG': 'W',
    }
    codon = ''.join([convert_base(base, Convert.TO_DNA) for base in codon])
    return codon_table.get(codon, '?')


def format_gen_seq_to_bases(seq, diff_idxs=[], conv_code=Convert.NONE):
    bases = []
    for i, base in enumerate(seq):
        bases.append(format_base(
            convert_base(base, conv_code),
            diff=i in diff_idxs))

    return bases


def chunk_generator(lst, size):
    """ Yield successive chunks of a given size from lst """
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def format_lsts_to_rows(lsts, chunk_size):
    rows = []

    chunked = [list(chunk_generator(lst, chunk_size)) for lst in lsts]

    for lst_chunks in chunked:
        for row_i, _ in enumerate(lst_chunks):
            if len(rows) <= row_i:
                rows.append([])

            rows[row_i].append(' '.join(lst_chunks[row_i]))
    return rows


def horizontal_print(lsts, chunk_size):
    for row in format_lsts_to_rows(lsts, chunk_size):
        print('\n'.join(row) + '\n\n')


class Gene:
    def __init__(self, sequence='', from_file=''):
        if from_file:
            with open(from_file) as f:
                sequence = re.sub(r'(\d|\s)', '', ''.join(f.readlines()))

        self.sequence = sequence.upper()
        self.start = 0
        self.end = None

        self.generate_codons()

    def generate_codons(self):
        self.codons = []
        self.aminos = []
        for codon in chunk_generator(self.sequence[self.start:self.end], 3):
            self.codons.append(codon)
            self.aminos.append(convert_codon(codon))

    @contextmanager
    def reading_frame(self, start, end):
        """ Handles contexts for actions in a specific reading frame """
        # TODO: Make this a no-op if the reading frame doesn't change
        self.start = start
        self.end = end

        self.generate_codons()
        try:
            yield
        finally:
            self.start = 0
            self.end = len(self.sequence)
            self.generate_codons()

    def format_for_print(self,
                         diff_idxs=[],
                         diff_aminos=[],
                         conv_code=Convert.NONE):
        codons = format_gen_seq_to_bases(
            self.sequence[self.start:self.end], diff_idxs, conv_code)
        codons = [''.join(chunk) for chunk in chunk_generator(codons, 3)]

        aminos = []
        for amino_i, amino in enumerate(self.aminos):
            if amino_i in diff_aminos:
                aminos.append(ansi.format_text(
                    f' {amino} ',
                    ansi.BOLD,
                    ansi.UNDERLINE,
                    ansi.REVERSE))
            else:
                aminos.append(f' {amino} ')

        return codons, aminos

    def __str__(self):
        return self.display(display=False)

    def display(self,
                start=0, end=None,
                show_aminos=False,
                split_codons=True,
                display=True):
        """
        # For displaying position in the gene, currently unused
        idx_str = ''.join([str(i % 10) for i in range(len(self.sequence))])
        idx_str = [idx_str[i:i + 3] for i in range(0, len(idx_str), 3)]
        idx_str = delim.join(idx_str)
        """
        with self.reading_frame(start, end):
            codons, aminos = self.format_for_print()

            delim = ' ' if split_codons else ''

            aminos = delim.join(aminos)
            codons = delim.join(codons)

            out = str(codons)
            if show_aminos:
                out = f'{aminos}\n{codons}'
            if display:
                print(out)
                return None
            return out

    def find_diff_idxs(self, other):
        a_sequence = ''.join(
            [convert_base(base, Convert.TO_RNA)
             for base in self.sequence[self.start:self.end]])
        b_sequence = ''.join(
            [convert_base(base, Convert.TO_RNA)
             for base in other.sequence[self.start:self.end]])
        return [i for i in range(len(a_sequence))
                if a_sequence[i] != b_sequence[i]]

    def visual_compare(self, other, start=0, end=None):
        with self.reading_frame(start, end), other.reading_frame(start, end):
            diff_idxs = self.find_diff_idxs(other)
            diff_aminos = [i for i in range(len(self.aminos))
                           if self.aminos[i] != other.aminos[i]]

            a_codons, a_aminos = self.format_for_print(
                diff_idxs, diff_aminos, conv_code=Convert.TO_RNA)
            b_codons, b_aminos = other.format_for_print(
                diff_idxs, diff_aminos, conv_code=Convert.TO_RNA)

            outputs = [
                a_aminos,
                a_codons,
                b_codons,
                b_aminos]

            print(f'Comparing sequences between offsets '
                  f'[{start}:'
                  f'{end if end is not None else len(self.sequence)}]')
            horizontal_print(outputs, 24)
