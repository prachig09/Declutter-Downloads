from src import config
from src.file_handler import is_temp_file, process_file


def test_is_temp_file():
    assert is_temp_file("document.pdf.crdownload") is True
    assert is_temp_file("file.tmp") is True
    assert is_temp_file(".hidden_file") is True
    assert is_temp_file("uni_homework.pdf") is False

def test_tag_matching(tmp_path, monkeypatch):
    downloads = tmp_path / "Downloads"
    sem3_docs = tmp_path / "Documents" / "University"
    downloads.mkdir()
    sem3_docs.mkdir(parents=True)

    monkeypatch.setattr(config, "TAG_RULES", {"sem3_": str(sem3_docs)})
    monkeypatch.setattr(config, "DRY_RUN", False)

    test_file = downloads / "sem3_lecture1.pdf"
    test_file.write_text("dummy content")

    process_file(str(test_file))

    assert not test_file.exists()
    assert (sem3_docs / "sem3_lecture1.pdf").exists()
