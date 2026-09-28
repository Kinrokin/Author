import pytest
from author.protocol import extract_enclosure, extract_new_canon, ProtocolError

def test_extract_enclosure():
    t="x\n<<<BEGIN_CANDIDATE>>>\nhello\n<<<END_CANDIDATE>>>\nNEW_CANON: NONE"
    assert extract_enclosure(t)=="hello"
    assert extract_new_canon(t)==("NONE",)

def test_duplicate_enclosure_rejected():
    t="<<<BEGIN_CANDIDATE>>>x<<<END_CANDIDATE>>><<<BEGIN_CANDIDATE>>>y<<<END_CANDIDATE>>>"
    with pytest.raises(ProtocolError): extract_enclosure(t)
