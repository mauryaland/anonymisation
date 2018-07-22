from generate_trainset.modify_strings import get_title_case, random_case_change, remove_corp, remove_key_words


def test_remove_corp_name():
    assert remove_corp("SA Toto") == "Toto"
    assert remove_corp("SA Toto Titi") == "Toto Titi"


def test_title_case():
    assert get_title_case("mic ben toto") == "Mic Ben Toto"


def test_random_case_change():
    text = "La Banque est fermée"
    offsets = [(3, 9, "PARTIE_PP")]

    results = [random_case_change(text, offsets, 100) for _ in range(1, 100)]

    assert "La Banque est fermée" in results
    assert "La banque est fermée" in results
    assert "La BANQUE est fermée" in results


def test_remove_key_words():
    text = "Ayant pour conseil Me Myriam MASSENGO LACAVE et Me Toto TITI, " \
           "avocat au barreau de PARIS, toque: B1132"
    offsets = [(22, 44, "AVOCAT"), (51, 60, "AVOCAT")]
    assert remove_key_words(text=text, offsets=offsets, rate=100) == ('Ayant pour conseil Myriam MASSENGO LACAVE '
                                                                      'et Toto TITI, avocat au barreau de PARIS, '
                                                                      'toque: B1132',
                                                                      [(19, 41, 'AVOCAT'),
                                                                       (45, 54, 'AVOCAT')])

    assert remove_key_words(text=text, offsets=offsets, rate=0) == (text, offsets)
