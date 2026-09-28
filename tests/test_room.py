import pytest
from author.room import WritingRoom

def make(tmp_path):
    room=WritingRoom(tmp_path)
    parent="A parent scene."
    a=room.prepare_assignment(source_label="chapter.md", source_text=parent, channel="gemini", brief="Rewrite.", assignment_id="A1")
    return room,parent,a

def test_packet_is_source_bound(tmp_path):
    room,parent,a=make(tmp_path)
    packet=room.render_packet(a,parent)
    assert a.source_sha256 in packet
    with pytest.raises(ValueError): room.render_packet(a,parent+" changed")

def test_adopt_requires_human_decision(tmp_path):
    room,parent,a=make(tmp_path)
    c=room.ingest_return(a,"<<<BEGIN_CANDIDATE>>>\nBetter scene.\n<<<END_CANDIDATE>>>\nNEW_CANON: NONE")
    d=room.decide(c,action="adopt",human="author",reason="preferred after reading")
    assert room.promote(parent_text=parent,candidate=c,decision=d)=="Better scene."

def test_new_canon_blocks_promotion(tmp_path):
    room,parent,a=make(tmp_path)
    c=room.ingest_return(a,"<<<BEGIN_CANDIDATE>>>\nBetter scene.\n<<<END_CANDIDATE>>>\nNEW_CANON: hero has a secret sister")
    d=room.decide(c,action="adopt",human="author",reason="prose preferred")
    with pytest.raises(ValueError): room.promote(parent_text=parent,candidate=c,decision=d)

def test_wrong_parent_blocks_promotion(tmp_path):
    room,parent,a=make(tmp_path)
    c=room.ingest_return(a,"<<<BEGIN_CANDIDATE>>>\nBetter scene.\n<<<END_CANDIDATE>>>\nNEW_CANON: NONE")
    d=room.decide(c,action="adopt",human="author",reason="ok")
    with pytest.raises(ValueError): room.promote(parent_text="other parent",candidate=c,decision=d)
