from dna import *
import pytest


@pytest.fixture
def gene_a():
    seq = 'ATCUGΨ'
    return Gene(seq)


@pytest.fixture
def gene():
    seq = 'ATCUGΨATCAUGΨATCUGΨATCUGΨATCUGΨATCUG'
    return Gene(seq)


def test_display_basic(gene_a):
    output = gene_a.display(
        split_codons=False, show_aminos=False, display=False)
    print(output)

    correct = ('\x1b[32;49mA\x1b[0m'
               '\x1b[35;49mT\x1b[0m'
               '\x1b[34;49mC\x1b[0m'
               '\x1b[35;49mU\x1b[0m'
               '\x1b[33;49mG\x1b[0m'
               '\x1b[35;49mΨ\x1b[0m')
    assert output == correct


def test_display_split(gene_a):
    output = gene_a.display(
        split_codons=True, show_aminos=False, display=False)
    print(output)


    correct = ('\x1b[32;49mA\x1b[0m'
               '\x1b[35;49mT\x1b[0m'
               '\x1b[34;49mC\x1b[0m'
               ' '
               '\x1b[35;49mU\x1b[0m'
               '\x1b[33;49mG\x1b[0m'
               '\x1b[35;49mΨ\x1b[0m')
    assert output == correct


def test_display_split_aminos(gene_a):
    output = gene_a.display(
        split_codons=True, show_aminos=True, display=False)
    print(output)


    correct = (' I   C \n'
              '\x1b[32;49mA\x1b[0m'
              '\x1b[35;49mT\x1b[0m'
              '\x1b[34;49mC\x1b[0m'
              ' '
              '\x1b[35;49mU\x1b[0m'
              '\x1b[33;49mG\x1b[0m'
              '\x1b[35;49mΨ\x1b[0m')
    assert output == correct


def test_display_frame(gene_a):
    output = gene_a.display(
        start=2, end=5,
        split_codons=False,
        show_aminos=False,
        display=False)
    print(output)


    correct = ('\x1b[34;49mC\x1b[0m'
               '\x1b[35;49mU\x1b[0m'
               '\x1b[33;49mG\x1b[0m')
    assert output == correct


def test_display_frame_aminos(gene_a):
    output = gene_a.display(
        start=2, end=5,
        split_codons=False,
        show_aminos=True,
        display=False)
    print(output)


    correct = (' L \n'
               '\x1b[34;49mC\x1b[0m'
               '\x1b[35;49mU\x1b[0m'
               '\x1b[33;49mG\x1b[0m')
    assert output == correct


def test_visual_compare():
    seq_a = 'ATCUGΨATCAUGΨATCUGΨATCUGΨATCUGΨATCUG'
    seq_b = 'ATCTGTATCATATATCTGTATCTGTATCTGTATCTG'

    gene_a = Gene(seq_a)
    gene_b = Gene(seq_b)

    print()
    gene_a.visual_compare(gene_b)
    gene_a.visual_compare(gene_b, start=1)
    gene_a.visual_compare(gene_b, start=3, end=12)
