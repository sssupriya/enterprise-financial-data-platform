from shared.landing import get_landing_path


def test_landing_paths_are_unique():
    path1 = get_landing_path(
        "mobile",
        "2026-07-01"
    )

    path2 = get_landing_path(
        "mobile",
        "2026-07-01"
    )

    assert path1 != path2