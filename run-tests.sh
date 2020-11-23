check_manifest () {
    python -m check_manifest --ignore ".*-requirements.txt"
}

check_pytest () {
  python -m pytest
  tests_exit_code=$?
  exit "$tests_exit_code"
}


if [ $# -eq 0 ]
then
  check_manifest
  check_pytest
else
  for arg in "$@"
  do
      case $arg in
          --check-manifest) check_manifest;;
          --check-pytest) check_pytest;;
      esac
  done
fi
