import enum

class Convert(enum.Enum):
    NONE = 0
    TO_DNA = 1
    TO_RNA = 2

# Ansi COlor Constants
COL_START =     '\x1b['

FG_BLACK =      '30'
FG_RED =        '31'
FG_GREEN =      '32'
FG_YELLOW =     '33'
FG_BLUE =       '34'
FG_MAGENTA =    '35'
FG_CYAN =       '36'
FG_DEFAULT =    '39'

BG_BLACK =      '40'
BG_RED =        '41'
BG_GREEN =      '42'
BG_YELLOW =     '43'
BG_BLUE =       '44'
BG_MAGENTA =    '45'
BG_CYAN =       '46'
BG_GRAY =       '100'
BG_GRAY =       '47'
BG_DEFAULT =    '49'

COL_END =       f'{COL_START}0'


def chunk_generator(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def convert_codon(codon):
    codon_table = { 
        'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M', 
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T', 
        'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K', 
        'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',                  
        'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L', 
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P', 
        'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q', 
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R', 
        'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V', 
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A', 
        'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E', 
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G', 
        'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S', 
        'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L', 
        'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_', 
        'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W', 
    } 
    codon = ''.join([convert_base(base, Convert.TO_DNA) for base in codon])
    return codon_table.get(codon, '?')

def horizontal_print(lsts, chunk_size):
    rows = []

    chunked = [list(chunk_generator(lst, chunk_size)) for lst in lsts]

    #print(chunked)

    for lst_chunks in chunked:
        for row_i, lst_chunk in enumerate(lst_chunks):
            #print(row_i)
            if len(rows) <= row_i:
                rows.append([])
            #print(lst_chunks[row_i])

            rows[row_i].append(' '.join(lst_chunks[row_i]))
            #rows[row_i].append(' '.join([' '.join(chunks) for chunks in row_chunks])
    #print()
    for row in rows:
        print('\n'.join(row))
        print('\n')


class Gene:
    def __init__(self, sequence):
        self.sequence = sequence.upper()

        self.generate_codons()

    def generate_codons(self, start=0, end=-1):
        if end == -1:
            end = len(self.sequence)
        self.codons = []
        self.aminos = []
        for codon in chunk_generator(self.sequence[start:end], 3):
            self.codons.append(codon)
            self.aminos.append(convert_codon(codon))

    def format_for_print(self, diff_idxs=[], diff_aminos=[], conv_code=Convert.NONE, start=0, end=-1):
        if end == -1:
            end = len(self.sequence)

        codons = format_gen_seq_to_bases(self.sequence[start:end], diff_idxs, conv_code)
        codons = [''.join(chunk) for chunk in chunk_generator(codons, 3)]

        aminos = []
        for amino_i, amino in enumerate(self.aminos):
            if amino_i in diff_aminos:
                amino = format_color_text(amino, bg=BG_GRAY)
            aminos.append(f' {amino} ')

        #aminos = [f' {amino} ' for amino_i, amino in enumerate(self.aminos)]

        return codons, aminos

    def __str__(self):
        idx_str = ''.join([str(i % 10) for i in range(len(self.sequence))])
        idx_str = [idx_str[i:i + 3] for i in range(0, len(idx_str), 3)]

        codons, aminos = self.format_for_print()

        aminos = ' '.join(aminos)
        idx_str = ' '.join(idx_str)
        codons = ' '.join(codons)
        return f'{aminos}\n{codons}'

    def visual_compare(self, other, start=0, end=-1):
        if end == -1:
            end = len(self.sequence)
        a_sequence = ''.join([convert_base(base, Convert.TO_RNA) for base in self.sequence[start:end]])
        b_sequence = ''.join([convert_base(base, Convert.TO_RNA) for base in other.sequence[start:end]])
        diff_idxs = [i for i in range(len(a_sequence)) if a_sequence[i] != b_sequence[i]]

        self.generate_codons(start=start, end=end)
        other.generate_codons(start=start, end=end)
        diff_aminos = [i for i in range(len(self.aminos)) if self.aminos[i] != other.aminos[i]]

        a_codons, a_aminos = self.format_for_print(diff_idxs, diff_aminos, conv_code=Convert.TO_RNA, start=start, end=end)
        b_codons, b_aminos = other.format_for_print(diff_idxs, diff_aminos, conv_code=Convert.TO_RNA, start=start, end=end)

        outputs = [
            a_aminos,
            a_codons,
            b_codons,
            b_aminos]

        print(f'Comparing sequences between offsets [{start}:{end}]')
        horizontal_print(outputs, 24)

        # Reset from offsets
        if start != 0 or end != 0:
            self.generate_codons()
            other.generate_codons()


def format_color_text(text, fg=FG_DEFAULT, bg=BG_DEFAULT):
    """ ANSI Color Codes
    See https://en.wikipedia.org/wiki/ANSI_escape_code
    """
    return f'{COL_START}{fg};{bg}m{text}{COL_END}m'

base_color_table = {
    'A': FG_GREEN,
    'T': FG_MAGENTA,
    'C': FG_BLUE,
    'G': FG_YELLOW,
    'U': FG_MAGENTA,
    'Ψ': FG_MAGENTA
}


def format_base(base, diff=None):
    return format_color_text(base, fg=base_color_table[base], bg=BG_GRAY if diff else BG_DEFAULT)


def convert_base(base, conv_code):
    if conv_code == Convert.TO_DNA:
        base = 'T' if base in ['U', 'Ψ'] else base
    if conv_code == Convert.TO_RNA:
        base = 'U' if base in ['T', 'Ψ']  else base
    return base


def format_gen_seq_to_bases(seq, diff_idxs=[], conv_code=Convert.NONE):
    bases = []
    for i, base in enumerate(seq):
        bases.append(format_base(convert_base(base, conv_code), diff=i in diff_idxs))

    return bases


def main():
    seq_a = 'ATCUGΨATCUGΨATCUGΨATCUGΨATCUGΨATCUGΨ'
    seq_b = 'ATCTGTATCTATATCTGTATCTGTATCTGTATCTGT'

    gene_a = Gene(seq_a)
    gene_b = Gene(seq_b)
    #print(gene_a)

    gene_a.visual_compare(gene_b)

    gene_a.visual_compare(gene_b, start=1)

    gene_a.visual_compare(gene_b, start=3, end=12)

if __name__ == '__main__':
    main()
