import subprocess

FUNCTIONAL_TESTS_PATHS = [
    "test_lignes_du_journal.LignesDuJournal.test_consulter_journal",
    "test_lignes_du_journal.LignesDuJournal.test_ajouter_une_recette",
]


def run() -> None:
    errors = []
    tests_count = len(FUNCTIONAL_TESTS_PATHS)
    for test_index, ft_path in enumerate(FUNCTIONAL_TESTS_PATHS):
        print(f"Running test {test_index}/{tests_count}: {ft_path}")  # noqa: T201
        response = subprocess.run(  # noqa: S603
            ["python", "manage.py", "test", f"functional_tests.{ft_path}"],  # noqa: S607
            check=False,
        )
        if response.returncode != 0:
            errors.append(f"functional_tests.{ft_path}")
    print(f"Successful tests: {tests_count - len(errors)}/{tests_count}")  # noqa: T201
    if errors:
        print("Errors:")  # noqa: T201
        for error in errors:
            print(f"- {error}")  # noqa: T201
